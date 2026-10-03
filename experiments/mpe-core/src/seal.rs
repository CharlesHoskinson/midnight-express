use crate::{
    keys::{tag, CryptoRngCore, StreamKeys},
    wire::{
        class_for, hash, Envelope, Error, Header, BODY_LENGTHS, CAPACITIES, HEADER_LEN, LIFETIME,
    },
};
use chacha20poly1305::{
    aead::{Aead, KeyInit, Payload},
    ChaCha20Poly1305, Nonce,
};
use ed25519_dalek::{Signature, Signer, SigningKey, VerifyingKey};
#[derive(Clone, Debug)]
pub struct EventIn {
    pub payload: Vec<u8>,
    pub lei: [u8; 16],
    pub seq: u64,
    pub schema: [u8; 8],
    pub schema_version: u16,
    pub key_index: u16,
}
#[derive(Clone, Debug)]
pub struct OpenedEvent {
    pub event: EventIn,
    pub creation: u32,
    pub expiry: u32,
    pub publisher: [u8; 32],
    pub signature: [u8; 64],
    pub statement: Vec<u8>,
    pub stream: [u8; 32],
}
fn aad(keys: &StreamKeys, first4: &[u8], prefix: &[u8]) -> Vec<u8> {
    [b"mpe/v1/aad".as_slice(), &keys.network, first4, prefix].concat()
}
fn statement(
    keys: &StreamKeys,
    first4: &[u8],
    prefix: &[u8],
    ev: &EventIn,
    creation: u32,
    expiry: u32,
) -> Vec<u8> {
    [
        b"mpe/v1/sig".as_slice(),
        &keys.network,
        &hash(&[&keys.network, first4, prefix]),
        &keys.stream_id(),
        &ev.lei,
        &ev.seq.to_be_bytes(),
        &ev.schema,
        &ev.schema_version.to_be_bytes(),
        &creation.to_be_bytes(),
        &expiry.to_be_bytes(),
        &hash(&[&ev.payload]),
        &keys.destination,
        &keys.action,
    ]
    .concat()
}
pub fn seal(
    keys: &StreamKeys,
    signer: &SigningKey,
    ev: &EventIn,
    requested: Option<u8>,
    now: u64,
    rng: &mut dyn CryptoRngCore,
) -> Result<Vec<u8>, Error> {
    let smallest = class_for(ev.payload.len())?;
    let class = requested.unwrap_or(smallest);
    if class > 3 || ev.payload.len() > CAPACITIES[class as usize] {
        return Err(Error::TooLarge);
    }
    let creation = u32::try_from(now).map_err(|_| Error::Malformed)?;
    let expiry = u32::try_from(now.checked_add(LIFETIME).ok_or(Error::Malformed)?)
        .map_err(|_| Error::Malformed)?;
    let h = Header {
        version: 1,
        class,
        shard: keys.shard(),
        expiry,
    };
    let mut salt = [0; 16];
    let mut nonce = [0; 12];
    rng.try_fill_bytes(&mut salt)
        .map_err(|_| Error::RandomnessUnavailable)?;
    rng.try_fill_bytes(&mut nonce)
        .map_err(|_| Error::RandomnessUnavailable)?;
    let mut prefix = salt.to_vec();
    prefix.extend_from_slice(&nonce);
    prefix.extend_from_slice(&tag(&keys.recognition(), &keys.network, &salt));
    let stmt = statement(keys, &h.encode()[..4], &prefix, ev, creation, expiry);
    let sig = signer.sign(&stmt);
    let mut pt = vec![0; BODY_LENGTHS[class as usize] - 60];
    pt[0] = 1;
    pt[1] = 1;
    pt[2..4].copy_from_slice(&1_u16.to_be_bytes());
    pt[4..6].copy_from_slice(&(ev.payload.len() as u16).to_be_bytes());
    pt[6..8].copy_from_slice(&ev.schema_version.to_be_bytes());
    pt[8..16].copy_from_slice(&ev.seq.to_be_bytes());
    pt[16..32].copy_from_slice(&ev.lei);
    pt[32..40].copy_from_slice(&ev.schema);
    pt[40..42].copy_from_slice(&ev.key_index.to_be_bytes());
    pt[42..46].copy_from_slice(&creation.to_be_bytes());
    pt[46..110].copy_from_slice(&sig.to_bytes());
    pt[110..110 + ev.payload.len()].copy_from_slice(&ev.payload);
    let enc = ChaCha20Poly1305::new((&keys.encryption(&salt)).into())
        .encrypt(
            Nonce::from_slice(&nonce),
            Payload {
                msg: &pt,
                aad: &aad(keys, &h.encode()[..4], &prefix),
            },
        )
        .map_err(|_| Error::Authentication)?;
    let mut wire = h.encode().to_vec();
    wire.resize(HEADER_LEN, 0);
    wire.extend_from_slice(&prefix);
    wire.extend_from_slice(&enc);
    Ok(wire)
}
pub fn open(
    keys: &StreamKeys,
    wire: &[u8],
    authorized: &[[u8; 32]],
    now: u64,
) -> Result<OpenedEvent, Error> {
    let env = Envelope::parse(wire)?;
    if env.header.shard != keys.shard() {
        return Err(Error::Authentication);
    }
    open_body(
        keys,
        env.header.class,
        env.body,
        authorized,
        now,
        Some(env.header.expiry),
    )
}
pub fn open_body(
    keys: &StreamKeys,
    class: u8,
    body: &[u8],
    authorized: &[[u8; 32]],
    now: u64,
    visible_expiry: Option<u32>,
) -> Result<OpenedEvent, Error> {
    if class > 3 || body.len() != BODY_LENGTHS[class as usize] {
        return Err(Error::Malformed);
    }
    let salt: [u8; 16] = body[..16].try_into().map_err(|_| Error::Malformed)?;
    let first4 = [1, class, keys.shard(), 0];
    let pt = ChaCha20Poly1305::new((&keys.encryption(&salt)).into())
        .decrypt(
            Nonce::from_slice(&body[16..28]),
            Payload {
                msg: &body[44..],
                aad: &aad(keys, &first4, &body[..44]),
            },
        )
        .map_err(|_| Error::Authentication)?;
    if pt.len() < 110 || pt[0] != 1 || pt[1] != 1 || pt[2..4] != [0, 1] {
        return Err(Error::Malformed);
    }
    let len = u16::from_be_bytes(pt[4..6].try_into().map_err(|_| Error::Malformed)?) as usize;
    let end = 110_usize
        .checked_add(len)
        .filter(|&n| n <= pt.len())
        .ok_or(Error::Malformed)?;
    if pt[end..].iter().any(|&b| b != 0) {
        return Err(Error::Malformed);
    }
    let ev = EventIn {
        payload: pt[110..end].to_vec(),
        schema_version: u16::from_be_bytes(pt[6..8].try_into().map_err(|_| Error::Malformed)?),
        seq: u64::from_be_bytes(pt[8..16].try_into().map_err(|_| Error::Malformed)?),
        lei: pt[16..32].try_into().map_err(|_| Error::Malformed)?,
        schema: pt[32..40].try_into().map_err(|_| Error::Malformed)?,
        key_index: u16::from_be_bytes(pt[40..42].try_into().map_err(|_| Error::Malformed)?),
    };
    let creation = u32::from_be_bytes(pt[42..46].try_into().map_err(|_| Error::Malformed)?);
    let expiry = creation
        .checked_add(LIFETIME as u32)
        .ok_or(Error::Malformed)?;
    if visible_expiry.is_some_and(|e| e != expiry) {
        return Err(Error::Authentication);
    }
    let publisher = *authorized
        .get(ev.key_index as usize)
        .ok_or(Error::Unauthorized)?;
    let vk = VerifyingKey::from_bytes(&publisher).map_err(|_| Error::Unauthorized)?;
    let signature: [u8; 64] = pt[46..110].try_into().map_err(|_| Error::Malformed)?;
    let stmt = statement(keys, &first4, &body[..44], &ev, creation, expiry);
    vk.verify_strict(&stmt, &Signature::from_bytes(&signature))
        .map_err(|_| Error::BadSignature)?;
    if now > u64::from(expiry) {
        return Err(Error::Expired);
    }
    Ok(OpenedEvent {
        event: ev,
        creation,
        expiry,
        publisher,
        signature,
        statement: stmt,
        stream: keys.stream_id(),
    })
}
#[cfg(test)]
mod tests {
    use super::*;
    use crate::wire::MOCK_NETWORK;
    use rand::{RngCore, SeedableRng};
    use rand_chacha::ChaCha20Rng;
    fn fixture() -> (StreamKeys, SigningKey, EventIn, ChaCha20Rng) {
        (
            StreamKeys::new(MOCK_NETWORK, [3; 32], 1).unwrap(),
            SigningKey::from_bytes(&[4; 32]),
            EventIn {
                payload: vec![5; 10],
                lei: [6; 16],
                seq: 1,
                schema: *b"schema01",
                schema_version: 1,
                key_index: 0,
            },
            ChaCha20Rng::seed_from_u64(42),
        )
    }
    #[test]
    fn body_length_per_class() {
        let (k, s, e, mut r) = fixture();
        for c in 0..4 {
            let b = seal(&k, &s, &e, Some(c), 100, &mut r).unwrap();
            assert_eq!(b.len(), HEADER_LEN + BODY_LENGTHS[c as usize]);
            let v = open(&k, &b, &[s.verifying_key().to_bytes()], 100).unwrap();
            assert_eq!(v.event.payload, e.payload);
            assert_eq!(v.expiry, 172900);
        }
    }
    #[test]
    fn equal_wire_length() {
        let (k, s, mut e, mut r) = fixture();
        for c in 0..4 {
            e.payload = vec![1];
            let a = seal(&k, &s, &e, Some(c), 100, &mut r).unwrap();
            e.payload = vec![1; CAPACITIES[c as usize]];
            assert_eq!(
                a.len(),
                seal(&k, &s, &e, Some(c), 100, &mut r).unwrap().len()
            );
        }
    }
    #[test]
    fn too_large() {
        let (k, s, mut e, mut r) = fixture();
        e.payload.resize(16215, 0);
        assert_eq!(seal(&k, &s, &e, None, 100, &mut r), Err(Error::TooLarge));
    }
    #[test]
    fn aad_tamper() {
        let (k, s, e, mut r) = fixture();
        let b = seal(&k, &s, &e, None, 100, &mut r).unwrap();
        for pos in [0, 1, 2, 3, 4, 5, 6, 7, 520, 535, 536, 547, 548, 563, 600] {
            let mut bad = b.clone();
            bad[pos] ^= 1;
            assert!(
                open(&k, &bad, &[s.verifying_key().to_bytes()], 100).is_err(),
                "offset {pos}"
            );
        }
        let mut other = k.clone();
        other.network[0] ^= 1;
        assert!(open(&other, &b, &[s.verifying_key().to_bytes()], 100).is_err());
    }
    #[test]
    fn foreign_profile_fails() {
        let (k, s, e, mut r) = fixture();
        let b = seal(&k, &s, &e, None, 100, &mut r).unwrap();
        let mut other = k.clone();
        other.profile = b"foreign".to_vec();
        assert!(open(&other, &b, &[s.verifying_key().to_bytes()], 100).is_err());
    }
    fn mutate_plaintext(k: &StreamKeys, b: &mut [u8], pos: usize) {
        let salt: [u8; 16] = b[520..536].try_into().unwrap();
        let nonce = b[536..548].to_vec();
        let ad = aad(k, &b[..4], &b[520..564]);
        let cipher = ChaCha20Poly1305::new((&k.encryption(&salt)).into());
        let mut pt = cipher
            .decrypt(
                Nonce::from_slice(&nonce),
                Payload {
                    msg: &b[564..],
                    aad: &ad,
                },
            )
            .unwrap();
        pt[pos] ^= 1;
        let ct = cipher
            .encrypt(Nonce::from_slice(&nonce), Payload { msg: &pt, aad: &ad })
            .unwrap();
        b[564..].copy_from_slice(&ct);
    }
    #[test]
    fn nonzero_pad_discarded() {
        let (k, s, e, mut r) = fixture();
        let mut b = seal(&k, &s, &e, None, 100, &mut r).unwrap();
        mutate_plaintext(&k, &mut b, 120);
        assert!(matches!(
            open(&k, &b, &[s.verifying_key().to_bytes()], 100),
            Err(Error::Malformed)
        ));
    }
    #[test]
    fn statement_field_substitution() {
        let (k, s, e, mut r) = fixture();
        let b = seal(&k, &s, &e, None, 100, &mut r).unwrap();
        for pos in [6, 8, 16, 32, 42, 46, 110] {
            let mut bad = b.clone();
            mutate_plaintext(&k, &mut bad, pos);
            assert!(open(&k, &bad, &[s.verifying_key().to_bytes()], 100).is_err());
        }
        for field in 0..2 {
            let mut other = k.clone();
            if field == 0 {
                other.destination[0] = 1;
            } else {
                other.action[0] = 1;
            }
            assert!(open(&other, &b, &[s.verifying_key().to_bytes()], 100).is_err());
        }
    }
    #[test]
    fn auth_block_layout() {
        let (k, s, e, mut r) = fixture();
        let b = seal(&k, &s, &e, None, 100, &mut r).unwrap();
        let v = open(&k, &b, &[s.verifying_key().to_bytes()], 100).unwrap();
        assert_eq!(v.creation, 100);
        assert_eq!(v.event.key_index, 0);
        assert_eq!(v.signature.len(), 64);
        for c in 0..4 {
            assert_eq!(CAPACITIES[c], BODY_LENGTHS[c] - 170);
        }
    }
    #[test]
    fn recognition_survives_seq_gaps() {
        let (k, s, mut e, mut r) = fixture();
        for seq in [1, 7, 1000] {
            e.seq = seq;
            let b = seal(&k, &s, &e, None, 100, &mut r).unwrap();
            assert!(crate::keys::matches(
                &k.recognition(),
                &k.network,
                &b[520..]
            ));
            assert_eq!(
                open(&k, &b, &[s.verifying_key().to_bytes()], 100)
                    .unwrap()
                    .event
                    .seq,
                seq
            );
        }
    }
    #[test]
    fn no_key_nonce_reuse() {
        let (k, _, _, mut r) = fixture();
        let mut seen = std::collections::HashSet::new();
        for _ in 0..100_000 {
            let mut salt = [0; 16];
            let mut nonce = [0; 12];
            r.fill_bytes(&mut salt);
            r.fill_bytes(&mut nonce);
            assert!(seen.insert((k.encryption(&salt), nonce)));
        }
    }
    #[test]
    fn vectors_written() {
        let (k, s, mut e, mut r) = fixture();
        for c in 0..4 {
            e.payload = vec![5; CAPACITIES[c as usize]];
            let b = seal(&k, &s, &e, Some(c), 100, &mut r).unwrap();
            let path = format!("{}/vectors/class{c}.json", env!("CARGO_MANIFEST_DIR"));
            let v = serde_json::json!({"class":c,"network":crate::wire::hex(&k.network),"secret":crate::wire::hex(&k.secret),"publisher":crate::wire::hex(&s.verifying_key().to_bytes()),"wire":crate::wire::hex(&b),"eid":crate::wire::hex(&crate::wire::eid(&k.network,&b).unwrap()),"payload_capacity":CAPACITIES[c as usize]});
            std::fs::write(path, serde_json::to_string_pretty(&v).unwrap()).unwrap();
        }
    }
}
