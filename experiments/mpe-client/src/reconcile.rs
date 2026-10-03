use crate::subscriber::{Carrier, Subscriber};
use async_trait::async_trait;
use mpe_core::{
    outcome::ClientError,
    store::{Cursor, InvPage, Page, TimeWindow},
    wire::{Eid, LIFETIME},
};
use std::collections::BTreeSet;
#[async_trait]
pub trait Retrieval: Send + Sync {
    async fn inventory(
        &self,
        source: &str,
        shard: u8,
        window: TimeWindow,
        after: Option<Eid>,
    ) -> Result<InvPage, ClientError>;
    async fn backfill(
        &self,
        source: &str,
        shard: u8,
        from: Cursor,
        until: u64,
    ) -> Result<Page, ClientError>;
}
#[derive(Clone)]
pub struct Source {
    pub peer: String,
    pub operator: [u8; 32],
}
pub struct Reconciler {
    pub feed: Source,
    pub repair: Source,
    pub last: u64,
    pub trace: Vec<String>,
}
impl Reconciler {
    pub fn new(feed: Source, repair: Source, now: u64) -> Result<Self, ClientError> {
        if feed.operator == repair.operator {
            return Err(ClientError::NotReady);
        }
        Ok(Self {
            feed,
            repair,
            last: now,
            trace: vec![],
        })
    }
    pub async fn reconcile(
        &mut self,
        subscriber: &mut Subscriber,
        transport: &dyn Retrieval,
        shard: u8,
        now: u64,
    ) -> Result<usize, ClientError> {
        if self.trace.len() > 1024 {
            self.trace.drain(..self.trace.len() - 1024);
        }
        if now.saturating_sub(self.last) < 60 {
            return Ok(0);
        }
        let window = TimeWindow {
            from: self.last.saturating_sub(60),
            until: now.saturating_sub(5),
        };
        let mut after = None;
        let mut missing_windows = BTreeSet::new();
        loop {
            self.trace.push(format!(
                "inventory:{shard}:{}:{}:{after:?}",
                window.from, window.until
            ));
            let page = transport
                .inventory(&self.repair.peer, shard, window, after)
                .await?;
            for id in page.eids {
                if !subscriber.received.contains(&id) {
                    missing_windows.extend(window.from / 60..=window.until / 60);
                }
            }
            if let Some(next) = page.next {
                after = Some(next);
            } else {
                break;
            }
        }
        let before = subscriber.received.len();
        for w in missing_windows {
            let mut cursor = Cursor {
                expiry: u32::try_from(w * 60 + LIFETIME).map_err(|_| ClientError::CorruptRecord)?,
                eid: [0; 32],
            };
            loop {
                self.trace.push(format!(
                    "backfill:{shard}:{}:{}",
                    cursor.expiry,
                    w * 60 + 59
                ));
                let page = transport
                    .backfill(&self.repair.peer, shard, cursor, w * 60 + 59)
                    .await?;
                for env in page.envelopes {
                    subscriber.process(&env, Carrier::Gateway, now);
                }
                if let Some(next) = page.next {
                    cursor = next;
                } else {
                    break;
                }
            }
        }
        self.last = now;
        Ok(subscriber.received.len() - before)
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use ed25519_dalek::SigningKey;
    use mpe_core::{
        store::{MemStore, Store},
        wire::{eid, Header, MOCK_NETWORK},
    };
    use std::sync::Mutex;
    struct Local(Mutex<MemStore>);
    #[async_trait]
    impl Retrieval for Local {
        async fn inventory(
            &self,
            _: &str,
            s: u8,
            w: TimeWindow,
            a: Option<Eid>,
        ) -> Result<InvPage, ClientError> {
            Ok(self.0.lock().unwrap().inventory(s, w, a, 64).unwrap())
        }
        async fn backfill(&self, _: &str, s: u8, c: Cursor, u: u64) -> Result<Page, ClientError> {
            Ok(self.0.lock().unwrap().page(s, c, u, 64).unwrap())
        }
    }
    #[tokio::test]
    async fn repair_independent_of_keys() {
        let mut store = MemStore::new(
            MOCK_NETWORK,
            [2; 32],
            SigningKey::from_bytes(&[2; 32]),
            1_000_000,
        );
        let mut all = vec![];
        for i in 0..100 {
            let mut b = Header {
                version: 1,
                class: 0,
                shard: 0,
                expiry: 172900,
            }
            .encode()
            .to_vec();
            b.resize(776, 0);
            b[700] = i;
            let id = eid(&MOCK_NETWORK, &b).unwrap();
            store.admit(&b, &id, 100).unwrap();
            all.push(b);
        }
        let transport = Local(Mutex::new(store));
        let mut traces = vec![];
        for key_count in [0, 32] {
            let mut subscriber = Subscriber::default();
            for n in 0..key_count {
                subscriber
                    .install(crate::subscriber::Subscription {
                        keys: mpe_core::keys::StreamKeys::new(MOCK_NETWORK, [n as u8; 32], 1)
                            .unwrap(),
                        publishers: vec![],
                    })
                    .unwrap();
            }
            for (i, b) in all.iter().enumerate() {
                if i % 20 != 0 {
                    subscriber.process(b, Carrier::Gateway, 100);
                }
            }
            let mut r = Reconciler::new(
                Source {
                    peer: "a".into(),
                    operator: [1; 32],
                },
                Source {
                    peer: "b".into(),
                    operator: [2; 32],
                },
                100,
            )
            .unwrap();
            assert_eq!(
                r.reconcile(&mut subscriber, &transport, 0, 160)
                    .await
                    .unwrap(),
                5
            );
            assert_eq!(subscriber.received.len(), 100);
            traces.push(r.trace);
        }
        assert_eq!(traces[0], traces[1]);
    }
}
