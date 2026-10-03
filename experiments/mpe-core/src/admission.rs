use crate::wire::{hash, Eid, Error, NetworkId, SLOT_LEN};
use curve25519_dalek::scalar::Scalar;
use hkdf::Hkdf;
use hmac::{Hmac, Mac};
use sha2::{Digest, Sha256, Sha512};
use std::{
    collections::HashMap,
    sync::{
        atomic::{AtomicU64, Ordering},
        Mutex,
    },
};
use subtle::ConstantTimeEq;
pub const LIMITS: [u16; 4] = [64, 16, 4, 1];
#[derive(Clone, Debug)]
pub struct Member {
    pub secret: [u8; 32],
    pub limits: [u16; 4],
}
impl Member {
    pub fn new(secret: [u8; 32]) -> Self {
        Self {
            secret: Scalar::from_bytes_mod_order(secret).to_bytes(),
            limits: LIMITS,
        }
    }
    pub fn commitment(&self) -> [u8; 32] {
        hash(&[b"mpe/v1/idc", &self.secret])
    }
    pub fn leaf(&self) -> [u8; 32] {
        let limits: Vec<u8> = self.limits.iter().flat_map(|n| n.to_be_bytes()).collect();
        hash(&[b"mpe/v1/leaf", &self.commitment(), &limits])
    }
}
#[derive(Clone, Debug)]
pub struct RootRecord {
    pub root: [u8; 32],
    pub period_start: u64,
    pub published_at: u64,
    pub superseded_at: Option<u64>,
}
#[derive(Clone, Debug)]
pub struct RegistryView {
    pub network: NetworkId,
    pub roots: Vec<RootRecord>,
    pub finalized_time: u64,
    pub shards: u8,
    pub bus_paused: bool,
}
impl RegistryView {
    pub fn stale(&self, now: u64) -> bool {
        now.abs_diff(self.finalized_time) > 60
    }
    pub fn eligible(&self, root: &[u8; 32], now: u64) -> bool {
        self.roots.iter().any(|r| {
            &r.root == root
                && r.superseded_at.is_none_or(|t| now.saturating_sub(t) < 3600)
                && now < r.period_start.saturating_add(90_000)
        })
    }
    pub fn historic_root(&self, root: &[u8; 32], now: u64) -> Option<RootRecord> {
        self.roots
            .iter()
            .find(|r| &r.root == root && now.saturating_sub(r.published_at) <= 176400)
            .cloned()
    }
}
#[derive(Clone, Debug)]
pub struct AdmissionPublic {
    pub network: NetworkId,
    pub epoch: u64,
    pub root: [u8; 32],
    pub nullifier: [u8; 32],
    pub share_y: [u8; 32],
    pub size_class: u8,
    pub eid: Eid,
}
#[derive(Clone, Debug)]
pub struct AdmissionWitness {
    pub secret: [u8; 32],
    pub credit_index: u16,
    pub limits: [u16; 4],
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum ProofVerdict {
    Valid,
    Invalid,
    OverQuota,
    UnknownRoot,
}
pub trait AdmissionProof: Send + Sync {
    fn proof_len(&self) -> usize;
    fn prove(&self, w: &AdmissionWitness, p: &AdmissionPublic) -> Result<Vec<u8>, Error>;
    fn verify(&self, p: &AdmissionPublic, proof: &[u8], ctx: &RegistryView) -> ProofVerdict;
}
fn scalar(parts: &[&[u8]]) -> Scalar {
    let mut h = Sha512::new();
    for p in parts {
        h.update(p);
    }
    Scalar::from_bytes_mod_order_wide(&h.finalize().into())
}
pub fn slope(secret: &[u8; 32], epoch: u64, class: u8, index: u16) -> Scalar {
    scalar(&[
        b"mpe/v1/rln/a1",
        secret,
        &epoch.to_be_bytes(),
        &[class],
        &index.to_be_bytes(),
    ])
}
pub fn nullifier(secret: &[u8; 32], epoch: u64, class: u8, index: u16) -> [u8; 32] {
    hash(&[
        b"mpe/v1/rln/nul",
        &slope(secret, epoch, class, index).to_bytes(),
    ])
}
fn x(eid: &Eid) -> Scalar {
    scalar(&[b"mpe/v1/rln/x", eid])
}
pub fn share(secret: &[u8; 32], epoch: u64, class: u8, index: u16, eid: &Eid) -> [u8; 32] {
    (Scalar::from_bytes_mod_order(*secret) + slope(secret, epoch, class, index) * x(eid)).to_bytes()
}
pub fn recover(a: &AdmissionPublic, b: &AdmissionPublic) -> Result<[u8; 32], Error> {
    if a.nullifier != b.nullifier || a.eid == b.eid {
        return Err(Error::InvalidAdmission);
    }
    let y1 = Option::<Scalar>::from(Scalar::from_canonical_bytes(a.share_y))
        .ok_or(Error::InvalidAdmission)?;
    let y2 = Option::<Scalar>::from(Scalar::from_canonical_bytes(b.share_y))
        .ok_or(Error::InvalidAdmission)?;
    let x1 = x(&a.eid);
    let x2 = x(&b.eid);
    if x1 == x2 {
        return Err(Error::InvalidAdmission);
    }
    Ok(((y1 * x2 - y2 * x1) * (x2 - x1).invert()).to_bytes())
}
fn proof_bytes(secret: &[u8; 32], p: &AdmissionPublic) -> Result<Vec<u8>, Error> {
    let mut h = Hmac::<Sha256>::new_from_slice(secret).map_err(|_| Error::InvalidAdmission)?;
    h.update(b"mpe/v1/standin");
    let prk = h.finalize().into_bytes();
    let hk = Hkdf::<Sha256>::from_prk(&prk).map_err(|_| Error::InvalidAdmission)?;
    let info = [
        p.epoch.to_be_bytes().as_slice(),
        &p.root,
        &p.nullifier,
        &p.share_y,
        &[p.size_class],
        &p.eid,
        &p.network,
    ]
    .concat();
    let mut proof = vec![0; 256];
    hk.expand(&info, &mut proof)
        .map_err(|_| Error::InvalidAdmission)?;
    Ok(proof)
}
type EpochTable = HashMap<[u8; 32], (usize, u8, u16)>;
/// Not zero knowledge: Bus Nodes possess member secrets, can link and forge. See LEAKAGE.md.
pub struct StandInRln {
    pub members: Vec<Member>,
    tables: Mutex<HashMap<u64, EpochTable>>,
    pub calls: AtomicU64,
}
impl StandInRln {
    pub fn new(members: Vec<Member>) -> Self {
        Self {
            members,
            tables: Mutex::new(HashMap::new()),
            calls: AtomicU64::new(0),
        }
    }
    // Explicit public inputs keep the stand-in relation auditable at call sites.
    #[allow(clippy::too_many_arguments)]
    pub fn public(
        &self,
        member: usize,
        index: u16,
        epoch: u64,
        class: u8,
        eid: Eid,
        network: NetworkId,
        root: [u8; 32],
    ) -> Result<AdmissionPublic, Error> {
        let m = self.members.get(member).ok_or(Error::InvalidAdmission)?;
        if class > 3 {
            return Err(Error::Malformed);
        }
        Ok(AdmissionPublic {
            network,
            epoch,
            root,
            nullifier: nullifier(&m.secret, epoch, class, index),
            share_y: share(&m.secret, epoch, class, index, &eid),
            size_class: class,
            eid,
        })
    }
    pub fn attach(
        &self,
        wire: &mut [u8],
        member: usize,
        index: u16,
        epoch: u64,
        network: NetworkId,
        root: [u8; 32],
    ) -> Result<AdmissionPublic, Error> {
        let env = crate::wire::Envelope::parse(wire)?;
        let p = self.public(
            member,
            index,
            epoch,
            env.header.class,
            env.eid(&network),
            network,
            root,
        )?;
        let m = self.members.get(member).ok_or(Error::InvalidAdmission)?;
        let proof = self.prove(
            &AdmissionWitness {
                secret: m.secret,
                credit_index: index,
                limits: m.limits,
            },
            &p,
        )?;
        wire[8..16].copy_from_slice(&epoch.to_be_bytes());
        wire[16..48].copy_from_slice(&root);
        wire[48..80].copy_from_slice(&p.nullifier);
        wire[80..112].copy_from_slice(&p.share_y);
        wire[112..368].copy_from_slice(&proof);
        wire[368..520].fill(0);
        Ok(p)
    }
}
impl AdmissionProof for StandInRln {
    fn proof_len(&self) -> usize {
        256
    }
    fn prove(&self, w: &AdmissionWitness, p: &AdmissionPublic) -> Result<Vec<u8>, Error> {
        if nullifier(&w.secret, p.epoch, p.size_class, w.credit_index) != p.nullifier
            || share(&w.secret, p.epoch, p.size_class, w.credit_index, &p.eid) != p.share_y
        {
            return Err(Error::InvalidAdmission);
        }
        proof_bytes(&w.secret, p)
    }
    fn verify(&self, p: &AdmissionPublic, proof: &[u8], ctx: &RegistryView) -> ProofVerdict {
        self.calls.fetch_add(1, Ordering::Relaxed);
        if p.network != ctx.network || p.size_class > 3 || proof.len() != 256 {
            return ProofVerdict::Invalid;
        }
        if !ctx.roots.iter().any(|r| r.root == p.root) {
            return ProofVerdict::UnknownRoot;
        }
        let Ok(mut tables) = self.tables.lock() else {
            return ProofVerdict::Invalid;
        };
        if !tables.contains_key(&p.epoch) {
            let mut table = HashMap::new();
            for (i, m) in self.members.iter().enumerate() {
                for c in 0..4 {
                    for index in 0..m.limits[c] * 2 {
                        table.insert(
                            nullifier(&m.secret, p.epoch, c as u8, index),
                            (i, c as u8, index),
                        );
                    }
                }
            }
            if tables.len() >= 3 {
                if let Some(old) = tables.keys().min().copied() {
                    tables.remove(&old);
                }
            }
            tables.insert(p.epoch, table);
        }
        let Some(&(member, class, index)) = tables.get(&p.epoch).and_then(|t| t.get(&p.nullifier))
        else {
            return ProofVerdict::Invalid;
        };
        let m = &self.members[member];
        if class != p.size_class || share(&m.secret, p.epoch, class, index, &p.eid) != p.share_y {
            return ProofVerdict::Invalid;
        }
        let Ok(expected) = proof_bytes(&m.secret, p) else {
            return ProofVerdict::Invalid;
        };
        if !bool::from(expected.ct_eq(proof)) {
            return ProofVerdict::Invalid;
        }
        if index >= m.limits[class as usize] {
            ProofVerdict::OverQuota
        } else {
            ProofVerdict::Valid
        }
    }
}
pub fn decode_public(
    slot: &[u8],
    network: NetworkId,
    class: u8,
    eid: Eid,
) -> Result<AdmissionPublic, Error> {
    if slot.len() != SLOT_LEN {
        return Err(Error::Malformed);
    }
    Ok(AdmissionPublic {
        network,
        epoch: u64::from_be_bytes(slot[..8].try_into().map_err(|_| Error::Malformed)?),
        root: slot[8..40].try_into().map_err(|_| Error::Malformed)?,
        nullifier: slot[40..72].try_into().map_err(|_| Error::Malformed)?,
        share_y: slot[72..104].try_into().map_err(|_| Error::Malformed)?,
        size_class: class,
        eid,
    })
}
#[cfg(test)]
mod tests {
    use super::*;
    use crate::wire::MOCK_NETWORK;
    fn view() -> RegistryView {
        RegistryView {
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
        }
    }
    #[test]
    fn secret_recovery() {
        let s = StandInRln::new(vec![Member::new([7; 32])]);
        let a = s
            .public(0, 0, 1, 0, [1; 32], MOCK_NETWORK, [1; 32])
            .unwrap();
        let b = s
            .public(0, 0, 1, 0, [2; 32], MOCK_NETWORK, [1; 32])
            .unwrap();
        assert_ne!(a.share_y, b.share_y);
        assert_eq!(recover(&a, &b).unwrap(), s.members[0].secret);
    }
    #[test]
    fn nullifier_class_epoch_index_bound() {
        let m = Member::new([7; 32]);
        let a = nullifier(&m.secret, 1, 0, 0);
        assert_ne!(a, nullifier(&m.secret, 1, 1, 0));
        assert_ne!(a, nullifier(&m.secret, 2, 0, 0));
        assert_ne!(a, nullifier(&m.secret, 1, 0, 1));
    }
    #[test]
    fn proof_mutation_and_class2_limit() {
        let s = StandInRln::new(vec![Member::new([7; 32])]);
        for i in 0..5 {
            let p = s
                .public(0, i, 1, 2, [i as u8; 32], MOCK_NETWORK, [1; 32])
                .unwrap();
            let m = &s.members[0];
            let mut proof = s
                .prove(
                    &AdmissionWitness {
                        secret: m.secret,
                        credit_index: i,
                        limits: m.limits,
                    },
                    &p,
                )
                .unwrap();
            assert_eq!(
                s.verify(&p, &proof, &view()),
                if i < 4 {
                    ProofVerdict::Valid
                } else {
                    ProofVerdict::OverQuota
                }
            );
            proof[0] ^= 1;
            assert_eq!(s.verify(&p, &proof, &view()), ProofVerdict::Invalid);
        }
    }
    #[test]
    fn epoch_boundaries() {
        assert_eq!(
            (
                crate::clock::epoch(59),
                crate::clock::epoch(60),
                crate::clock::epoch(61)
            ),
            (0, 1, 1)
        );
        assert_eq!(crate::clock::epoch(1_800_000_060), 30_000_001);
    }
    #[test]
    fn slot_unlinkable() {
        let s = StandInRln::new(vec![Member::new([7; 32]), Member::new([8; 32])]);
        let mut slots = [Vec::new(), Vec::new()];
        for (member, list) in slots.iter_mut().enumerate() {
            for i in 0..100 {
                let p = s
                    .public(
                        member,
                        i,
                        1,
                        0,
                        hash(&[&i.to_be_bytes()]),
                        MOCK_NETWORK,
                        [1; 32],
                    )
                    .unwrap();
                let m = &s.members[member];
                let proof = s
                    .prove(
                        &AdmissionWitness {
                            secret: m.secret,
                            credit_index: i,
                            limits: m.limits,
                        },
                        &p,
                    )
                    .unwrap();
                let mut slot = vec![0; 512];
                slot[..8].copy_from_slice(&p.epoch.to_be_bytes());
                slot[8..40].copy_from_slice(&p.root);
                slot[40..72].copy_from_slice(&p.nullifier);
                slot[72..104].copy_from_slice(&p.share_y);
                slot[104..360].copy_from_slice(&proof);
                list.push(slot);
            }
        }
        for offset in 0..512 {
            let ca = slots[0].iter().all(|s| s[offset] == slots[0][0][offset]);
            let cb = slots[1].iter().all(|s| s[offset] == slots[1][0][offset]);
            assert!(!(ca && cb && slots[0][0][offset] != slots[1][0][offset]));
        }
    }
}
