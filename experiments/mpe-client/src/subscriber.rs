use mpe_core::{
    keys::{matches, StreamKeys},
    outcome::ClientError,
    seal::{open, open_body, OpenedEvent},
    store::{stored, OperatorId, Receipt},
    wire::{eid, Eid, Envelope, Error, Header, HEADER_LEN},
};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeSet, HashMap, VecDeque};
#[derive(Clone)]
pub struct Subscription {
    pub keys: StreamKeys,
    pub publishers: Vec<[u8; 32]>,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Finality {
    Gossip,
    Final,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Carrier {
    Overlay,
    Gateway,
    Ledger,
}
#[derive(Clone, Debug)]
pub struct Delivery {
    pub eid: Eid,
    pub event: OpenedEvent,
    pub finality: Finality,
    pub carrier: Carrier,
    pub stored: bool,
    pub received_at: u64,
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Gap {
    pub publisher: [u8; 32],
    pub stream: [u8; 32],
    pub from: u64,
    pub until: u64,
}
#[derive(Default)]
struct Sequence {
    pub high: Option<u64>,
    pub missing: BTreeSet<u64>,
    pub since: Option<u64>,
    last: u64,
}
#[derive(Default)]
pub struct Subscriber {
    pub subscriptions: Vec<Subscription>,
    seen: HashMap<Eid, u64>,
    logical: HashMap<([u8; 32], [u8; 16]), u64>,
    pub received: BTreeSet<Eid>,
    pub deliveries: Vec<Delivery>,
    pub failures: HashMap<String, u64>,
    #[cfg(any(test, feature = "diagnostics"))]
    pub rejected_eids: HashMap<Eid, Error>,
    observations: VecDeque<(Eid, u64)>,
    last_prune: u64,
    sequences: HashMap<([u8; 32], [u8; 32]), Sequence>,
    pub network_bytes: u64,
}
impl Subscriber {
    /// Ten-minute observations and plaintext; expiry-based dedup remains separately bounded.
    pub fn prune(&mut self, now: u64) {
        if self.last_prune == now {
            return;
        }
        self.last_prune = now;
        while self
            .observations
            .front()
            .is_some_and(|(_, at)| now.saturating_sub(*at) >= 600)
        {
            if let Some((id, _)) = self.observations.pop_front() {
                self.received.remove(&id);
            }
        }
        self.deliveries
            .retain(|d| now.saturating_sub(d.received_at) < 600);
        self.sequences
            .retain(|_, s| now.saturating_sub(s.last) < 600);
        self.seen.retain(|_, until| *until >= now);
        self.logical.retain(|_, until| *until >= now);
        #[cfg(any(test, feature = "diagnostics"))]
        self.rejected_eids
            .retain(|id, _| self.received.contains(id));
    }
    fn observe(&mut self, id: Eid, now: u64) {
        if self.received.insert(id) {
            self.observations.push_back((id, now));
        }
        while self.observations.len() > 100_000 {
            if let Some((id, _)) = self.observations.pop_front() {
                self.received.remove(&id);
            }
        }
    }
    pub fn install(&mut self, subscription: Subscription) -> Result<(), ClientError> {
        let rec = subscription.keys.recognition();
        if self
            .subscriptions
            .iter()
            .any(|s| s.keys.recognition() == rec)
        {
            return Ok(());
        }
        if self.subscriptions.len() >= 256 {
            return Err(ClientError::KeyLimit);
        }
        self.subscriptions.push(subscription);
        Ok(())
    }
    fn deliver(
        &mut self,
        id: Eid,
        event: OpenedEvent,
        carrier: Carrier,
        now: u64,
    ) -> Option<Delivery> {
        self.seen.retain(|_, until| *until >= now);
        self.logical.retain(|_, until| *until >= now);
        if self.seen.contains_key(&id)
            || self
                .logical
                .contains_key(&(event.publisher, event.event.lei))
        {
            return None;
        }
        if self.seen.len() >= 2_000_000
            || self.logical.len() >= 2_000_000
            || self.deliveries.len() >= 100_000
            || self.sequences.len() >= 65_536
        {
            *self.failures.entry("Busy".into()).or_default() += 1;
            return None;
        }
        self.seen.insert(id, u64::from(event.expiry) + 3600);
        self.logical.insert(
            (event.publisher, event.event.lei),
            u64::from(event.expiry) + 3600,
        );
        let state = self
            .sequences
            .entry((event.stream, event.publisher))
            .or_default();
        state.last = now;
        let seq = event.event.seq;
        if let Some(high) = state.high {
            if seq > high.saturating_add(1) {
                let end = seq.min(high.saturating_add(10001));
                state.missing.extend(high.saturating_add(1)..end);
                state.since.get_or_insert(now);
            }
            state.missing.remove(&seq);
            state.high = Some(high.max(seq));
        } else {
            state.high = Some(seq);
        }
        let delivery = Delivery {
            eid: id,
            event,
            finality: if carrier == Carrier::Ledger {
                Finality::Final
            } else {
                Finality::Gossip
            },
            carrier,
            stored: false,
            received_at: now,
        };
        self.deliveries.push(delivery.clone());
        Some(delivery)
    }
    pub fn process(&mut self, wire: &[u8], carrier: Carrier, now: u64) -> Option<Delivery> {
        self.prune(now);
        self.network_bytes += wire.len() as u64;
        let env = match Envelope::parse(wire) {
            Ok(e) => e,
            Err(e) => {
                *self.failures.entry(format!("{e:?}")).or_default() += 1;
                return None;
            }
        };
        let network = self
            .subscriptions
            .first()
            .map(|s| s.keys.network)
            .unwrap_or(mpe_core::wire::MOCK_NETWORK);
        let id = env.eid(&network);
        self.observe(id, now);
        // Scan every installed key. Recognition changes no request, acknowledgement or timing schedule.
        let candidates: Vec<_> = self
            .subscriptions
            .iter()
            .enumerate()
            .filter_map(|(i, s)| {
                matches(&s.keys.recognition(), &s.keys.network, env.body).then_some(i)
            })
            .collect();
        for i in candidates {
            let sub = &self.subscriptions[i];
            match open(&sub.keys, wire, &sub.publishers, now) {
                Ok(event) => return self.deliver(id, event, carrier, now),
                Err(e) => {
                    #[cfg(any(test, feature = "diagnostics"))]
                    self.rejected_eids.insert(id, e);
                    *self.failures.entry(format!("{e:?}")).or_default() += 1;
                }
            }
        }
        None
    }
    pub fn process_ledger_body(&mut self, class: u8, body: &[u8], now: u64) -> Option<Delivery> {
        self.prune(now);
        self.network_bytes += body.len() as u64;
        let candidates: Vec<_> = self
            .subscriptions
            .iter()
            .enumerate()
            .filter_map(|(i, s)| matches(&s.keys.recognition(), &s.keys.network, body).then_some(i))
            .collect();
        for i in candidates {
            let sub = &self.subscriptions[i];
            match open_body(&sub.keys, class, body, &sub.publishers, now, None) {
                Ok(event) => {
                    let h = Header {
                        version: 1,
                        class,
                        shard: sub.keys.shard(),
                        expiry: event.expiry,
                    };
                    let mut wire = h.encode().to_vec();
                    wire.resize(HEADER_LEN, 0);
                    wire.extend_from_slice(body);
                    let Ok(id) = eid(&sub.keys.network, &wire) else {
                        continue;
                    };
                    self.observe(id, now);
                    return self.deliver(id, event, Carrier::Ledger, now);
                }
                Err(e) => {
                    *self.failures.entry(format!("{e:?}")).or_default() += 1;
                }
            }
        }
        None
    }
    pub fn gaps(&mut self, now: u64) -> Vec<Gap> {
        self.prune(now);
        let mut gaps = vec![];
        for ((stream, publisher), state) in &mut self.sequences {
            if state
                .since
                .is_some_and(|since| now.saturating_sub(since) >= 120)
            {
                let mut iter = state.missing.iter().copied().peekable();
                while let Some(from) = iter.next() {
                    let mut until = from;
                    while iter.peek().is_some_and(|n| *n == until + 1) {
                        until = iter.next().unwrap_or(until);
                    }
                    gaps.push(Gap {
                        publisher: *publisher,
                        stream: *stream,
                        from,
                        until,
                    });
                }
                state.since = None;
            }
        }
        gaps
    }
    pub fn mark_stored(
        &mut self,
        network: &[u8; 32],
        roster: &HashMap<OperatorId, [u8; 32]>,
        receipts: &[Receipt],
    ) {
        for d in &mut self.deliveries {
            let shard = self
                .subscriptions
                .iter()
                .find(|s| s.keys.stream_id() == d.event.stream)
                .map(|s| s.keys.shard())
                .unwrap_or(0);
            d.stored = stored(network, roster, &d.eid, shard, d.event.expiry, receipts);
        }
    }
    pub fn last_error(&self, error: Error) -> ClientError {
        error.into()
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use ed25519_dalek::SigningKey;
    use mpe_core::{
        seal::{seal, EventIn},
        wire::MOCK_NETWORK,
    };
    use rand::SeedableRng;
    use rand_chacha::ChaCha20Rng;
    fn fixture() -> (Subscriber, StreamKeys, SigningKey, EventIn, ChaCha20Rng) {
        let keys = StreamKeys::new(MOCK_NETWORK, [7; 32], 1).unwrap();
        let signer = SigningKey::from_bytes(&[8; 32]);
        let mut s = Subscriber::default();
        s.install(Subscription {
            keys: keys.clone(),
            publishers: vec![signer.verifying_key().to_bytes()],
        })
        .unwrap();
        (
            s,
            keys,
            signer,
            EventIn {
                payload: b"private".to_vec(),
                lei: [9; 16],
                seq: 1,
                schema: [1; 8],
                schema_version: 1,
                key_index: 0,
            },
            ChaCha20Rng::seed_from_u64(42),
        )
    }
    #[test]
    fn key_cap() {
        let (mut s, _, _, _, _) = fixture();
        for n in 1..256 {
            let mut secret = [0; 32];
            secret[..4].copy_from_slice(&(n as u32).to_be_bytes());
            s.install(Subscription {
                keys: StreamKeys::new(MOCK_NETWORK, secret, 1).unwrap(),
                publishers: vec![],
            })
            .unwrap();
        }
        assert_eq!(
            s.install(Subscription {
                keys: StreamKeys::new(MOCK_NETWORK, [99; 32], 1).unwrap(),
                publishers: vec![]
            }),
            Err(ClientError::KeyLimit)
        );
        assert_eq!(s.subscriptions.len(), 256);
    }
    #[test]
    fn tag_match_bad_ciphertext_not_delivered() {
        let (mut s, k, sign, e, mut r) = fixture();
        let mut b = seal(&k, &sign, &e, None, 100, &mut r).unwrap();
        b[600] ^= 1;
        assert!(s.process(&b, Carrier::Overlay, 100).is_none());
        assert_eq!(s.deliveries.len(), 0);
    }
    #[test]
    fn three_paths_one_delivery() {
        let (mut s, k, sign, e, mut r) = fixture();
        let b = seal(&k, &sign, &e, None, 100, &mut r).unwrap();
        for carrier in [Carrier::Overlay, Carrier::Gateway, Carrier::Overlay] {
            s.process(&b, carrier, 100);
        }
        assert_eq!(s.deliveries.len(), 1);
    }
    #[test]
    fn same_lei_both_carriers() {
        let (mut s, k, sign, e, mut r) = fixture();
        let a = seal(&k, &sign, &e, None, 100, &mut r).unwrap();
        let b = seal(&k, &sign, &e, None, 100, &mut r).unwrap();
        assert!(s.process(&a, Carrier::Overlay, 100).is_some());
        assert!(s.process_ledger_body(0, &b[520..], 100).is_none());
        assert_eq!(s.deliveries.len(), 1);
    }
    #[test]
    fn rejects_malformed_expired_unauthorized_badsig() {
        let (mut s, k, sign, e, mut r) = fixture();
        let b = seal(&k, &sign, &e, None, 100, &mut r).unwrap();
        assert!(s.process(&b[..100], Carrier::Overlay, 100).is_none());
        assert!(s.process(&b, Carrier::Overlay, 172901).is_none());
        let other = SigningKey::from_bytes(&[99; 32]);
        let bad = seal(&k, &other, &e, None, 100, &mut r).unwrap();
        assert!(s.process(&bad, Carrier::Overlay, 100).is_none());
        assert!(s.failures.contains_key("BadSignature"));
        s.subscriptions[0].publishers.clear();
        assert!(s.process(&b, Carrier::Overlay, 100).is_none());
    }
    #[test]
    fn gap_after_120s() {
        let (mut s, k, sign, mut e, mut r) = fixture();
        e.seq = 4;
        s.process(
            &seal(&k, &sign, &e, None, 100, &mut r).unwrap(),
            Carrier::Overlay,
            100,
        );
        e.seq = 6;
        e.lei = [10; 16];
        s.process(
            &seal(&k, &sign, &e, None, 100, &mut r).unwrap(),
            Carrier::Overlay,
            100,
        );
        assert!(s.gaps(219).is_empty());
        let gap = s.gaps(220);
        assert_eq!((gap[0].from, gap[0].until), (5, 5));
    }
    #[test]
    fn carrier_attribute_and_finality() {
        for carrier in [Carrier::Overlay, Carrier::Gateway, Carrier::Ledger] {
            let (mut s, k, sign, e, mut r) = fixture();
            let b = seal(&k, &sign, &e, None, 100, &mut r).unwrap();
            let d = if carrier == Carrier::Ledger {
                s.process_ledger_body(0, &b[520..], 100)
            } else {
                s.process(&b, carrier, 100)
            }
            .unwrap();
            assert_eq!(d.carrier, carrier);
            assert_eq!(
                d.finality,
                if carrier == Carrier::Ledger {
                    Finality::Final
                } else {
                    Finality::Gossip
                }
            );
        }
    }
    #[test]
    fn plaintext_and_tag_match_diagnostics_expire_at_ten_minutes() {
        let (mut s, k, sign, e, mut rng) = fixture();
        let good = seal(&k, &sign, &e, None, 100, &mut rng).unwrap();
        assert!(s.process(&good, Carrier::Overlay, 100).is_some());
        let mut bad = good.clone();
        bad[600] ^= 1;
        s.process(&bad, Carrier::Overlay, 100);
        assert!(!s.rejected_eids.is_empty());
        s.prune(699);
        assert_eq!(s.deliveries.len(), 1);
        s.prune(700);
        assert!(s.deliveries.is_empty());
        assert!(s.received.is_empty());
        assert!(s.rejected_eids.is_empty());
        assert!(s.sequences.is_empty());
        // Expiry dedup survives removal of plaintext history.
        assert!(s.process(&good, Carrier::Gateway, 700).is_none());
    }
}
