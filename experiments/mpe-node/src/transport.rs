use futures::{AsyncRead, AsyncWrite};
use std::{
    io,
    pin::Pin,
    sync::{
        atomic::{AtomicU64, Ordering},
        Arc,
    },
    task::{Context, Poll},
};
#[derive(Default)]
pub struct Counters {
    pub incoming: AtomicU64,
    pub outgoing: AtomicU64,
    pub egress: Arc<[AtomicU64; 4]>,
}
impl Counters {
    pub fn egress_snapshot(&self) -> [u64; 4] {
        std::array::from_fn(|i| self.egress[i].load(Ordering::Relaxed))
    }
    pub fn snapshot(&self) -> (u64, u64) {
        (
            self.incoming.load(Ordering::Relaxed),
            self.outgoing.load(Ordering::Relaxed),
        )
    }
}
pub struct CountIo<T> {
    pub inner: T,
    pub counters: Arc<Counters>,
}
impl<T: AsyncRead + Unpin> AsyncRead for CountIo<T> {
    fn poll_read(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>,
        buf: &mut [u8],
    ) -> Poll<io::Result<usize>> {
        let this = self.get_mut();
        match Pin::new(&mut this.inner).poll_read(cx, buf) {
            Poll::Ready(Ok(n)) => {
                this.counters
                    .incoming
                    .fetch_add(n as u64, Ordering::Relaxed);
                Poll::Ready(Ok(n))
            }
            other => other,
        }
    }
}
impl<T: AsyncWrite + Unpin> AsyncWrite for CountIo<T> {
    fn poll_write(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>,
        buf: &[u8],
    ) -> Poll<io::Result<usize>> {
        let this = self.get_mut();
        match Pin::new(&mut this.inner).poll_write(cx, buf) {
            Poll::Ready(Ok(n)) => {
                this.counters
                    .outgoing
                    .fetch_add(n as u64, Ordering::Relaxed);
                Poll::Ready(Ok(n))
            }
            other => other,
        }
    }
    fn poll_flush(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<io::Result<()>> {
        Pin::new(&mut self.get_mut().inner).poll_flush(cx)
    }
    fn poll_close(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<io::Result<()>> {
        Pin::new(&mut self.get_mut().inner).poll_close(cx)
    }
}
