use std::collections::{HashMap, VecDeque};
/// Bounds include the job currently running. Call complete only after verification ends.
pub struct FairQueue<T> {
    queues: HashMap<String, VecDeque<T>>,
    rotation: VecDeque<String>,
    outstanding: HashMap<String, usize>,
    total: usize,
    pub max_total: usize,
    pub max_peer: usize,
}
impl<T> Default for FairQueue<T> {
    fn default() -> Self {
        Self {
            queues: HashMap::new(),
            rotation: VecDeque::new(),
            outstanding: HashMap::new(),
            total: 0,
            max_total: 0,
            max_peer: 0,
        }
    }
}
impl<T> FairQueue<T> {
    pub fn enqueue(&mut self, peer: String, item: T) -> Result<(), T> {
        let count = self.outstanding.get(&peer).copied().unwrap_or(0);
        if self.total >= 128 || count >= 8 {
            return Err(item);
        }
        let q = self.queues.entry(peer.clone()).or_default();
        if q.is_empty() {
            self.rotation.push_back(peer.clone());
        }
        q.push_back(item);
        *self.outstanding.entry(peer).or_default() += 1;
        self.total += 1;
        self.max_total = self.max_total.max(self.total);
        self.max_peer = self.max_peer.max(count + 1);
        Ok(())
    }
    pub fn dispatch(&mut self) -> Option<(String, T)> {
        let peer = self.rotation.pop_front()?;
        let q = self.queues.get_mut(&peer)?;
        let item = q.pop_front()?;
        if !q.is_empty() {
            self.rotation.push_back(peer.clone());
        }
        Some((peer, item))
    }
    pub fn complete(&mut self, peer: &str) {
        if let Some(c) = self.outstanding.get_mut(peer) {
            if *c > 0 {
                *c -= 1;
                self.total = self.total.saturating_sub(1);
            }
        }
    }
    pub fn len(&self) -> usize {
        self.total
    }
    pub fn is_empty(&self) -> bool {
        self.total == 0
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn queue_bounds() {
        let mut q = FairQueue::default();
        for p in 0..16 {
            for i in 0..8 {
                q.enqueue(p.to_string(), i).unwrap();
            }
            assert!(q.enqueue(p.to_string(), 9).is_err());
        }
        assert_eq!(q.len(), 128);
        let (p, _) = q.dispatch().unwrap();
        assert!(q.enqueue("new".into(), 0).is_err());
        q.complete(&p);
        assert!(q.enqueue("new".into(), 0).is_ok());
        assert_eq!(q.max_peer, 8);
    }
    #[test]
    fn round_robin_dispatch() {
        let mut q = FairQueue::default();
        for p in ["a", "b", "c"] {
            for i in 0..8 {
                q.enqueue(p.to_owned(), i).unwrap();
            }
        }
        let peers: Vec<_> = (0..6).map(|_| q.dispatch().unwrap().0).collect();
        assert_eq!(peers, ["a", "b", "c", "a", "b", "c"]);
    }
}
