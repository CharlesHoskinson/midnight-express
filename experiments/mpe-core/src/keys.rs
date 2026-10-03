use crate::wire::{hash, Error, NetworkId};
use hkdf::Hkdf;
use hmac::{Hmac, Mac};
use rand::{CryptoRng, RngCore};
use sha2::Sha256;
pub const PROFILE: &[u8] = b"mpe-v1-sym";
pub trait CryptoRngCore: CryptoRng + RngCore {}
impl<T: CryptoRng + RngCore> CryptoRngCore for T {}
#[derive(Clone)]
pub struct StreamKeys {
    pub network: NetworkId,
    pub secret: [u8; 32],
    pub profile: Vec<u8>,
    pub shards: u8,
    pub destination: [u8; 32],
    pub action: [u8; 32],
}
impl StreamKeys {
    pub fn new(network: NetworkId, secret: [u8; 32], shards: u8) -> Result<Self, Error> {
        if !(1..=8).contains(&shards) {
            return Err(Error::Malformed);
        }
        Ok(Self {
            network,
            secret,
            profile: PROFILE.to_vec(),
            shards,
            destination: [0; 32],
            action: [0; 32],
        })
    }
    pub fn random(
        network: NetworkId,
        shards: u8,
        rng: &mut dyn CryptoRngCore,
    ) -> Result<Self, Error> {
        let mut s = [0; 32];
        rng.try_fill_bytes(&mut s)
            .map_err(|_| Error::RandomnessUnavailable)?;
        Self::new(network, s, shards)
    }
    pub fn create(network: NetworkId, shards: u8) -> Result<Self, Error> {
        Self::random(network, shards, &mut rand::rngs::OsRng)
    }
    fn derive(&self, salt: &[u8], info: &[u8]) -> [u8; 32] {
        let hk = Hkdf::<Sha256>::new(Some(salt), &self.secret);
        let mut out = [0; 32];
        // Fixed 32-byte expansion is below the RFC5869 bound for SHA256.
        if hk.expand(info, &mut out).is_err() {
            return [0; 32];
        }
        out
    }
    pub fn recognition(&self) -> [u8; 32] {
        self.derive(
            &self.network,
            &[b"mpe/v1/rec".as_slice(), &self.profile].concat(),
        )
    }
    pub fn encryption(&self, salt: &[u8; 16]) -> [u8; 32] {
        self.derive(
            salt,
            &[b"mpe/v1/enc".as_slice(), &self.network, &self.profile].concat(),
        )
    }
    pub fn stream_id(&self) -> [u8; 32] {
        hash(&[b"mpe/v1/stream", &self.secret])
    }
    pub fn shard(&self) -> u8 {
        let h = hash(&[b"mpe/v1/shard", &self.secret]);
        let mut n = [0; 8];
        n.copy_from_slice(&h[..8]);
        (u64::from_be_bytes(n) % u64::from(self.shards)) as u8
    }
    pub fn event_secret(&self, lei: &[u8; 16]) -> [u8; 32] {
        self.derive(&self.network, &[b"mpe/v1/event".as_slice(), lei].concat())
    }
}
pub fn tag(rec: &[u8; 32], network: &NetworkId, salt: &[u8; 16]) -> [u8; 16] {
    let Ok(mut mac) = Hmac::<Sha256>::new_from_slice(rec) else {
        return [0; 16];
    };
    mac.update(b"mpe/v1/tag");
    mac.update(network);
    mac.update(salt);
    let bytes = mac.finalize().into_bytes();
    let mut t = [0; 16];
    t.copy_from_slice(&bytes[..16]);
    t
}
pub fn matches(rec: &[u8; 32], network: &NetworkId, body: &[u8]) -> bool {
    if body.len() < 44 {
        return false;
    }
    let Ok(mut mac) = Hmac::<Sha256>::new_from_slice(rec) else {
        return false;
    };
    mac.update(b"mpe/v1/tag");
    mac.update(network);
    mac.update(&body[..16]);
    mac.verify_truncated_left(&body[28..44]).is_ok()
}
#[cfg(test)]
mod tests {
    use super::*;
    use crate::wire::MOCK_NETWORK;
    #[test]
    fn primitive_vectors() {
        let hk = Hkdf::<Sha256>::new(
            Some(&[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]),
            &[0x0b; 22],
        );
        let mut okm = [0; 42];
        hk.expand(
            &[0xf0, 0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8, 0xf9],
            &mut okm,
        )
        .unwrap();
        assert_eq!(
            crate::wire::hex(&okm),
            "3cb25f25faacd57a90434f64d0362f2a2d2d0a90cf1a5a4c5db02d56ecc4c5bf34007208d5b887185865"
        );
        let mut mac = Hmac::<Sha256>::new_from_slice(&[0x0b; 20]).unwrap();
        mac.update(b"Hi There");
        assert_eq!(
            crate::wire::hex(&mac.finalize().into_bytes()),
            "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7"
        );
    }
    struct Failed;
    impl CryptoRng for Failed {}
    impl RngCore for Failed {
        fn next_u32(&mut self) -> u32 {
            0
        }
        fn next_u64(&mut self) -> u64 {
            0
        }
        fn fill_bytes(&mut self, _: &mut [u8]) {}
        fn try_fill_bytes(&mut self, _: &mut [u8]) -> Result<(), rand::Error> {
            Err(rand::Error::new("fixture failure"))
        }
    }
    #[test]
    fn rng_failure() {
        assert!(matches!(
            StreamKeys::random(MOCK_NETWORK, 1, &mut Failed),
            Err(Error::RandomnessUnavailable)
        ));
    }
    #[test]
    fn shard_vectors() {
        for n in 0_u32..1000 {
            let mut s = [0; 32];
            s[..4].copy_from_slice(&n.to_be_bytes());
            assert_eq!(StreamKeys::new(MOCK_NETWORK, s, 1).unwrap().shard(), 0);
            let h = hash(&[b"mpe/v1/shard", &s]);
            let k = StreamKeys::new(MOCK_NETWORK, s, 8).unwrap();
            assert_eq!(k.shard(), h[7] & 7);
        }
    }
    #[test]
    fn salted_tag_and_profile_separation() {
        let k = StreamKeys::new(MOCK_NETWORK, [7; 32], 1).unwrap();
        let a = tag(&k.recognition(), &k.network, &[1; 16]);
        let b = tag(&k.recognition(), &k.network, &[2; 16]);
        assert_ne!(a, b);
        let mut other = k.clone();
        other.profile = b"other".to_vec();
        assert_ne!(k.recognition(), other.recognition());
    }
}

