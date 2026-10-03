use futures::{AsyncRead, AsyncReadExt, AsyncWrite, AsyncWriteExt};
use libp2p::{request_response, StreamProtocol};
use mpe_core::{
    store::{Cursor, InvPage, Page, Receipt, TimeWindow},
    wire::Eid,
};
use serde::{Deserialize, Serialize};
use std::{
    collections::BTreeMap,
    io,
    sync::{Arc, Mutex, RwLock},
};
pub const FRAME_CAP: usize = 65536;
#[derive(Clone, Debug, Serialize, Deserialize)]
pub enum Request {
    Publish(Vec<u8>),
    Feed {
        shard: u8,
        after: u64,
    },
    Backfill {
        shard: u8,
        from: Cursor,
        until: u64,
    },
    Inventory {
        shard: u8,
        window: TimeWindow,
        after: Option<Eid>,
    },
    Receipts {
        shard: u8,
        window: TimeWindow,
        after: Option<Eid>,
    },
    AnchorLeaves {
        window: u64,
        shard: u8,
    },
    Inclusion {
        eid: Eid,
    },
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub enum Response {
    Accepted {
        eid: Eid,
    },
    Feed {
        cursor: u64,
        envelopes: Vec<Vec<u8>>,
    },
    Backfill(Page),
    Inventory(InvPage),
    Receipts {
        receipts: Vec<Receipt>,
        next: Option<Eid>,
    },
    AnchorLeaves(Vec<Eid>),
    Inclusion(mpe_core::anchor::InclusionProof),
    Busy,
    Refused,
}
#[derive(Default, Debug)]
pub struct CaptureStats {
    pub sizes: BTreeMap<usize, u64>,
    pub leaks: u64,
    pub frames: u64,
    pub unsigned_messages: u64,
    pub signed_messages: u64,
}
type MatcherCache = Arc<Mutex<Option<(usize, Arc<aho_corasick::AhoCorasick>)>>>;
#[derive(Clone, Default)]
pub struct Capture {
    pub stats: Arc<Mutex<CaptureStats>>,
    pub forbidden: Arc<RwLock<Vec<Vec<u8>>>>,
    matcher: MatcherCache,
}
impl Capture {
    pub fn frame(&self, bytes: &[u8]) {
        let matcher = self.forbidden.read().ok().and_then(|strings| {
            let mut cache = self.matcher.lock().ok()?;
            if cache
                .as_ref()
                .is_none_or(|(count, _)| *count != strings.len())
            {
                let patterns: Vec<_> = strings.iter().filter(|s| s.len() >= 8).collect();
                let matcher = aho_corasick::AhoCorasick::new(patterns).ok()?;
                *cache = Some((strings.len(), Arc::new(matcher)));
            }
            cache.as_ref().map(|(_, matcher)| matcher.clone())
        });
        let leak = matcher.is_some_and(|matcher| matcher.is_match(bytes));
        if let Ok(mut stats) = self.stats.lock() {
            stats.frames += 1;
            if leak {
                stats.leaks += 1;
            }
        }
    }
    pub fn envelope(&self, bytes: &[u8]) {
        if let Ok(mut stats) = self.stats.lock() {
            *stats.sizes.entry(bytes.len()).or_default() += 1;
        }
        self.frame(bytes);
    }
    fn request(&self, r: &Request) {
        if let Request::Publish(b) = r {
            self.envelope(b);
        }
    }
    fn response(&self, r: &Response) {
        match r {
            Response::Feed { envelopes, .. } => {
                for b in envelopes {
                    self.envelope(b);
                }
            }
            Response::Backfill(p) => {
                for b in &p.envelopes {
                    self.envelope(b);
                }
            }
            _ => {}
        }
    }
}
#[derive(Clone, Default)]
pub struct Codec {
    pub capture: Capture,
}
fn invalid(e: impl std::fmt::Display) -> io::Error {
    io::Error::new(io::ErrorKind::InvalidData, e.to_string())
}
async fn read<T: AsyncRead + Unpin + Send, V: serde::de::DeserializeOwned>(
    io: &mut T,
    capture: &Capture,
) -> io::Result<V> {
    let mut prefix = [0; 4];
    io.read_exact(&mut prefix).await?;
    let n = u32::from_be_bytes(prefix) as usize;
    if n > FRAME_CAP {
        return Err(invalid("frame cap exceeded"));
    }
    let mut b = vec![0; n];
    io.read_exact(&mut b).await?;
    capture.frame(&b);
    ciborium::from_reader(&b[..]).map_err(invalid)
}
async fn write<T: AsyncWrite + Unpin + Send, V: Serialize>(
    io: &mut T,
    value: &V,
    capture: &Capture,
) -> io::Result<()> {
    let mut b = vec![];
    ciborium::into_writer(value, &mut b).map_err(invalid)?;
    if b.len() > FRAME_CAP {
        return Err(invalid("frame cap exceeded"));
    }
    capture.frame(&b);
    io.write_all(&(b.len() as u32).to_be_bytes()).await?;
    io.write_all(&b).await?;
    io.close().await
}
impl request_response::Codec for Codec {
    type Protocol = StreamProtocol;
    type Request = Request;
    type Response = Response;
    async fn read_request<T>(&mut self, _: &StreamProtocol, io: &mut T) -> io::Result<Request>
    where
        T: AsyncRead + Unpin + Send,
    {
        let r = read(io, &self.capture).await?;
        self.capture.request(&r);
        Ok(r)
    }
    async fn read_response<T>(&mut self, _: &StreamProtocol, io: &mut T) -> io::Result<Response>
    where
        T: AsyncRead + Unpin + Send,
    {
        let r = read(io, &self.capture).await?;
        self.capture.response(&r);
        Ok(r)
    }
    async fn write_request<T>(
        &mut self,
        _: &StreamProtocol,
        io: &mut T,
        r: Request,
    ) -> io::Result<()>
    where
        T: AsyncWrite + Unpin + Send,
    {
        self.capture.request(&r);
        write(io, &r, &self.capture).await
    }
    async fn write_response<T>(
        &mut self,
        _: &StreamProtocol,
        io: &mut T,
        r: Response,
    ) -> io::Result<()>
    where
        T: AsyncWrite + Unpin + Send,
    {
        self.capture.response(&r);
        write(io, &r, &self.capture).await
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[tokio::test]
    async fn oversize_frame_checked() {
        let mut b = futures::io::Cursor::new((65537_u32).to_be_bytes().to_vec());
        assert!(read::<_, Request>(&mut b, &Capture::default())
            .await
            .is_err());
    }
    #[tokio::test]
    async fn garbage_frame_checked() {
        for b in [vec![0, 0, 0, 1, 0xff], vec![0, 0, 0, 2, 0xff]] {
            let mut io = futures::io::Cursor::new(b);
            assert!(read::<_, Request>(&mut io, &Capture::default())
                .await
                .is_err());
        }
    }
    #[test]
    fn capture_scans_binary_canaries_and_refreshes_after_append() {
        let capture = Capture::default();
        let first = vec![0, 1, 2, 3, 4, 5, 6, 7, 8];
        capture.forbidden.write().unwrap().push(first.clone());
        capture.frame(&[99; 100]);
        capture.frame(&first);
        let second = vec![9, 8, 7, 6, 5, 4, 3, 2, 1];
        capture.forbidden.write().unwrap().push(second.clone());
        capture.frame(&second);
        let stats = capture.stats.lock().unwrap();
        assert_eq!(stats.frames, 3);
        assert_eq!(stats.leaks, 2);
    }
}
