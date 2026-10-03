use crate::subscriber::{Delivery, Subscriber};
use mpe_core::{
    indexer::Indexer,
    ledger::{
        Action, ContractAddress, ContractEvent, Intent, LedgerAdapter, LedgerError, Misc, MockTx,
        TxTicket,
    },
    outcome::ClientError,
    wire::{Envelope, BODY_LENGTHS},
};
use std::collections::{BTreeMap, HashSet};
pub const BUS_CONTRACT: ContractAddress = [0x42; 32];
pub fn name() -> [u8; 32] {
    let mut n = [0; 32];
    n[..10].copy_from_slice(b"mpe/env/v1");
    n
}
#[derive(Default)]
pub struct Fallback {
    pub opted_in: bool,
    pub cursor: u64,
    seen_rows: HashSet<u64>,
    pending: BTreeMap<(u64, u32), Vec<ContractEvent>>,
    pub malformed_groups: u64,
}
impl Fallback {
    pub fn select_profile(&mut self) {
        self.opted_in = true;
    }
    pub fn transaction(&self, wire: &[u8], now: u64) -> Result<MockTx, ClientError> {
        if !self.opted_in {
            return Err(ClientError::NotReady);
        }
        let env = Envelope::parse(wire)?;
        if env.header.class > 2 {
            return Err(ClientError::TooLarge);
        }
        let events = env
            .body
            .as_chunks::<256>()
            .0
            .iter()
            .map(|part| Misc {
                name: name(),
                payload: part.to_vec(),
            })
            .collect();
        Ok(MockTx {
            contract: BUS_CONTRACT,
            intents: vec![Intent {
                id: 0,
                guaranteed: true,
                succeeds: true,
                events,
            }],
            action: Action::Events,
            ttl: now + 600,
            fee: 1,
        })
    }
    pub fn publish(
        &self,
        ledger: &dyn LedgerAdapter,
        wire: &[u8],
        now: u64,
    ) -> Result<TxTicket, ClientError> {
        let tx = self.transaction(wire, now)?;
        ledger.submit(tx).map_err(map_error)
    }
    pub fn poll(
        &mut self,
        indexer: &dyn Indexer,
        subscriber: &mut Subscriber,
        now: u64,
    ) -> Result<Vec<Delivery>, ClientError> {
        if !self.opted_in {
            return Err(ClientError::NotReady);
        }
        let mut delivered = vec![];
        // Fetch to the finalized head before closing a group, so a 16-part body cannot be cut by pagination.
        loop {
            let rows = indexer
                .contract_events(&BUS_CONTRACT, self.cursor, 500)
                .map_err(map_error)?;
            let full = rows.len() == 500;
            let max = rows.last().map(|e| e.id);
            for row in rows {
                if self.seen_rows.insert(row.id) && row.misc.name == name() {
                    self.pending
                        .entry((row.tx, row.intent))
                        .or_default()
                        .push(row);
                }
            }
            if let Some(max) = max {
                self.cursor = max.saturating_add(1);
            }
            if !full {
                break;
            }
        }
        for (_, mut rows) in std::mem::take(&mut self.pending) {
            rows.sort_unstable_by_key(|e| e.ordinal);
            let n = rows.len();
            let class = match n {
                1 => 0,
                4 => 1,
                16 => 2,
                _ => {
                    self.malformed_groups += 1;
                    continue;
                }
            };
            if rows.iter().any(|r| r.misc.payload.len() != 256) {
                self.malformed_groups += 1;
                continue;
            }
            let body: Vec<_> = rows.into_iter().flat_map(|r| r.misc.payload).collect();
            if let Some(d) = subscriber.process_ledger_body(class, &body, now) {
                delivered.push(d);
            }
        }
        Ok(delivered)
    }
    pub fn reassemble(rows: &[ContractEvent]) -> Result<(u8, Vec<u8>), ClientError> {
        let class = match rows.len() {
            1 => 0,
            4 => 1,
            16 => 2,
            _ => return Err(ClientError::CorruptRecord),
        };
        let first = rows.first().ok_or(ClientError::CorruptRecord)?;
        if rows.iter().any(|r| {
            r.tx != first.tx
                || r.intent != first.intent
                || r.misc.name != name()
                || r.misc.payload.len() != 256
        }) {
            return Err(ClientError::CorruptRecord);
        }
        let mut ordered = rows.to_vec();
        ordered.sort_unstable_by_key(|r| r.ordinal);
        let body: Vec<_> = ordered.into_iter().flat_map(|r| r.misc.payload).collect();
        if body.len() != BODY_LENGTHS[class as usize] {
            return Err(ClientError::CorruptRecord);
        }
        Ok((class, body))
    }
}
pub fn map_error(error: LedgerError) -> ClientError {
    match error {
        LedgerError::Paused => ClientError::LedgerPaused,
        LedgerError::Unavailable => ClientError::LedgerUnavailable,
        LedgerError::Limit => ClientError::ResourceExhausted,
        LedgerError::Invalid => ClientError::CorruptRecord,
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use crate::subscriber::Subscription;
    use ed25519_dalek::SigningKey;
    use mpe_core::{
        indexer::MockIndexer,
        keys::StreamKeys,
        ledger::MockLedger,
        seal::{seal, EventIn},
        wire::MOCK_NETWORK,
    };
    use rand::SeedableRng;
    use rand_chacha::ChaCha20Rng;
    use std::sync::Arc;
    fn fixture(class: u8) -> (Vec<u8>, Subscriber) {
        let keys = StreamKeys::new(MOCK_NETWORK, [7; 32], 1).unwrap();
        let signer = SigningKey::from_bytes(&[8; 32]);
        let mut rng = ChaCha20Rng::seed_from_u64(42);
        let ev = EventIn {
            payload: vec![1],
            lei: [9; 16],
            seq: 1,
            schema: [1; 8],
            schema_version: 1,
            key_index: 0,
        };
        let b = seal(&keys, &signer, &ev, Some(class), 100, &mut rng).unwrap();
        let mut sub = Subscriber::default();
        sub.install(Subscription {
            keys,
            publishers: vec![signer.verifying_key().to_bytes()],
        })
        .unwrap();
        (b, sub)
    }
    #[test]
    fn no_silent_fallback_and_class3_refused() {
        let f = Fallback::default();
        let (b, _) = fixture(0);
        assert!(matches!(f.transaction(&b, 100), Err(ClientError::NotReady)));
        let mut f = Fallback::default();
        f.select_profile();
        let (b, _) = fixture(3);
        assert!(matches!(f.transaction(&b, 100), Err(ClientError::TooLarge)));
    }
    #[test]
    fn ledger_copy_opens_and_part_vectors() {
        for c in 0..3 {
            let (b, mut sub) = fixture(c);
            let ledger = Arc::new(MockLedger::new(MOCK_NETWORK, 100, vec![], vec![], 1));
            let indexer = MockIndexer::new(ledger.clone());
            let mut f = Fallback::default();
            f.select_profile();
            let tx = f.transaction(&b, 100).unwrap();
            assert_eq!(tx.intents[0].events.len(), 4_usize.pow(c as u32));
            assert!(tx.intents[0].events.iter().all(|m| m.name == name()));
            assert_eq!(
                tx.intents[0]
                    .events
                    .iter()
                    .flat_map(|m| m.payload.clone())
                    .collect::<Vec<_>>(),
                b[520..]
            );
            f.publish(&*ledger, &b, 100).unwrap();
            ledger.advance_to(118).unwrap();
            assert!(f.poll(&indexer, &mut sub, 118).unwrap().is_empty());
            ledger.advance_to(124).unwrap();
            let d = f.poll(&indexer, &mut sub, 124).unwrap();
            assert_eq!(d.len(), 1);
            assert_eq!(d[0].event.event.payload, vec![1]);
            assert!(indexer
                .calls
                .lock()
                .unwrap()
                .iter()
                .all(|(contract, _, _)| *contract == BUS_CONTRACT));
        }
    }
    #[test]
    fn interleaved_intents_and_bad_counts() {
        let (b, mut sub) = fixture(1);
        let ledger = Arc::new(MockLedger::new(MOCK_NETWORK, 100, vec![], vec![], 1));
        let indexer = MockIndexer::new(ledger.clone());
        let mut f = Fallback::default();
        f.select_profile();
        let mut tx = f.transaction(&b, 100).unwrap();
        let mut second = tx.intents[0].clone();
        second.id = 1;
        tx.intents.push(second);
        ledger.submit(tx).unwrap();
        ledger.advance_to(124).unwrap();
        f.poll(&indexer, &mut sub, 124).unwrap();
        assert_eq!(sub.deliveries.len(), 1);
        assert_eq!(f.malformed_groups, 0);
        for n in [2, 3, 5] {
            let rows: Vec<_> = (0..n)
                .map(|i| ContractEvent {
                    id: i,
                    contract: BUS_CONTRACT,
                    tx: 1,
                    intent: 0,
                    ordinal: i as u32,
                    misc: Misc {
                        name: name(),
                        payload: vec![0; 256],
                    },
                    height: 1,
                })
                .collect();
            assert!(Fallback::reassemble(&rows).is_err());
        }
    }
}
