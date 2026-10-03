use async_trait::async_trait;
use ed25519_dalek::SigningKey;
use mpe_core::{
    admission::{nullifier, share, AdmissionProof, AdmissionPublic, AdmissionWitness},
    clock::Clock,
    keys::{CryptoRngCore, StreamKeys},
    outcome::ClientError,
    seal::{seal, EventIn},
    wire::{class_for, eid, Eid},
};
use rand::{seq::SliceRandom, Rng};
use std::{collections::HashMap, sync::Arc, time::Duration};
pub struct Publisher {
    pub keys: StreamKeys,
    pub signer: SigningKey,
    pub witness: AdmissionWitness,
    pub root: [u8; 32],
    pub proof: Arc<dyn AdmissionProof>,
    pub next_seq: u64,
    pub key_index: u16,
    used: HashMap<(u64, u8), u16>,
}
#[derive(Clone)]
pub struct Publication {
    pub wire: Vec<u8>,
    pub eid: Eid,
    pub event: EventIn,
    pub epoch: u64,
}
#[async_trait]
pub trait Ingress: Send + Sync {
    async fn submit(&self, peer: &str, bytes: &[u8]) -> Result<Option<Eid>, ClientError>;
}
impl Publisher {
    pub fn new(
        keys: StreamKeys,
        signer: SigningKey,
        witness: AdmissionWitness,
        root: [u8; 32],
        proof: Arc<dyn AdmissionProof>,
    ) -> Self {
        Self {
            keys,
            signer,
            witness,
            root,
            proof,
            next_seq: 1,
            key_index: 0,
            used: HashMap::new(),
        }
    }
    pub fn prepare(
        &mut self,
        payload: Vec<u8>,
        requested: Option<u8>,
        now: u64,
        rng: &mut dyn CryptoRngCore,
    ) -> Result<Publication, ClientError> {
        let min = class_for(payload.len())?;
        let class = requested.unwrap_or(min);
        if class > 3 || class < min {
            return Err(ClientError::TooLarge);
        }
        let epoch = mpe_core::clock::epoch(now);
        let index = *self.used.get(&(epoch, class)).unwrap_or(&0);
        if index >= self.witness.limits[class as usize] {
            return Err(ClientError::NotReady);
        }
        let mut lei = [0; 16];
        rng.try_fill_bytes(&mut lei)
            .map_err(|_| ClientError::NotReady)?;
        let event = EventIn {
            payload,
            lei,
            seq: self.next_seq,
            schema: *b"mpe/data",
            schema_version: 1,
            key_index: self.key_index,
        };
        let mut wire = seal(&self.keys, &self.signer, &event, Some(class), now, rng)?;
        let id = eid(&self.keys.network, &wire)?;
        let public = AdmissionPublic {
            network: self.keys.network,
            epoch,
            root: self.root,
            nullifier: nullifier(&self.witness.secret, epoch, class, index),
            share_y: share(&self.witness.secret, epoch, class, index, &id),
            size_class: class,
            eid: id,
        };
        let mut witness = self.witness.clone();
        witness.credit_index = index;
        let proof = self.proof.prove(&witness, &public)?;
        if proof.len() != 256 {
            return Err(ClientError::SessionUpdateRequired);
        }
        wire[8..16].copy_from_slice(&epoch.to_be_bytes());
        wire[16..48].copy_from_slice(&self.root);
        wire[48..80].copy_from_slice(&public.nullifier);
        wire[80..112].copy_from_slice(&public.share_y);
        wire[112..368].copy_from_slice(&proof);
        self.used.insert((epoch, class), index + 1);
        self.used.retain(|(e, _), _| *e + 2 >= epoch);
        self.next_seq = self
            .next_seq
            .checked_add(1)
            .ok_or(ClientError::SessionUpdateRequired)?;
        Ok(Publication {
            wire,
            eid: id,
            event,
            epoch,
        })
    }
    pub async fn publish(
        &self,
        publication: &Publication,
        peers: &[String],
        transport: &dyn Ingress,
        clock: &dyn Clock,
    ) -> Result<Eid, ClientError> {
        if peers.len() < 2 {
            return Err(ClientError::NotReady);
        }
        let mut selected = peers.to_vec();
        selected.shuffle(&mut rand::thread_rng());
        for peer in selected.iter().take(3) {
            if clock.now() >= publication.epoch.saturating_mul(60).saturating_add(80) {
                break;
            }
            let deadline = tokio::time::Instant::now() + Duration::from_secs(5);
            let result =
                tokio::time::timeout_at(deadline, transport.submit(peer, &publication.wire)).await;
            if let Ok(Ok(Some(id))) = result {
                if id == publication.eid {
                    return Ok(id);
                }
            }
            tokio::time::sleep_until(deadline).await;
        }
        Err(ClientError::NotAccepted)
    }
    pub fn choose_ingress<R: Rng>(peers: &[String], rng: &mut R) -> Result<String, ClientError> {
        if peers.len() < 2 {
            return Err(ClientError::NotReady);
        }
        peers.choose(rng).cloned().ok_or(ClientError::NotReady)
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use mpe_core::{
        admission::{Member, StandInRln, LIMITS},
        wire::MOCK_NETWORK,
    };
    use rand::SeedableRng;
    use rand_chacha::ChaCha20Rng;
    fn fixture() -> (Publisher, ChaCha20Rng) {
        let m = Member::new([7; 32]);
        let p = Arc::new(StandInRln::new(vec![m.clone()]));
        (
            Publisher::new(
                StreamKeys::new(MOCK_NETWORK, [8; 32], 1).unwrap(),
                SigningKey::from_bytes(&[9; 32]),
                AdmissionWitness {
                    secret: m.secret,
                    credit_index: 0,
                    limits: LIMITS,
                },
                [1; 32],
                p,
            ),
            ChaCha20Rng::seed_from_u64(42),
        )
    }
    #[test]
    fn second_authorized_publisher_index() {
        let (mut p, mut r) = fixture();
        p.key_index = 1;
        let b = p.prepare(vec![1], None, 60, &mut r).unwrap();
        let other = SigningKey::from_bytes(&[33; 32]);
        assert!(mpe_core::seal::open(
            &p.keys,
            &b.wire,
            &[
                other.verifying_key().to_bytes(),
                p.signer.verifying_key().to_bytes()
            ],
            60
        )
        .is_ok());
    }
    #[test]
    fn seq_monotonic() {
        let (mut p, mut r) = fixture();
        for n in 1..=1000 {
            let b = p.prepare(vec![1], None, n * 60, &mut r).unwrap();
            assert_eq!(b.event.seq, n);
        }
    }
    #[test]
    fn too_large_before_admission() {
        let (mut p, mut r) = fixture();
        assert!(matches!(
            p.prepare(vec![0; 16215], None, 60, &mut r),
            Err(ClientError::TooLarge)
        ));
        assert_eq!(p.next_seq, 1);
        assert!(p.used.is_empty());
    }
    #[test]
    fn one_ingress_of_two() {
        let mut r = ChaCha20Rng::seed_from_u64(42);
        let peers = vec!["a".into(), "b".into()];
        let selected: std::collections::HashSet<_> = (0..1000)
            .map(|_| Publisher::choose_ingress(&peers, &mut r).unwrap())
            .collect();
        assert_eq!(selected.len(), 2);
    }
}

#[cfg(test)]
mod retry_tests {
    use super::*;
    use mpe_core::{
        admission::{Member, StandInRln, LIMITS},
        clock::SimClock,
        wire::MOCK_NETWORK,
    };
    use rand::SeedableRng;
    use rand_chacha::ChaCha20Rng;
    use std::{sync::Mutex, time::Instant};
    struct FirstSilent {
        calls: Mutex<Vec<(String, Vec<u8>, Instant)>>,
        eid: Eid,
    }
    #[async_trait]
    impl Ingress for FirstSilent {
        async fn submit(&self, peer: &str, bytes: &[u8]) -> Result<Option<Eid>, ClientError> {
            let mut calls = self.calls.lock().unwrap();
            calls.push((peer.to_string(), bytes.to_vec(), Instant::now()));
            Ok(if calls.len() == 1 {
                None
            } else {
                Some(self.eid)
            })
        }
    }
    fn fixture() -> (Publisher, Publication) {
        let m = Member::new([7; 32]);
        let proof = Arc::new(StandInRln::new(vec![m.clone()]));
        let mut p = Publisher::new(
            StreamKeys::new(MOCK_NETWORK, [8; 32], 1).unwrap(),
            SigningKey::from_bytes(&[9; 32]),
            AdmissionWitness {
                secret: m.secret,
                credit_index: 0,
                limits: LIMITS,
            },
            [1; 32],
            proof,
        );
        let b = p
            .prepare(vec![1], None, 60, &mut ChaCha20Rng::seed_from_u64(42))
            .unwrap();
        (p, b)
    }
    #[tokio::test]
    async fn retry_to_second_node_identical_bytes() {
        let (p, b) = fixture();
        let t = FirstSilent {
            calls: Mutex::new(vec![]),
            eid: b.eid,
        };
        let clock = SimClock::new(60);
        assert_eq!(
            p.publish(&b, &["a".into(), "b".into()], &t, &clock)
                .await
                .unwrap(),
            b.eid
        );
        let calls = t.calls.lock().unwrap();
        assert_eq!(calls.len(), 2);
        assert_ne!(calls[0].0, calls[1].0);
        assert_eq!(calls[0].1, calls[1].1);
        assert!(calls[1].2.duration_since(calls[0].2) >= Duration::from_secs(5));
    }
    #[tokio::test]
    async fn retry_stops_after_epoch_tolerance() {
        let (p, b) = fixture();
        let t = FirstSilent {
            calls: Mutex::new(vec![]),
            eid: b.eid,
        };
        let clock = SimClock::new(141);
        assert_eq!(
            p.publish(&b, &["a".into(), "b".into()], &t, &clock).await,
            Err(ClientError::NotAccepted)
        );
        assert!(t.calls.lock().unwrap().is_empty());
    }
}
