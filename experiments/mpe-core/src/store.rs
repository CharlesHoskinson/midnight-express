use crate::wire::{Eid, Envelope, Error, NetworkId, LIFETIME};
use ed25519_dalek::{Signature, Signer, SigningKey, VerifyingKey};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, HashMap, HashSet};
pub type OperatorId = [u8; 32];
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct Cursor {
    pub expiry: u32,
    pub eid: Eid,
}
impl Cursor {
    pub fn overlap(self) -> Self {
        Self {
            expiry: self.expiry.saturating_sub(60),
            eid: [0; 32],
        }
    }
}
#[derive(Clone, Copy, Debug, Serialize, Deserialize)]
pub struct TimeWindow {
    pub from: u64,
    pub until: u64,
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Page {
    pub envelopes: Vec<Vec<u8>>,
    pub next: Option<Cursor>,
    pub head: bool,
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct InvPage {
    pub eids: Vec<Eid>,
    pub next: Option<Eid>,
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Receipt {
    pub operator: OperatorId,
    pub eid: Eid,
    pub shard: u8,
    pub deadline: u32,
    pub signature: Vec<u8>,
}
fn receipt_message(network: &NetworkId, eid: &Eid, shard: u8, deadline: u32) -> Vec<u8> {
    [
        b"mpe/v1/receipt".as_slice(),
        network,
        eid,
        &[shard],
        &deadline.to_be_bytes(),
    ]
    .concat()
}
impl Receipt {
    pub fn verify(&self, network: &NetworkId, roster: &HashMap<OperatorId, [u8; 32]>) -> bool {
        let Some(key) = roster.get(&self.operator) else {
            return false;
        };
        let Ok(vk) = VerifyingKey::from_bytes(key) else {
            return false;
        };
        let Ok(sig) = Signature::from_slice(&self.signature) else {
            return false;
        };
        vk.verify_strict(
            &receipt_message(network, &self.eid, self.shard, self.deadline),
            &sig,
        )
        .is_ok()
    }
}
pub fn stored(
    network: &NetworkId,
    roster: &HashMap<OperatorId, [u8; 32]>,
    eid: &Eid,
    shard: u8,
    deadline: u32,
    receipts: &[Receipt],
) -> bool {
    receipts
        .iter()
        .filter(|r| {
            r.eid == *eid && r.shard == shard && r.deadline == deadline && r.verify(network, roster)
        })
        .map(|r| r.operator)
        .collect::<HashSet<_>>()
        .len()
        >= 3
}
pub trait Store: Send {
    fn admit(&mut self, env: &[u8], eid: &Eid, now: u64) -> Result<u32, Error>;
    fn page(&self, shard: u8, from: Cursor, until: u64, limit: usize) -> Result<Page, Error>;
    fn inventory(
        &self,
        shard: u8,
        window: TimeWindow,
        after: Option<Eid>,
        limit: usize,
    ) -> Result<InvPage, Error>;
    fn get(&self, eid: &Eid) -> Result<Option<Vec<u8>>, Error>;
    fn prune(&mut self, now: u64) -> usize;
    fn bytes(&self, shard: u8) -> u64;
}
pub struct MemStore {
    entries: BTreeMap<(u8, Cursor), Vec<u8>>,
    by_id: HashMap<Eid, (u8, Cursor)>,
    bytes: [u64; 8],
    pub cap: u64,
    pub network: NetworkId,
    pub operator: OperatorId,
    signer: SigningKey,
    pub max_bytes: u64,
}
impl MemStore {
    pub fn new(network: NetworkId, operator: OperatorId, signer: SigningKey, cap: u64) -> Self {
        Self {
            entries: BTreeMap::new(),
            by_id: HashMap::new(),
            bytes: [0; 8],
            cap,
            network,
            operator,
            signer,
            max_bytes: 0,
        }
    }
    pub fn receipts(&self, shard: u8, window: TimeWindow) -> Vec<Receipt> {
        self.receipts_page(shard, window, None, 64).0
    }
    pub fn receipts_page(
        &self,
        shard: u8,
        window: TimeWindow,
        after: Option<Eid>,
        limit: usize,
    ) -> (Vec<Receipt>, Option<Eid>) {
        let limit = limit.clamp(1, 64);
        let mut cursors: Vec<_> = self
            .entries
            .keys()
            .filter(|(s, c)| {
                *s == shard
                    && after.is_none_or(|id| c.eid > id)
                    && window.from <= u64::from(c.expiry).saturating_sub(LIFETIME)
                    && u64::from(c.expiry).saturating_sub(LIFETIME) <= window.until
            })
            .map(|(_, c)| *c)
            .collect();
        cursors.sort_unstable_by_key(|c| c.eid);
        let more = cursors.len() > limit;
        cursors.truncate(limit);
        let next = if more {
            cursors.last().map(|c| c.eid)
        } else {
            None
        };
        let receipts = cursors
            .into_iter()
            .map(|c| Receipt {
                operator: self.operator,
                eid: c.eid,
                shard,
                deadline: c.expiry,
                signature: self
                    .signer
                    .sign(&receipt_message(&self.network, &c.eid, shard, c.expiry))
                    .to_bytes()
                    .to_vec(),
            })
            .collect();
        (receipts, next)
    }
}
impl Store for MemStore {
    fn admit(&mut self, env: &[u8], eid: &Eid, now: u64) -> Result<u32, Error> {
        let e = Envelope::parse(env)?;
        let s = e.header.shard as usize;
        if s >= 8 || u64::from(e.header.expiry) > now.saturating_add(LIFETIME + 60) {
            return Err(Error::Malformed);
        }
        if self.by_id.contains_key(eid) {
            return Ok(e.header.expiry);
        }
        let bytes = env.len() as u64 + 72;
        if self.bytes[s] + bytes > self.cap {
            return Err(Error::StorageExhausted);
        }
        let cursor = Cursor {
            expiry: e.header.expiry,
            eid: *eid,
        };
        self.entries.insert((s as u8, cursor), env.to_vec());
        self.by_id.insert(*eid, (s as u8, cursor));
        self.bytes[s] += bytes;
        self.max_bytes = self.max_bytes.max(self.bytes.iter().sum());
        Ok(e.header.expiry)
    }
    fn page(&self, shard: u8, from: Cursor, until: u64, limit: usize) -> Result<Page, Error> {
        if shard >= 8 {
            return Err(Error::Refused);
        }
        let limit = limit.clamp(1, 64);
        let mut envelopes = vec![];
        let mut size = 0;
        let mut next = None;
        for ((s, c), b) in self.entries.range((shard, from)..) {
            if *s != shard {
                break;
            }
            if u64::from(c.expiry).saturating_sub(LIFETIME) > until {
                break;
            }
            if envelopes.len() >= limit || size + b.len() * 2 > 58000 {
                next = Some(*c);
                break;
            }
            size += b.len() * 2;
            envelopes.push(b.clone());
        }
        Ok(Page {
            envelopes,
            next,
            head: next.is_none(),
        })
    }
    fn inventory(
        &self,
        shard: u8,
        window: TimeWindow,
        after: Option<Eid>,
        limit: usize,
    ) -> Result<InvPage, Error> {
        if shard >= 8 {
            return Err(Error::Refused);
        }
        let mut ids: Vec<_> = self
            .entries
            .iter()
            .filter(|((s, c), _)| {
                *s == shard
                    && window.from <= u64::from(c.expiry).saturating_sub(LIFETIME)
                    && u64::from(c.expiry).saturating_sub(LIFETIME) <= window.until
                    && after.is_none_or(|id| c.eid > id)
            })
            .map(|((_, c), _)| c.eid)
            .collect();
        ids.sort_unstable();
        let limit = limit.clamp(1, 64);
        let more = ids.len() > limit;
        ids.truncate(limit);
        let next = if more { ids.last().copied() } else { None };
        Ok(InvPage { eids: ids, next })
    }
    fn get(&self, eid: &Eid) -> Result<Option<Vec<u8>>, Error> {
        Ok(self
            .by_id
            .get(eid)
            .and_then(|key| self.entries.get(key))
            .cloned())
    }
    fn prune(&mut self, now: u64) -> usize {
        let keys: Vec<_> = self
            .entries
            .keys()
            .filter(|(_, c)| u64::from(c.expiry) < now)
            .copied()
            .collect();
        let n = keys.len();
        for key in keys {
            if let Some(b) = self.entries.remove(&key) {
                self.bytes[key.0 as usize] =
                    self.bytes[key.0 as usize].saturating_sub(b.len() as u64 + 72);
                self.by_id.remove(&key.1.eid);
            }
        }
        n
    }
    fn bytes(&self, shard: u8) -> u64 {
        self.bytes.get(shard as usize).copied().unwrap_or(0)
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use crate::wire::{Header, MOCK_NETWORK};
    fn fixture(count: u16, reverse: bool) -> MemStore {
        let mut s = MemStore::new(
            MOCK_NETWORK,
            [1; 32],
            SigningKey::from_bytes(&[1; 32]),
            10000000,
        );
        let indices: Vec<_> = if reverse {
            (0..count).rev().collect()
        } else {
            (0..count).collect()
        };
        for n in indices {
            let mut id = [0; 32];
            id[..2].copy_from_slice(&n.to_be_bytes());
            let mut b = Header {
                version: 1,
                class: 0,
                shard: 0,
                expiry: 172900,
            }
            .encode()
            .to_vec();
            b.resize(776, 0);
            b[700..702].copy_from_slice(&n.to_be_bytes());
            s.admit(&b, &id, 100).unwrap();
        }
        s
    }
    #[test]
    fn retained_body_retrievable() {
        let s = fixture(1, false);
        assert_eq!(s.get(&[0; 32]).unwrap().unwrap().len(), 776);
    }
    #[test]
    fn backfill_pages() {
        let s = fixture(200, false);
        let mut cursor = Cursor::default();
        let mut ids = HashSet::new();
        loop {
            let p = s.page(0, cursor, 100, 64).unwrap();
            assert!(p.envelopes.len() <= 64);
            for wire in &p.envelopes {
                assert_eq!(Envelope::parse(wire).unwrap().header.expiry, 172900);
                let n = u16::from_be_bytes(wire[700..702].try_into().unwrap());
                assert!(n < 200);
                assert!(ids.insert(n), "duplicate page entry");
                let mut id = [0; 32];
                id[..2].copy_from_slice(&n.to_be_bytes());
                assert_eq!(s.get(&id).unwrap().as_ref(), Some(wire));
            }
            if let Some(c) = p.next {
                cursor = c;
            } else {
                break;
            }
        }
        assert_eq!(ids.len(), 200);
    }
    #[test]
    fn inventory_pages() {
        let s = fixture(200, false);
        let mut after = None;
        let mut ids = HashSet::new();
        loop {
            let p = s
                .inventory(
                    0,
                    TimeWindow {
                        from: 0,
                        until: 100,
                    },
                    after,
                    64,
                )
                .unwrap();
            ids.extend(p.eids);
            if let Some(c) = p.next {
                after = Some(c);
            } else {
                break;
            }
        }
        assert_eq!(ids.len(), 200);
    }
    #[test]
    fn switch_store_mid_backfill() {
        let a = fixture(200, false);
        let b = fixture(200, true);
        let first = a.page(0, Cursor::default(), 100, 64).unwrap();
        let cursor = first.next.unwrap();
        let rest = b.page(0, cursor, 100, 64).unwrap();
        assert_eq!(rest.next, a.page(0, cursor, 100, 64).unwrap().next);
        assert_eq!(
            rest.envelopes,
            a.page(0, cursor, 100, 64).unwrap().envelopes
        );
    }
    #[test]
    fn receipts_by_window_three_operators() {
        let mut roster = HashMap::new();
        let mut receipts = vec![];
        for n in 1..=3 {
            let signer = SigningKey::from_bytes(&[n; 32]);
            roster.insert([n; 32], signer.verifying_key().to_bytes());
            let mut s = fixture(1, false);
            s.operator = [n; 32];
            s.signer = signer;
            receipts.extend(s.receipts(
                0,
                TimeWindow {
                    from: 0,
                    until: 100,
                },
            ));
        }
        assert!(stored(
            &MOCK_NETWORK,
            &roster,
            &[0; 32],
            0,
            172900,
            &receipts
        ));
        let original = receipts.clone();
        receipts[2] = receipts[0].clone();
        assert!(receipts.iter().all(|r| r.verify(&MOCK_NETWORK, &roster)));
        assert!(!stored(
            &MOCK_NETWORK,
            &roster,
            &[0; 32],
            0,
            172901,
            &original
        ));
        assert!(!stored(
            &MOCK_NETWORK,
            &roster,
            &[0; 32],
            0,
            172900,
            &receipts
        ));
        assert!(!stored(
            &MOCK_NETWORK,
            &roster,
            &[9; 32],
            0,
            172900,
            &receipts
        ));
    }
    #[test]
    fn storage_cap_and_pruning() {
        let mut s = fixture(1, false);
        assert_eq!(s.bytes(0), 848);
        s.cap = 848;
        assert_eq!(
            s.admit(&s.get(&[0; 32]).unwrap().unwrap(), &[1; 32], 100),
            Err(Error::StorageExhausted)
        );
        assert_eq!(s.prune(172901), 1);
        assert_eq!(s.bytes(0), 0);
    }
}
