use crate::wire::{hash, Eid, Error, LIFETIME};
use serde::{Deserialize, Serialize};
pub fn merkle_root(leaves: &[Eid]) -> Eid {
    match leaves.len() {
        0 => hash(&[b""]),
        1 => hash(&[&[0], &leaves[0]]),
        n => {
            let k = split(n);
            hash(&[&[1], &merkle_root(&leaves[..k]), &merkle_root(&leaves[k..])])
        }
    }
}
fn split(n: usize) -> usize {
    1 << ((usize::BITS - 1) - (n - 1).leading_zeros())
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct MerklePath {
    pub index: usize,
    pub count: usize,
    pub siblings: Vec<Eid>,
}
pub fn path(leaves: &[Eid], index: usize) -> Result<MerklePath, Error> {
    if index >= leaves.len() {
        return Err(Error::Refused);
    }
    fn walk(leaves: &[Eid], index: usize, out: &mut Vec<Eid>) {
        if leaves.len() <= 1 {
            return;
        }
        let k = split(leaves.len());
        if index < k {
            walk(&leaves[..k], index, out);
            out.push(merkle_root(&leaves[k..]));
        } else {
            walk(&leaves[k..], index - k, out);
            out.push(merkle_root(&leaves[..k]));
        }
    }
    let mut siblings = vec![];
    walk(leaves, index, &mut siblings);
    Ok(MerklePath {
        index,
        count: leaves.len(),
        siblings,
    })
}
impl MerklePath {
    pub fn verify(&self, leaf: &Eid, root: &Eid) -> bool {
        if self.count == 0 || self.index >= self.count || self.siblings.len() > 64 {
            return false;
        }
        fn shape(n: usize, i: usize, out: &mut Vec<bool>) {
            if n <= 1 {
                return;
            }
            let k = split(n);
            if i < k {
                shape(k, i, out);
                out.push(false);
            } else {
                shape(n - k, i - k, out);
                out.push(true);
            }
        }
        let mut sides = vec![];
        shape(self.count, self.index, &mut sides);
        if sides.len() != self.siblings.len() {
            return false;
        }
        let mut h = hash(&[&[0], leaf]);
        for (left, sibling) in sides.into_iter().zip(&self.siblings) {
            h = if left {
                hash(&[&[1], sibling, &h])
            } else {
                hash(&[&[1], &h, sibling])
            };
        }
        h == *root
    }
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct AnchorPayload {
    pub window: u64,
    pub root: Eid,
    pub counts: Vec<u32>,
}
impl AnchorPayload {
    pub fn encode(&self) -> Result<Vec<u8>, Error> {
        if !(1..=8).contains(&self.counts.len()) {
            return Err(Error::Malformed);
        }
        let mut b = self.window.to_be_bytes().to_vec();
        b.extend_from_slice(&self.root);
        for count in &self.counts {
            b.extend_from_slice(&count.to_be_bytes());
        }
        Ok(b)
    }
    pub fn decode(b: &[u8]) -> Result<Self, Error> {
        if b.len() < 44 || b.len() > 72 || !(b.len() - 40).is_multiple_of(4) {
            return Err(Error::Malformed);
        }
        let window = u64::from_be_bytes(b[..8].try_into().map_err(|_| Error::Malformed)?);
        let root = b[8..40].try_into().map_err(|_| Error::Malformed)?;
        let counts = b[40..]
            .as_chunks::<4>()
            .0
            .iter()
            .map(|c| u32::from_be_bytes([c[0], c[1], c[2], c[3]]))
            .collect();
        Ok(Self {
            window,
            root,
            counts,
        })
    }
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct InclusionProof {
    pub window: u64,
    pub shard: u8,
    pub batch_root: Eid,
    pub batch_path: MerklePath,
    pub window_path: MerklePath,
}
impl InclusionProof {
    pub fn verify(&self, eid: &Eid, anchor: &AnchorPayload) -> bool {
        anchor.window == self.window
            && anchor
                .counts
                .get(self.shard as usize)
                .is_some_and(|&n| n as usize == self.batch_path.count)
            && self.window_path.index == self.shard as usize
            && self.window_path.count == anchor.counts.len()
            && self.batch_path.verify(eid, &self.batch_root)
            && self.window_path.verify(&self.batch_root, &anchor.root)
    }
}
pub struct Batch {
    pub payload: AnchorPayload,
    pub leaves: Vec<Vec<Eid>>,
    pub roots: Vec<Eid>,
}
impl Batch {
    pub fn new(window: u64, mut shards: Vec<Vec<Eid>>) -> Result<Self, Error> {
        if !(1..=8).contains(&shards.len()) {
            return Err(Error::Malformed);
        }
        for list in &mut shards {
            list.sort_unstable();
            list.dedup();
        }
        let roots: Vec<_> = shards.iter().map(|s| merkle_root(s)).collect();
        let payload = AnchorPayload {
            window,
            root: merkle_root(&roots),
            counts: shards.iter().map(|s| s.len() as u32).collect(),
        };
        Ok(Self {
            payload,
            leaves: shards,
            roots,
        })
    }
    pub fn inclusion(&self, eid: &Eid) -> Result<InclusionProof, Error> {
        for (shard, list) in self.leaves.iter().enumerate() {
            if let Ok(index) = list.binary_search(eid) {
                return Ok(InclusionProof {
                    window: self.payload.window,
                    shard: shard as u8,
                    batch_root: self.roots[shard],
                    batch_path: path(list, index)?,
                    window_path: path(&self.roots, shard)?,
                });
            }
        }
        Err(Error::Refused)
    }
}
pub fn window(expiry: u32) -> u64 {
    u64::from(expiry).saturating_sub(LIFETIME) / 60
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn rfc6962_vectors() {
        assert_eq!(merkle_root(&[]), hash(&[b""]));
        assert_eq!(merkle_root(&[[1; 32]]), hash(&[&[0], &[1; 32]]));
        assert_eq!(
            merkle_root(&[[1; 32], [2; 32]]),
            hash(&[&[1], &hash(&[&[0], &[1; 32]]), &hash(&[&[0], &[2; 32]])])
        );
    }
    #[test]
    fn independent_merkle_roots() {
        fn independent(leaves: &[Eid]) -> Eid {
            if leaves.is_empty() {
                return hash(&[b""]);
            }
            let mut levels: Vec<Option<Eid>> = vec![];
            for leaf in leaves {
                let mut h = hash(&[&[0], leaf]);
                let mut level = 0;
                loop {
                    if level == levels.len() {
                        levels.push(Some(h));
                        break;
                    }
                    if let Some(left) = levels[level].take() {
                        h = hash(&[&[1], &left, &h]);
                        level += 1;
                    } else {
                        levels[level] = Some(h);
                        break;
                    }
                }
            }
            let mut root: Option<Eid> = None;
            for node in levels.into_iter().flatten() {
                root = Some(match root {
                    None => node,
                    Some(right) => hash(&[&[1], &node, &right]),
                });
            }
            root.unwrap()
        }
        for n in 0..70 {
            let leaves: Vec<_> = (0..n).map(|i| hash(&[&(i as u64).to_be_bytes()])).collect();
            assert_eq!(merkle_root(&leaves), independent(&leaves));
        }
    }
    #[test]
    fn paths_verify() {
        for n in 1..40 {
            let leaves: Vec<_> = (0..n).map(|i| hash(&[&(i as u64).to_be_bytes()])).collect();
            let batch = Batch::new(1, vec![leaves.clone(), vec![]]).unwrap();
            for id in leaves {
                let p = batch.inclusion(&id).unwrap();
                assert!(p.verify(&id, &batch.payload));
                assert!(!p.verify(&[0; 32], &batch.payload));
            }
            assert!(batch.inclusion(&[0; 32]).is_err());
        }
    }
    #[test]
    fn payload_vectors() {
        for n in [1, 8] {
            let p = AnchorPayload {
                window: 0x0102030405060708,
                root: [9; 32],
                counts: vec![2; n],
            };
            let b = p.encode().unwrap();
            assert_eq!(b.len(), 40 + n * 4);
            let decoded = AnchorPayload::decode(&b).unwrap();
            assert_eq!(decoded.root, p.root);
            assert_eq!(decoded.window, p.window);
            assert_eq!(decoded.counts, p.counts);
        }
        assert!(AnchorPayload::decode(&[0; 43]).is_err());
    }
}