#[cfg(test)]
mod rfc_vectors {
    use chacha20poly1305::{
        aead::{Aead, KeyInit, Payload},
        ChaCha20Poly1305, Nonce,
    };
    use ed25519_dalek::{Signer, SigningKey};
    fn unhex(s: &str) -> Vec<u8> {
        s.as_bytes()
            .as_chunks::<2>()
            .0
            .iter()
            .map(|p| u8::from_str_radix(std::str::from_utf8(p).unwrap(), 16).unwrap())
            .collect()
    }
    #[test]
    fn rfc8032_empty_message() {
        let seed: [u8; 32] =
            unhex("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")
                .try_into()
                .unwrap();
        let s = SigningKey::from_bytes(&seed);
        assert_eq!(
            crate::wire::hex(&s.verifying_key().to_bytes()),
            "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a"
        );
        assert_eq!(crate::wire::hex(&s.sign(b"").to_bytes()),"e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b");
    }
    #[test]
    fn rfc8439_aead() {
        let key: Vec<u8> = (0x80..=0x9f).collect();
        let nonce = unhex("070000004041424344454647");
        let aad = unhex("50515253c0c1c2c3c4c5c6c7");
        let plain=b"Ladies and Gentlemen of the class of '99: If I could offer you only one tip for the future, sunscreen would be it.";
        let cipher = ChaCha20Poly1305::new_from_slice(&key).unwrap();
        let ct = cipher
            .encrypt(
                Nonce::from_slice(&nonce),
                Payload {
                    msg: plain,
                    aad: &aad,
                },
            )
            .unwrap();
        assert_eq!(crate::wire::hex(&ct),"d31a8d34648e60db7b86afbc53ef7ec2a4aded51296e08fea9e2b5a736ee62d63dbea45e8ca9671282fafb69da92728b1a71de0a9e060b2905d6a5b67ecd3b3692ddbd7f2d778b8c9803aee328091b58fab324e4fad675945585808b4831d7bc3ff4def08e4b7a9de576d26586cec64b61161ae10b594f09e26a7e902ecbd0600691");
    }
}
