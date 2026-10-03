use crate::{
    admission::{decode_public, AdmissionProof, AdmissionPublic, ProofVerdict, RegistryView},
    wire::{Eid, Envelope, HEADER_LEN, LIFETIME},
};
use std::{collections::HashMap, sync::Arc};
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum RejectReason {
    Malformed,
    Oversize,
    BadAdmission,
    OverQuota,
    Version,
    Reserved,
    Class,
    Length,
    Shard,
    FutureExpiry,
    Filler,
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum IgnoreReason {
    Replay,
    Expired,
    Epoch,
    Root,
    Restart,
    Busy,
    Rate,
    Equivocation,
    Stale,
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Outcome {
    Accept(Eid),
    Reject(RejectReason),
    Ignore(IgnoreReason),
}
pub fn structural(bytes: &[u8], version: u8, shard: u8) -> Result<(), RejectReason> {
    if bytes.len() < 8 {
        return Err(RejectReason::Malformed);
    }
    if bytes[0] != version {
        return Err(RejectReason::Version);
    }
    if bytes[3] != 0 {
        return Err(RejectReason::Reserved);
    }
    if bytes[1] > 3 {
        return Err(RejectReason::Class);
    }
    let expected = HEADER_LEN + crate::wire::BODY_LENGTHS[bytes[1] as usize];
    if bytes.len() != expected {
        return Err(if bytes.len() > expected {
            RejectReason::Oversize
        } else {
            RejectReason::Length
        });
    }
    if bytes[2] != shard {
        return Err(RejectReason::Shard);
    }
    Ok(())
}
#[derive(Clone)]
pub struct Job {
    pub public: AdmissionPublic,
    pub wire: Vec<u8>,
    pub expiry: u64,
    pub peer: String,
}
pub enum Precheck {
    Done(Outcome),
    NeedsProof(Job),
}
#[derive(Clone)]
pub struct Evidence {
    pub first: Vec<u8>,
    pub second: Vec<u8>,
    pub nullifier: [u8; 32],
}
struct Bucket {
    tokens: f64,
    at: u64,
}
pub struct Validator {
    pub proof: Arc<dyn AdmissionProof>,
    pub view: RegistryView,
    pub started: u64,
    seen: HashMap<Eid, u64>,
    nullifiers: HashMap<[u8; 32], (Eid, Vec<u8>, u64)>,
    rates: HashMap<(String, u8), Bucket>,
    pub evidence: Vec<Evidence>,
    pub seen_cap: usize,
}
impl Validator {
    pub fn new(proof: Arc<dyn AdmissionProof>, view: RegistryView, started: u64) -> Self {
        Self {
            proof,
            view,
            started,
            seen: HashMap::new(),
            nullifiers: HashMap::new(),
            rates: HashMap::new(),
            evidence: vec![],
            seen_cap: 2_000_000,
        }
    }
    pub fn cache_len(&self) -> usize {
        self.seen.len()
    }
    pub fn prune(&mut self, now: u64) {
        self.seen.retain(|_, until| *until >= now);
        self.nullifiers.retain(|_, (_, _, until)| *until >= now);
        self.rates.retain(|_, b| now.saturating_sub(b.at) < 140);
    }
    pub fn precheck(
        &mut self,
        bytes: &[u8],
        version: u8,
        shard: u8,
        peer: &str,
        now: u64,
    ) -> Precheck {
        if shard >= self.view.shards || bytes.get(2).is_some_and(|s| *s >= self.view.shards) {
            return Precheck::Done(Outcome::Reject(RejectReason::Shard));
        }
        self.prune(now);
        let bucket = self
            .rates
            .entry((peer.to_owned(), shard))
            .or_insert(Bucket {
                tokens: 20.,
                at: now,
            });
        bucket.tokens = (bucket.tokens + 20. * now.saturating_sub(bucket.at) as f64).min(20.);
        bucket.at = now;
        if bucket.tokens < 1. {
            return Precheck::Done(Outcome::Ignore(IgnoreReason::Rate));
        }
        bucket.tokens -= 1.;
        if let Err(reason) = structural(bytes, version, shard) {
            return Precheck::Done(Outcome::Reject(reason));
        }
        let Ok(env) = Envelope::parse(bytes) else {
            return Precheck::Done(Outcome::Reject(RejectReason::Malformed));
        };
        let expiry = u64::from(env.header.expiry);
        if expiry > now.saturating_add(LIFETIME + 60) {
            return Precheck::Done(if self.view.stale(now) {
                Outcome::Ignore(IgnoreReason::Stale)
            } else {
                Outcome::Reject(RejectReason::FutureExpiry)
            });
        }
        if expiry < now.saturating_sub(60) {
            return Precheck::Done(Outcome::Ignore(IgnoreReason::Expired));
        }
        if env.slot[360..].iter().any(|&b| b != 0) {
            return Precheck::Done(Outcome::Reject(RejectReason::Filler));
        }
        let eid = env.eid(&self.view.network);
        if self.seen.contains_key(&eid) {
            return Precheck::Done(Outcome::Ignore(IgnoreReason::Replay));
        }
        let genesis_exemption = self
            .view
            .roots
            .iter()
            .map(|r| r.published_at)
            .min()
            .is_some_and(|published| self.started < published);
        if now < self.started.saturating_add(140) && !genesis_exemption {
            return Precheck::Done(Outcome::Ignore(IgnoreReason::Restart));
        }
        let Ok(public) = decode_public(env.slot, self.view.network, env.header.class, eid) else {
            return Precheck::Done(Outcome::Reject(RejectReason::BadAdmission));
        };
        let Some(epoch_start) = public.epoch.checked_mul(60) else {
            return Precheck::Done(Outcome::Ignore(IgnoreReason::Epoch));
        };
        if now < epoch_start.saturating_sub(20) || now >= epoch_start.saturating_add(80) {
            return Precheck::Done(Outcome::Ignore(IgnoreReason::Epoch));
        }
        if !self.view.eligible(&public.root, now) {
            return Precheck::Done(Outcome::Ignore(IgnoreReason::Root));
        }
        if self
            .nullifiers
            .get(&public.nullifier)
            .is_some_and(|(known, _, _)| known == &eid)
        {
            return Precheck::Done(Outcome::Ignore(IgnoreReason::Replay));
        }
        if self.seen.len() >= self.seen_cap {
            return Precheck::Done(Outcome::Ignore(IgnoreReason::Busy));
        }
        Precheck::NeedsProof(Job {
            public,
            wire: bytes.to_vec(),
            expiry,
            peer: peer.to_owned(),
        })
    }
    pub fn finish(&mut self, job: Job, verdict: ProofVerdict, now: u64) -> Outcome {
        match verdict {
            ProofVerdict::Invalid => return Outcome::Reject(RejectReason::BadAdmission),
            ProofVerdict::OverQuota => return Outcome::Reject(RejectReason::OverQuota),
            ProofVerdict::UnknownRoot => return Outcome::Ignore(IgnoreReason::Root),
            ProofVerdict::Valid => {}
        }
        if self.seen.contains_key(&job.public.eid) {
            return Outcome::Ignore(IgnoreReason::Replay);
        }
        if let Some((_, first, _)) = self.nullifiers.get(&job.public.nullifier) {
            if self.evidence.len() < 128 {
                self.evidence.push(Evidence {
                    first: first.clone(),
                    second: job.wire,
                    nullifier: job.public.nullifier,
                });
            }
            return Outcome::Ignore(IgnoreReason::Equivocation);
        }
        self.seen
            .insert(job.public.eid, job.expiry.saturating_add(60));
        self.nullifiers.insert(
            job.public.nullifier,
            (job.public.eid, job.wire, now.saturating_add(140)),
        );
        Outcome::Accept(job.public.eid)
    }
    pub fn validate(
        &mut self,
        bytes: &[u8],
        version: u8,
        shard: u8,
        peer: &str,
        now: u64,
    ) -> Outcome {
        match self.precheck(bytes, version, shard, peer, now) {
            Precheck::Done(out) => out,
            Precheck::NeedsProof(job) => {
                let verdict = self
                    .proof
                    .verify(&job.public, &job.wire[112..368], &self.view);
                self.finish(job, verdict, now)
            }
        }
    }
    pub fn validate_historic(&self, bytes: &[u8], now: u64) -> Outcome {
        if let Err(r) = structural(bytes, 1, bytes.get(2).copied().unwrap_or(0)) {
            return Outcome::Reject(r);
        }
        let Ok(env) = Envelope::parse(bytes) else {
            return Outcome::Reject(RejectReason::Malformed);
        };
        if env.slot[360..].iter().any(|&b| b != 0) {
            return Outcome::Reject(RejectReason::Filler);
        }
        let Ok(p) = decode_public(
            env.slot,
            self.view.network,
            env.header.class,
            env.eid(&self.view.network),
        ) else {
            return Outcome::Reject(RejectReason::BadAdmission);
        };
        if self.view.historic_root(&p.root, now).is_none() {
            return Outcome::Ignore(IgnoreReason::Root);
        }
        match self.proof.verify(&p, &bytes[112..368], &self.view) {
            ProofVerdict::Valid => Outcome::Accept(p.eid),
            _ => Outcome::Reject(RejectReason::BadAdmission),
        }
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use crate::{
        admission::{Member, RootRecord, StandInRln},
        wire::{Header, MOCK_NETWORK},
    };
    use std::sync::atomic::Ordering;
    fn fixture() -> (Arc<StandInRln>, Validator, Vec<u8>) {
        let proof = Arc::new(StandInRln::new(vec![Member::new([7; 32])]));
        let view = RegistryView {
            network: MOCK_NETWORK,
            roots: vec![RootRecord {
                root: [1; 32],
                period_start: 0,
                published_at: 1,
                superseded_at: None,
            }],
            finalized_time: 60,
            shards: 1,
            bus_paused: false,
        };
        let v = Validator::new(proof.clone(), view, 0);
        let mut b = Header {
            version: 1,
            class: 0,
            shard: 0,
            expiry: 172860,
        }
        .encode()
        .to_vec();
        b.resize(776, 0);
        proof
            .attach(&mut b, 0, 0, 1, MOCK_NETWORK, [1; 32])
            .unwrap();
        (proof, v, b)
    }
    #[test]
    fn reserved_bits() {
        for bit in 0..8 {
            let (_, mut v, mut b) = fixture();
            b[3] = 1 << bit;
            assert_eq!(
                v.validate(&b, 1, 0, "peer", 60),
                Outcome::Reject(RejectReason::Reserved)
            );
        }
    }
    #[test]
    fn outcome_table() {
        let mutations = [
            (0, 2, RejectReason::Version),
            (1, 4, RejectReason::Class),
            (2, 1, RejectReason::Shard),
            (3, 1, RejectReason::Reserved),
            (368, 1, RejectReason::Filler),
            (112, 1, RejectReason::BadAdmission),
        ];
        for (offset, value, want) in mutations {
            let (_, mut v, mut b) = fixture();
            b[offset] = value;
            assert_eq!(v.validate(&b, 1, 0, "p", 60), Outcome::Reject(want));
        }
        let (_, mut v, b) = fixture();
        assert!(matches!(v.validate(&b, 1, 0, "p", 60), Outcome::Accept(_)));
        assert_eq!(
            v.validate(&b, 1, 0, "p", 61),
            Outcome::Ignore(IgnoreReason::Replay)
        );
    }
    #[test]
    fn structural_before_crypto() {
        let (p, mut v, b) = fixture();
        for i in 0..10_000 {
            let mut bad = b.clone();
            bad[3] = 1;
            assert!(matches!(
                v.validate(&bad, 1, 0, &i.to_string(), 60),
                Outcome::Reject(_)
            ));
        }
        assert_eq!(p.calls.load(Ordering::Relaxed), 0);
    }
    #[test]
    fn filler_byte_reject() {
        for offset in 368..520 {
            let (_, mut v, mut b) = fixture();
            b[offset] = 1;
            assert_eq!(
                v.validate(&b, 1, 0, "p", 60),
                Outcome::Reject(RejectReason::Filler)
            );
        }
    }
    #[test]
    fn length_off_by_one() {
        let (_, mut v, b) = fixture();
        assert_eq!(
            v.validate(&b[..775], 1, 0, "p", 60),
            Outcome::Reject(RejectReason::Length)
        );
        let mut long = b;
        long.push(0);
        assert_eq!(
            v.validate(&long, 1, 0, "p", 60),
            Outcome::Reject(RejectReason::Oversize)
        );
    }
    #[test]
    fn stale_epoch_never_verified() {
        let (p, mut v, b) = fixture();
        assert_eq!(
            v.validate(&b, 1, 0, "p", 141),
            Outcome::Ignore(IgnoreReason::Epoch)
        );
        assert_eq!(p.calls.load(Ordering::Relaxed), 0);
    }
    #[test]
    fn epoch_tolerance() {
        let (_, mut v, b) = fixture();
        assert!(matches!(v.validate(&b, 1, 0, "p", 139), Outcome::Accept(_)));
        let (_, mut v, b) = fixture();
        assert_eq!(
            v.validate(&b, 1, 0, "p", 141),
            Outcome::Ignore(IgnoreReason::Epoch)
        );
    }
    #[test]
    fn expiry_upper_bound_and_stale() {
        let (p, mut v, mut b) = fixture();
        b[4..8].copy_from_slice(&172920_u32.to_be_bytes());
        p.attach(&mut b, 0, 0, 1, MOCK_NETWORK, [1; 32]).unwrap();
        assert!(matches!(v.validate(&b, 1, 0, "p", 60), Outcome::Accept(_)));
        let (_, mut v, mut b) = fixture();
        b[4..8].copy_from_slice(&172921_u32.to_be_bytes());
        assert_eq!(
            v.validate(&b, 1, 0, "p", 60),
            Outcome::Reject(RejectReason::FutureExpiry)
        );
        v.view.finalized_time = 0;
        b[4..8].copy_from_slice(&172922_u32.to_be_bytes());
        assert_eq!(
            v.validate(&b, 1, 0, "p", 61),
            Outcome::Ignore(IgnoreReason::Stale)
        );
    }
    #[test]
    fn expired_ignore() {
        let (_, mut v, mut b) = fixture();
        b[4..8].copy_from_slice(&0_u32.to_be_bytes());
        assert_eq!(
            v.validate(&b, 1, 0, "p", 61),
            Outcome::Ignore(IgnoreReason::Expired)
        );
    }
    #[test]
    fn rejected_copy_does_not_block_valid_copy() {
        let (_, mut v, b) = fixture();
        let mut bad = b.clone();
        bad[112] ^= 1;
        assert_eq!(
            v.validate(&bad, 1, 0, "p", 60),
            Outcome::Reject(RejectReason::BadAdmission)
        );
        assert!(matches!(v.validate(&b, 1, 0, "p", 60), Outcome::Accept(_)));
    }
    #[test]
    fn equivocation_ignore_and_evidence() {
        let (p, mut v, b) = fixture();
        assert!(matches!(v.validate(&b, 1, 0, "p", 60), Outcome::Accept(_)));
        let mut conflicting = b;
        conflicting[700] = 1;
        p.attach(&mut conflicting, 0, 0, 1, MOCK_NETWORK, [1; 32])
            .unwrap();
        assert_eq!(
            v.validate(&conflicting, 1, 0, "p", 60),
            Outcome::Ignore(IgnoreReason::Equivocation)
        );
        assert_eq!(v.evidence.len(), 1);
    }
    #[test]
    fn seen_set_retention() {
        let (_, mut v, b) = fixture();
        assert!(matches!(v.validate(&b, 1, 0, "p", 60), Outcome::Accept(_)));
        for now in [61, 172859] {
            assert_eq!(
                v.validate(&b, 1, 0, "p", now),
                Outcome::Ignore(IgnoreReason::Replay)
            );
        }
    }
    #[test]
    fn restart_barrier() {
        let (_, mut v, b) = fixture();
        v.started = 60;
        assert_eq!(
            v.validate(&b, 1, 0, "p", 61),
            Outcome::Ignore(IgnoreReason::Restart)
        );
        assert_eq!(
            v.validate(&b, 1, 0, "p", 201),
            Outcome::Ignore(IgnoreReason::Epoch)
        );
        let (_, mut genesis, b) = fixture();
        assert!(matches!(
            genesis.validate(&b, 1, 0, "p", 60),
            Outcome::Accept(_)
        ));
    }
    #[test]
    fn root_window_and_stale_root_bound() {
        let (_, v, _) = fixture();
        assert!(v.view.eligible(&[1; 32], 7200));
        let mut view = v.view;
        view.roots[0].superseded_at = Some(1);
        assert!(!view.eligible(&[1; 32], 3602));
        view.roots[0].superseded_at = None;
        assert!(!view.eligible(&[1; 32], 90001));
    }
    #[test]
    fn per_peer_rate() {
        let (p, mut v, b) = fixture();
        for i in 0..100 {
            let mut msg = b.clone();
            msg[700] = i;
            p.attach(&mut msg, 0, i as u16, 1, MOCK_NETWORK, [1; 32])
                .unwrap();
            let _ = v.validate(&msg, 1, 0, "p", 60);
        }
        assert_eq!(p.calls.load(Ordering::Relaxed), 20);
    }
    #[test]
    fn random_body_same_outcome() {
        let (p, mut v, mut b) = fixture();
        b[520..].fill(0xff);
        p.attach(&mut b, 0, 0, 1, MOCK_NETWORK, [1; 32]).unwrap();
        assert!(matches!(v.validate(&b, 1, 0, "p", 60), Outcome::Accept(_)));
    }
}
