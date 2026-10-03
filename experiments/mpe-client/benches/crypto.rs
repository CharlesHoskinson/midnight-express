use criterion::{criterion_group, criterion_main, Criterion};
use ed25519_dalek::{Signer, SigningKey};
use mpe_core::{
    keys::{matches, StreamKeys},
    seal::{open, seal, EventIn},
    wire::MOCK_NETWORK,
};
use rand::{RngCore, SeedableRng};
use rand_chacha::ChaCha20Rng;
use std::hint::black_box;
fn benches(c: &mut Criterion) {
    let mut rng = ChaCha20Rng::seed_from_u64(42);
    let mut ring = vec![];
    for _ in 0..32 {
        let mut s = [0; 32];
        rng.fill_bytes(&mut s);
        ring.push(StreamKeys::new(MOCK_NETWORK, s, 1).unwrap());
    }
    let key = &ring[0];
    let signer = SigningKey::from_bytes(&[7; 32]);
    let event = EventIn {
        payload: vec![1; 3926],
        lei: [8; 16],
        seq: 1,
        schema: [9; 8],
        schema_version: 1,
        key_index: 0,
    };
    let b = seal(key, &signer, &event, Some(2), 100, &mut rng).unwrap();
    let pubkey = signer.verifying_key().to_bytes();
    c.bench_function("seal_class2", |bench| {
        bench.iter(|| seal(key, &signer, black_box(&event), Some(2), 100, &mut rng).unwrap())
    });
    c.bench_function("open_class2", |bench| {
        bench.iter(|| open(key, black_box(&b), &[pubkey], 100).unwrap())
    });
    c.bench_function("recognition_32_keys_class2", |bench| {
        bench.iter(|| {
            for key in &ring {
                black_box(matches(
                    &key.recognition(),
                    &key.network,
                    black_box(&b[520..]),
                ));
            }
        })
    });
    c.bench_function("tag", |bench| {
        bench.iter(|| matches(&key.recognition(), &key.network, black_box(&b[520..])))
    });
    let statement = b"benchmark statement";
    let signature = signer.sign(statement);
    let vk = signer.verifying_key();
    c.bench_function("sign", |bench| {
        bench.iter(|| signer.sign(black_box(statement)))
    });
    c.bench_function("verify", |bench| {
        bench.iter(|| vk.verify_strict(black_box(statement), &signature).unwrap())
    });
}
criterion_group! {name=crypto;config=Criterion::default().sample_size(20).warm_up_time(std::time::Duration::from_secs(1)).measurement_time(std::time::Duration::from_secs(2));targets=benches}
criterion_main!(crypto);
