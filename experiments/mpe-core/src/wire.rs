use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

pub type Eid = [u8; 32];
pub type NetworkId = [u8; 32];
pub const HEADER_LEN: usize = 520;
pub const SLOT_LEN: usize = 512;
pub const BODY_LENGTHS: [usize; 4] = [256, 1024, 4096, 16384];
pub const CAPACITIES: [usize; 4] = [86, 854, 3926, 16214];
pub const LIFETIME: u64 = 172_800;
pub const CLOCK_TOLERANCE: u64 = 60;
pub const MOCK_NETWORK: NetworkId = [0x4d; 32];

#[derive(Debug, Clone, Copy, PartialEq, Eq, thiserror::Error)]
pub enum Error {
    #[error("malformed canonical encoding")]
    Malformed,
    #[error("payload too large")]
    TooLarge,
    #[error("authentication failed")]
    Authentication,
    #[error("unauthorized publisher")]
    Unauthorized,
    #[error("invalid publisher signature")]
    BadSignature,
    #[error("expired event")]
    Expired,
    #[error("randomness unavailable")]
    RandomnessUnavailable,
    #[error("invalid admission proof")]
    InvalidAdmission,
    #[error("unknown root")]
    UnknownRoot,
    #[error("quota exhausted")]
    OverQuota,
    #[error("storage exhausted")]
    StorageExhausted,
    #[error("request refused")]
    Refused,
}
pub type WireError = Error;
pub fn class_for(len: usize) -> Result<u8, Error> {
    CAPACITIES
        .iter()
        .position(|&cap| len <= cap)
        .map(|c| c as u8)
        .ok_or(Error::TooLarge)
}
pub fn hash(parts: &[&[u8]]) -> [u8; 32] {
    let mut h = Sha256::new();
    for part in parts {
        h.update(part);
    }
    h.finalize().into()
}
pub fn hex(bytes: &[u8]) -> String {
    bytes.iter().map(|b| format!("{b:02x}")).collect()
}
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Header {
    pub version: u8,
    pub class: u8,
    pub shard: u8,
    pub expiry: u32,
}
impl Header {
    pub fn encode(self) -> [u8; 8] {
        let mut b = [self.version, self.class, self.shard, 0, 0, 0, 0, 0];
        b[4..8].copy_from_slice(&self.expiry.to_be_bytes());
        b
    }
    pub fn parse(bytes: &[u8]) -> Result<Self, Error> {
        let b = bytes.get(..8).ok_or(Error::Malformed)?;
        if b[0] != 1 || b[1] > 3 || b[3] != 0 {
            return Err(Error::Malformed);
        }
        let expiry = u32::from_be_bytes(b[4..8].try_into().map_err(|_| Error::Malformed)?);
        Ok(Self {
            version: b[0],
            class: b[1],
            shard: b[2],
            expiry,
        })
    }
    pub fn wire_len(self) -> usize {
        HEADER_LEN + BODY_LENGTHS.get(self.class as usize).copied().unwrap_or(0)
    }
}
#[derive(Debug)]
pub struct Envelope<'a> {
    pub header: Header,
    pub slot: &'a [u8],
    pub body: &'a [u8],
}
impl<'a> Envelope<'a> {
    pub fn parse(bytes: &'a [u8]) -> Result<Self, Error> {
        let header = Header::parse(bytes)?;
        if bytes.len() != header.wire_len() {
            return Err(Error::Malformed);
        }
        Ok(Self {
            header,
            slot: &bytes[8..HEADER_LEN],
            body: &bytes[HEADER_LEN..],
        })
    }
    pub fn encode(&self) -> Vec<u8> {
        let mut b = self.header.encode().to_vec();
        b.extend_from_slice(self.slot);
        b.extend_from_slice(self.body);
        b
    }
    pub fn eid(&self, network: &NetworkId) -> Eid {
        hash(&[
            b"midnight-pe/id/v1",
            network,
            &self.header.encode(),
            self.body,
        ])
    }
}
pub fn eid(network: &NetworkId, bytes: &[u8]) -> Result<Eid, Error> {
    Ok(Envelope::parse(bytes)?.eid(network))
}
pub fn message_id(bytes: &[u8]) -> [u8; 32] {
    hash(&[b"mpe/v1/msgid", bytes])
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn class_edges() {
        for (len, class) in [
            (86, 0),
            (87, 1),
            (854, 1),
            (855, 2),
            (3926, 2),
            (3927, 3),
            (16214, 3),
        ] {
            assert_eq!(class_for(len), Ok(class));
        }
        assert_eq!(class_for(16215), Err(Error::TooLarge));
    }
    #[test]
    fn eid_ignores_slot() {
        let h = Header {
            version: 1,
            class: 0,
            shard: 0,
            expiry: 0x01020304,
        };
        let mut b = h.encode().to_vec();
        b.resize(776, 0);
        let old = eid(&MOCK_NETWORK, &b).unwrap();
        let mid = message_id(&b);
        b[112] = 1;
        assert_eq!(eid(&MOCK_NETWORK, &b).unwrap(), old);
        assert_ne!(message_id(&b), mid);
        b[700] = 1;
        assert_ne!(eid(&MOCK_NETWORK, &b).unwrap(), old);
        assert_eq!(&b[4..8], &[1, 2, 3, 4]);
    }
    #[test]
    fn vectors_roundtrip() {
        for c in 0..4 {
            let h = Header {
                version: 1,
                class: c,
                shard: 0,
                expiry: 123,
            };
            let mut b = h.encode().to_vec();
            b.resize(h.wire_len(), 0);
            assert_eq!(Envelope::parse(&b).unwrap().encode(), b);
        }
    }
    proptest::proptest! { #[test] fn arbitrary_input_never_panics(b in proptest::collection::vec(proptest::prelude::any::<u8>(),0..20000)) { let _=Envelope::parse(&b); } }
}
