use libp2p::identity;
use mpe_core::{
    admission::{Member, RegistryView, RootRecord, StandInRln},
    clock::{Clock, SimClock},
    validator::Outcome,
    wire::{Header, LIFETIME, MOCK_NETWORK},
};
use mpe_node::{
    config::MeshConfig,
    node::{self, NodeHandle, NodeOptions},
    protocols::{Capture, Request, Response},
};
use std::{collections::HashSet, sync::Arc, time::Duration};
use tokio::sync::Semaphore;
async fn fixture(
    n: usize,
) -> (
    Vec<NodeHandle>,
    Arc<StandInRln>,
    Arc<SimClock>,
    Vec<tokio::task::JoinHandle<()>>,
) {
    fixture_with_heartbeat(n, Duration::from_secs(1)).await
}
async fn fixture_with_heartbeat(
    n: usize,
    interval: Duration,
) -> (
    Vec<NodeHandle>,
    Arc<StandInRln>,
    Arc<SimClock>,
    Vec<tokio::task::JoinHandle<()>>,
) {
    fixture_with_gate(n, interval, Arc::new(Semaphore::new(4))).await
}
async fn fixture_with_gate(
    n: usize,
    interval: Duration,
    gate: Arc<Semaphore>,
) -> (
    Vec<NodeHandle>,
    Arc<StandInRln>,
    Arc<SimClock>,
    Vec<tokio::task::JoinHandle<()>>,
) {
    let clock = Arc::new(SimClock::new(1_800_000_000));
    let p = Arc::new(StandInRln::new(vec![Member::new([7; 32])]));
    let keys: Vec<_> = (0..n)
        .map(|_| identity::Keypair::generate_ed25519())
        .collect();
    let peers: HashSet<_> = keys.iter().map(|k| k.public().to_peer_id()).collect();
    let mut handles = vec![];
    let mut tasks = vec![];
    for key in keys {
        let view = RegistryView {
            network: MOCK_NETWORK,
            roots: vec![RootRecord {
                root: [1; 32],
                period_start: clock.now(),
                published_at: clock.now() + 1,
                superseded_at: None,
            }],
            finalized_time: clock.now(),
            shards: 1,
            bus_paused: false,
        };
        let (h, t) = node::start(NodeOptions {
            key,
            proof: p.clone(),
            view,
            clock: clock.clone(),
            mesh: MeshConfig::default(),
            subscribe: true,
            open: false,
            allowlist: peers.clone(),
            withholding: false,
            heartbeat_interval: interval,
            verify_cost_us: 0,
            global_verify: gate.clone(),
            capture: Capture::default(),
        })
        .await
        .unwrap();
        handles.push(h);
        tasks.push(t);
    }
    for i in 0..n {
        for j in 0..i {
            handles[i].dial(handles[j].address.clone()).await.unwrap();
        }
    }
    tokio::time::sleep(Duration::from_secs(3)).await;
    (handles, p, clock, tasks)
}
fn envelope(p: &StandInRln, clock: &dyn Clock, index: u16) -> Vec<u8> {
    let now = clock.now();
    let mut b = Header {
        version: 1,
        class: 0,
        shard: 0,
        expiry: (now + LIFETIME) as u32,
    }
    .encode()
    .to_vec();
    b.resize(776, 0);
    b[700..702].copy_from_slice(&index.to_be_bytes());
    p.attach(&mut b, 0, index % 64, now / 60, MOCK_NETWORK, [1; 32])
        .unwrap();
    b
}
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn tcp_noise_yamux_eight_nodes_forward_and_feed() {
    let (h, p, clock, tasks) = fixture(8).await;
    for i in 0..30 {
        let b = envelope(&p, &*clock, i);
        assert!(matches!(
            h[0].inject(b, 0, false).await.unwrap(),
            Outcome::Accept(_)
        ));
        tokio::time::sleep(Duration::from_millis(100)).await;
    }
    tokio::time::sleep(Duration::from_secs(2)).await;
    for node in &h {
        assert_eq!(node.accepted_since(0).len(), 30);
        let stats = node.stats.lock().unwrap();
        assert!(!stats.scores.is_empty());
        assert!(stats.scores.values().all(|s| *s >= 0.));
        assert!(node.counters.snapshot().0 > 0);
        let capture = node.capture.stats.lock().unwrap();
        assert_eq!(capture.signed_messages, 0);
    }
    let response = h[1]
        .request(h[2].peer, Request::Feed { shard: 0, after: 0 })
        .await
        .unwrap();
    match response {
        Response::Feed { cursor, envelopes } => {
            assert_eq!(cursor, 30);
            assert_eq!(envelopes.len(), 30);
        }
        _ => panic!("wrong response"),
    }
    for node in &h {
        node.stop().await;
    }
    for t in tasks {
        t.await.unwrap();
    }
}
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn corrupted_slot_front_run() {
    let (h, p, clock, tasks) = fixture(8).await;
    let b = envelope(&p, &*clock, 0);
    let mut bad = b.clone();
    bad[112] ^= 1;
    h[0].inject(bad, 0, true).await.unwrap();
    tokio::time::sleep(Duration::from_millis(200)).await;
    assert!(matches!(
        h[0].inject(b, 0, false).await.unwrap(),
        Outcome::Accept(_)
    ));
    tokio::time::sleep(Duration::from_secs(2)).await;
    for node in &h {
        assert_eq!(node.accepted_since(0).len(), 1);
    }
    for node in &h {
        node.stop().await;
    }
    for t in tasks {
        t.await.unwrap();
    }
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn distributed_equivocation_exposes_aggregate_gap() {
    let (h, p, clock, tasks) = fixture(8).await;
    let now = clock.now();
    let mut a = Header {
        version: 1,
        class: 3,
        shard: 0,
        expiry: (now + LIFETIME) as u32,
    }
    .encode()
    .to_vec();
    a.resize(16904, 0);
    let mut b = a.clone();
    b[700] = 1;
    p.attach(&mut a, 0, 0, now / 60, MOCK_NETWORK, [1; 32])
        .unwrap();
    p.attach(&mut b, 0, 0, now / 60, MOCK_NETWORK, [1; 32])
        .unwrap();
    let (a_out, b_out) = tokio::join!(h[0].inject(a, 0, false), h[1].inject(b, 0, false));
    assert!(matches!(a_out.unwrap(), Outcome::Accept(_)));
    assert!(matches!(b_out.unwrap(), Outcome::Accept(_)));
    tokio::time::sleep(Duration::from_secs(2)).await;
    let union: HashSet<_> = h
        .iter()
        .flat_map(|n| n.accepted_since(0))
        .map(|a| a.eid)
        .collect();
    assert_eq!(union.len(),2,"Two different EIDs consume the same class-3 allowance at racing ingress nodes; MPE-ECO-022 is not proved.");
    for node in &h {
        node.stop().await;
    }
    for t in tasks {
        t.await.unwrap();
    }
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn member_out_of_range_publish_rejected_without_anchorer_panic() {
    let (h, p, clock, tasks) = fixture(3).await;
    let ledger = Arc::new(mpe_core::ledger::MockLedger::new(
        MOCK_NETWORK,
        clock.now(),
        vec![],
        vec![],
        1,
    ));
    h[0].enable_anchoring(ledger).await;
    let mut b = envelope(&p, &*clock, 0);
    b[2] = 7;
    p.attach(&mut b, 0, 0, clock.now() / 60, MOCK_NETWORK, [1; 32])
        .unwrap();
    let reply = h[1].request(h[0].peer, Request::Publish(b)).await;
    assert!(matches!(reply, Ok(Response::Refused)), "{reply:?}");
    clock.advance(100);
    tokio::time::sleep(Duration::from_secs(2)).await;
    assert!(!h[0].is_stopped());
    assert!(h[0].accepted_since(0).is_empty());
    assert_eq!(
        h[0].stats.lock().unwrap().outcomes.get("Reject:Shard"),
        Some(&1)
    );
    for node in &h {
        node.stop().await;
    }
    for t in tasks {
        t.await.unwrap();
    }
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn withholding_mesh_peer_pruned_and_score_held_for_backoff() {
    let (h, p, clock, tasks) = fixture_with_heartbeat(8, Duration::from_millis(25)).await;
    h[1].withhold(true).await;
    for i in 0..300_u16 {
        if i % 60 == 0 {
            clock.advance(60);
        }
        let b = envelope(&p, &*clock, i);
        let _ = h[0].inject(b, 0, false).await.unwrap();
        tokio::time::sleep(Duration::from_millis(35)).await;
    }
    tokio::time::sleep(Duration::from_secs(2)).await;
    let pruned = h
        .iter()
        .enumerate()
        .filter(|(i, _)| *i != 0 && *i != 1)
        .filter(|(_, node)| {
            let s = node.stats.lock().unwrap();
            s.scores.get(&h[1].peer).is_some_and(|score| *score < 0.)
                && !s.mesh.contains(&h[1].peer)
        })
        .count();
    assert!(
        pruned > 0,
        "silent peer must leave at least one loaded honest mesh"
    );
    assert!(h[2].stats.lock().unwrap().v12_peers > 0);
    for node in &h {
        node.stop().await;
    }
    for t in tasks {
        t.await.unwrap();
    }
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn closed_verifier_gate_completes_every_job_as_busy() {
    let gate = Arc::new(Semaphore::new(0));
    gate.close();
    let (h, p, clock, tasks) = fixture_with_gate(3, Duration::from_millis(20), gate).await;
    for i in 0..2 {
        let out = tokio::time::timeout(
            Duration::from_secs(1),
            h[0].inject(envelope(&p, &*clock, i), 0, false),
        )
        .await
        .unwrap()
        .unwrap();
        assert_eq!(
            out,
            Outcome::Ignore(mpe_core::validator::IgnoreReason::Busy)
        );
    }
    for node in &h {
        node.stop().await;
    }
    for t in tasks {
        t.await.unwrap();
    }
}
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn full_publish_queue_answers_busy_and_recovers() {
    let gate = Arc::new(Semaphore::new(0));
    let (h, p, clock, tasks) = fixture_with_gate(3, Duration::from_millis(20), gate.clone()).await;
    let mut requests = vec![];
    for i in 0..8 {
        let client = h[1].clone();
        let peer = h[0].peer;
        let b = envelope(&p, &*clock, i);
        requests.push(tokio::spawn(async move {
            client.request(peer, Request::Publish(b)).await
        }));
    }
    tokio::time::sleep(Duration::from_millis(300)).await;
    let response = tokio::time::timeout(
        Duration::from_secs(1),
        h[1].request(h[0].peer, Request::Publish(envelope(&p, &*clock, 8))),
    )
    .await
    .unwrap()
    .unwrap();
    assert!(matches!(response, Response::Busy));
    gate.add_permits(4);
    for request in requests {
        assert!(matches!(
            request.await.unwrap(),
            Ok(Response::Accepted { .. })
        ));
    }
    assert!(matches!(
        h[1].request(h[0].peer, Request::Publish(envelope(&p, &*clock, 9)))
            .await,
        Ok(Response::Accepted { .. })
    ));
    for node in &h {
        node.stop().await;
    }
    for t in tasks {
        t.await.unwrap();
    }
}
