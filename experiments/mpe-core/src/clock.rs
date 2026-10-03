use std::{
    sync::atomic::{AtomicU64, Ordering},
    time::Instant,
};
pub trait Clock: Send + Sync {
    fn now(&self) -> u64;
}
pub struct SimClock {
    base: u64,
    started: Instant,
    offset: AtomicU64,
}
impl SimClock {
    pub fn new(base: u64) -> Self {
        Self {
            base,
            started: Instant::now(),
            offset: AtomicU64::new(0),
        }
    }
    pub fn advance(&self, seconds: u64) {
        self.offset.fetch_add(seconds, Ordering::Relaxed);
    }
}
impl Clock for SimClock {
    fn now(&self) -> u64 {
        self.base + self.started.elapsed().as_secs() + self.offset.load(Ordering::Relaxed)
    }
}

/// The protocol epoch is a UTC minute, independent of node startup.
pub fn epoch(now: u64) -> u64 {
    now / 60
}
