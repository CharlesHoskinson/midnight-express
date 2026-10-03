use sha2::{Digest, Sha256};
fn unhex(s: &str) -> Vec<u8> {
    assert_eq!(s.len() % 2, 0);
    s.as_bytes()
        .as_chunks::<2>()
        .0
        .iter()
        .map(|p| u8::from_str_radix(std::str::from_utf8(p).unwrap(), 16).unwrap())
        .collect()
}
#[test]
fn fixed_offsets_independent_decoder() {
    for class in 0..4 {
        let path = format!("{}/vectors/class{class}.json", env!("CARGO_MANIFEST_DIR"));
        let v: serde_json::Value = serde_json::from_slice(&std::fs::read(path).unwrap()).unwrap();
        let b = unhex(v["wire"].as_str().unwrap());
        let network = unhex(v["network"].as_str().unwrap());
        assert_eq!(b[0], 1);
        assert_eq!(b[1], class);
        assert_eq!(b[2], 0);
        assert_eq!(b[3], 0);
        assert_eq!(b.len(), 520 + [256, 1024, 4096, 16384][class as usize]);
        assert_eq!(u32::from_be_bytes(b[4..8].try_into().unwrap()), 172900);
        assert!(b[368..520].iter().all(|&b| b == 0));
        assert_eq!(b[520..536].len(), 16);
        assert_eq!(b[536..548].len(), 12);
        assert_eq!(b[548..564].len(), 16);
        let mut h = Sha256::new();
        h.update(b"midnight-pe/id/v1");
        h.update(network);
        h.update(&b[..8]);
        h.update(&b[520..]);
        assert_eq!(&h.finalize()[..], unhex(v["eid"].as_str().unwrap()));
    }
}
