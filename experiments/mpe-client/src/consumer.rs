use crate::subscriber::Delivery;
pub trait Consumer {
    fn on_event(&mut self, event: &Delivery);
}
pub struct AgentAdapter<F: FnMut(&Delivery)>(pub F);
impl<F: FnMut(&Delivery)> Consumer for AgentAdapter<F> {
    fn on_event(&mut self, event: &Delivery) {
        (self.0)(event);
    }
}
#[derive(Default)]
pub struct WalletAdapter {
    pub events: Vec<Delivery>,
}
impl Consumer for WalletAdapter {
    fn on_event(&mut self, event: &Delivery) {
        self.events.push(event.clone());
    }
}
use mpe_core::{
    anchor::{AnchorPayload, InclusionProof},
    keys::StreamKeys,
    ledger::{Action, LedgerAdapter, MockTx, Reaction},
    outcome::ClientError,
    wire::hash,
};
pub fn consumption_nullifier(keys: &StreamKeys, contract: &[u8; 32], lei: &[u8; 16]) -> [u8; 32] {
    hash(&[
        b"mpe/v1/consume",
        &keys.network,
        contract,
        &keys.event_secret(lei),
    ])
}
pub fn reaction_transaction(
    keys: &StreamKeys,
    delivery: &Delivery,
    inclusion: Option<InclusionProof>,
    now: u64,
) -> Result<MockTx, ClientError> {
    Ok(MockTx {
        contract: keys.destination,
        intents: vec![],
        action: Action::Reaction(Box::new(Reaction {
            statement: delivery.event.statement.clone(),
            signature: delivery.event.signature.to_vec(),
            nullifier: consumption_nullifier(keys, &keys.destination, &delivery.event.event.lei),
            inclusion,
        })),
        ttl: now + 600,
        fee: 1,
    })
}
pub fn mark_final(
    delivery: &mut Delivery,
    proof: &InclusionProof,
    ledger: &dyn LedgerAdapter,
) -> Result<bool, ClientError> {
    let anchors = ledger
        .anchors(proof.window)
        .map_err(crate::fallback::map_error)?;
    let valid = anchors
        .iter()
        .any(|a| proof.verify(&delivery.eid, &a.payload));
    if valid {
        delivery.finality = crate::subscriber::Finality::Final;
    }
    Ok(valid)
}
pub fn verify_whole_window(
    deliveries: &mut [Delivery],
    batch: &mpe_core::anchor::Batch,
    finalized: &AnchorPayload,
) -> bool {
    if batch.payload.window != finalized.window
        || batch.payload.root != finalized.root
        || batch.payload.counts != finalized.counts
    {
        return false;
    }
    for delivery in deliveries {
        if batch
            .leaves
            .iter()
            .any(|list| list.binary_search(&delivery.eid).is_ok())
        {
            delivery.finality = crate::subscriber::Finality::Final;
        }
    }
    true
}
#[cfg(test)]
mod tests {
    use super::*;
    use crate::subscriber::{Carrier, Finality, Subscriber, Subscription};
    use ed25519_dalek::SigningKey;
    use mpe_core::{
        anchor::Batch,
        keys::StreamKeys,
        ledger::{MockContract, MockLedger},
        seal::{seal, EventIn},
        wire::{eid, MOCK_NETWORK},
    };
    use rand::SeedableRng;
    use rand_chacha::ChaCha20Rng;
    use std::{collections::HashSet, sync::Arc};
    #[test]
    fn nullifier_vectors() {
        let k = StreamKeys::new(MOCK_NETWORK, [7; 32], 1).unwrap();
        let a = consumption_nullifier(&k, &[1; 32], &[2; 16]);
        assert_eq!(a, consumption_nullifier(&k, &[1; 32], &[2; 16]));
        assert_ne!(a, consumption_nullifier(&k, &[2; 32], &[2; 16]));
        assert_ne!(a, consumption_nullifier(&k, &[1; 32], &[3; 16]));
    }
    #[test]
    fn hundred_reactors_one_effect_and_finalized_anchor() {
        let mut keys = StreamKeys::new(MOCK_NETWORK, [7; 32], 1).unwrap();
        keys.destination = [3; 32];
        keys.action = [4; 32];
        let signer = SigningKey::from_bytes(&[8; 32]);
        let pubs = vec![signer.verifying_key().to_bytes()];
        let ev = EventIn {
            payload: vec![1],
            lei: [9; 16],
            seq: 1,
            schema: [1; 8],
            schema_version: 1,
            key_index: 0,
        };
        let b = seal(
            &keys,
            &signer,
            &ev,
            None,
            100,
            &mut ChaCha20Rng::seed_from_u64(42),
        )
        .unwrap();
        let mut sub = Subscriber::default();
        sub.install(Subscription {
            keys: keys.clone(),
            publishers: pubs.clone(),
        })
        .unwrap();
        let mut d = sub.process(&b, Carrier::Overlay, 100).unwrap();
        let batch = Batch::new(1, vec![vec![eid(&MOCK_NETWORK, &b).unwrap()]]).unwrap();
        let proof = batch.inclusion(&d.eid).unwrap();
        let ledger = Arc::new(MockLedger::new(MOCK_NETWORK, 100, vec![], vec![], 1));
        ledger.add_contract(
            keys.destination,
            MockContract {
                publishers: HashSet::from([pubs[0]]),
                action: keys.action,
                nullifiers: HashSet::new(),
                effects: vec![],
            },
        );
        ledger
            .submit(MockTx {
                contract: [1; 32],
                intents: vec![],
                action: Action::Anchor(batch.payload),
                ttl: 1000,
                fee: 1,
            })
            .unwrap();
        ledger.advance_to(106).unwrap();
        assert!(!mark_final(&mut d, &proof, &*ledger).unwrap());
        assert_eq!(d.finality, Finality::Gossip);
        ledger.advance_to(124).unwrap();
        assert!(mark_final(&mut d, &proof, &*ledger).unwrap());
        let mut forged = proof.clone();
        forged.batch_root[0] ^= 1;
        assert!(!mark_final(&mut d, &forged, &*ledger).unwrap());
        ledger.register_reaction_witness(
            &d.event.statement,
            d.eid,
            consumption_nullifier(&keys, &keys.destination, &d.event.event.lei),
            u64::from(d.event.expiry),
        );
        let tx = reaction_transaction(&keys, &d, Some(proof), 124).unwrap();
        if let Action::Reaction(reaction) = &tx.action {
            assert_eq!(reaction.statement, d.event.statement);
            assert_eq!(reaction.signature, d.event.signature);
            let visible = format!("{reaction:?}");
            assert!(!visible.contains("stream_secret"));
            assert!(!visible.contains("body:"));
            let mut forged = tx.clone();
            if let Action::Reaction(r) = &mut forged.action {
                r.nullifier[0] ^= 1;
            }
            let ticket = ledger.submit(forged).unwrap();
            ledger.advance_to(130).unwrap();
            assert_eq!(
                ledger.tx_status(&ticket).unwrap(),
                mpe_core::ledger::TxStatus::Failed
            );
            assert_eq!(ledger.effect_count(&keys.destination), 0);
            let mut forged = tx.clone();
            if let Action::Reaction(r) = &mut forged.action {
                r.signature[0] ^= 1;
            }
            let ticket = ledger.submit(forged).unwrap();
            ledger.advance_to(136).unwrap();
            assert_eq!(
                ledger.tx_status(&ticket).unwrap(),
                mpe_core::ledger::TxStatus::Failed
            );
        }
        std::thread::scope(|scope| {
            for _ in 0..100 {
                let ledger = ledger.clone();
                let tx = tx.clone();
                scope.spawn(move || ledger.submit(tx).unwrap());
            }
        });
        ledger.advance_to(142).unwrap();
        assert_eq!(ledger.effect_count(&keys.destination), 1);
    }
}
