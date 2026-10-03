use crate::{
    metrics::{blank, percentile},
    RunArgs,
};
use anyhow::{anyhow, bail, Result};
use ed25519_dalek::SigningKey;
use libp2p::{identity, PeerId};
use mpe_client::{
    consumer::{reaction_transaction, verify_whole_window},
    fallback::Fallback,
    publisher::Publisher,
    reconcile::{Reconciler, Retrieval, Source as RepairSource},
    subscriber::{Carrier, Subscriber, Subscription},
};
use mpe_core::{
    admission::{AdmissionWitness, Member, RegistryView, RootRecord, StandInRln, LIMITS},
    anchor::{merkle_root, Batch},
    clock::{Clock, SimClock},
    indexer::MockIndexer,
    keys::StreamKeys,
    ledger::{LedgerAdapter, MockContract, MockLedger, RelayEntry},
    outcome::ClientError,
    seal::{seal, EventIn},
    store::{Cursor, InvPage, MemStore, Page, TimeWindow},
    validator::{IgnoreReason, Outcome, RejectReason},
    wire::{eid, hex, message_id, Eid, Envelope, CAPACITIES, LIFETIME, MOCK_NETWORK},
};
use mpe_node::{
    config::MeshConfig,
    node::{self, NodeHandle, NodeOptions},
    protocols::{Capture, Request, Response},
};
use rand::{seq::SliceRandom, Rng, RngCore, SeedableRng};
use rand_chacha::ChaCha20Rng;
use serde_json::{json, Value};
use std::{
    collections::{BTreeMap, BTreeSet, HashMap, HashSet},
    sync::{
        atomic::{AtomicBool, Ordering},
        Arc, Mutex,
    },
    time::{Duration, Instant},
};
use tokio::sync::Semaphore;
#[derive(Clone)]
struct Published {
    eid: Eid,
    stream: usize,
    at: Instant,
    wire: Vec<u8>,
    accepted: bool,
    lei: [u8; 16],
}
#[derive(Clone)]
struct Injection {
    wire: Vec<u8>,
    at: Instant,
    kind: String,
}
#[derive(Default)]
struct ReaderState {
    subscriber: Subscriber,
    recognized: HashMap<Eid, Instant>,
    requests: Vec<String>,
    failovers: u64,
    backfill_eids: BTreeSet<Eid>,
    join_at: Option<Instant>,
    reconciliations: u64,
    repaired: usize,
}
fn bytes32(rng: &mut ChaCha20Rng) -> [u8; 32] {
    let mut b = [0; 32];
    rng.fill_bytes(&mut b);
    b
}
fn peer_key(rng: &mut ChaCha20Rng) -> Result<identity::Keypair> {
    Ok(identity::Keypair::ed25519_from_bytes(bytes32(rng))?)
}
fn process(reader: &Arc<Mutex<ReaderState>>, envelopes: &[Vec<u8>], carrier: Carrier, now: u64) {
    if let Ok(mut state) = reader.lock() {
        for b in envelopes {
            if let Some(d) = state.subscriber.process(b, carrier, now) {
                state.recognized.insert(d.eid, Instant::now());
            }
        }
    }
}
fn make_sub(
    keys: &[StreamKeys],
    signers: &[SigningKey],
    streams: &[usize],
    rng: &mut ChaCha20Rng,
) -> Result<ReaderState> {
    let mut state = ReaderState::default();
    for &stream in streams {
        state.subscriber.install(Subscription {
            keys: keys[stream].clone(),
            publishers: vec![
                signers[stream * 2].verifying_key().to_bytes(),
                signers[stream * 2 + 1].verifying_key().to_bytes(),
            ],
        })?;
    }
    while state.subscriber.subscriptions.len() < 32 {
        state.subscriber.install(Subscription {
            keys: StreamKeys::new(MOCK_NETWORK, bytes32(rng), keys[0].shards)?,
            publishers: vec![],
        })?;
    }
    Ok(state)
}
async fn rpc_feed(
    client: &NodeHandle,
    source: &NodeHandle,
    shard: u8,
    after: u64,
) -> Result<(u64, Vec<Vec<u8>>)> {
    match client
        .request(source.peer, Request::Feed { shard, after })
        .await
        .map_err(|e| anyhow!(e))?
    {
        Response::Feed { cursor, envelopes } => Ok((cursor, envelopes)),
        _ => bail!("feed refused"),
    }
}
async fn backfill(
    client: &NodeHandle,
    sources: &[NodeHandle],
    reader: &Arc<Mutex<ReaderState>>,
    clock: &dyn Clock,
    from: u64,
    until: u64,
    slow: bool,
) -> Result<()> {
    let mut source = 0;
    let mut cursor = Cursor {
        expiry: u32::try_from(from + LIFETIME)?,
        eid: [0; 32],
    };

    loop {
        if source >= sources.len() {
            bail!("all stores unavailable");
        }
        let result = client
            .request(
                sources[source].peer,
                Request::Backfill {
                    shard: 0,
                    from: cursor,
                    until,
                },
            )
            .await;
        match result {
            Ok(Response::Backfill(page)) => {
                if let Ok(mut r) = reader.lock() {
                    r.requests
                        .push(format!("backfill:0:{}:{until}", cursor.expiry));
                }
                if let Ok(mut r) = reader.lock() {
                    r.backfill_eids.extend(
                        page.envelopes
                            .iter()
                            .filter_map(|wire| eid(&MOCK_NETWORK, wire).ok()),
                    );
                }
                process(reader, &page.envelopes, Carrier::Gateway, clock.now());

                if let Some(next) = page.next {
                    cursor = next;
                } else {
                    break;
                }
                if slow {
                    tokio::time::sleep(Duration::from_secs(2)).await;
                }
            }
            _ => {
                source += 1;
                cursor = cursor.overlap();
                if let Ok(mut r) = reader.lock() {
                    r.failovers += 1;
                }
            }
        }
    }
    Ok(())
}
struct RpcRetrieval {
    client: NodeHandle,
    sources: Vec<NodeHandle>,
}
#[async_trait::async_trait]
impl Retrieval for RpcRetrieval {
    async fn inventory(
        &self,
        source: &str,
        shard: u8,
        window: TimeWindow,
        after: Option<Eid>,
    ) -> Result<InvPage, ClientError> {
        let peer = self
            .sources
            .iter()
            .find(|n| n.peer.to_string() == source)
            .ok_or(ClientError::NotReady)?;
        match self
            .client
            .request(
                peer.peer,
                Request::Inventory {
                    shard,
                    window,
                    after,
                },
            )
            .await
        {
            Ok(Response::Inventory(page)) => Ok(page),
            _ => Err(ClientError::NotReady),
        }
    }
    async fn backfill(
        &self,
        source: &str,
        shard: u8,
        from: Cursor,
        until: u64,
    ) -> Result<Page, ClientError> {
        let peer = self
            .sources
            .iter()
            .find(|n| n.peer.to_string() == source)
            .ok_or(ClientError::NotReady)?;
        match self
            .client
            .request(peer.peer, Request::Backfill { shard, from, until })
            .await
        {
            Ok(Response::Backfill(page)) => Ok(page),
            _ => Err(ClientError::NotReady),
        }
    }
}
async fn reconcile_reader(
    reader: &Arc<Mutex<ReaderState>>,
    reconciler: &mut Reconciler,
    transport: &RpcRetrieval,
    shard: u8,
    now: u64,
) {
    let mut subscriber = if let Ok(mut r) = reader.lock() {
        std::mem::take(&mut r.subscriber)
    } else {
        return;
    };
    let result = reconciler
        .reconcile(&mut subscriber, transport, shard, now)
        .await;
    if let Ok(mut r) = reader.lock() {
        for d in &subscriber.deliveries {
            r.recognized.entry(d.eid).or_insert_with(Instant::now);
        }
        if let Ok(repaired) = result {
            r.reconciliations += 1;
            r.repaired += repaired;
        }
        r.subscriber = subscriber;
    }
}
fn record_injection(injections: &Arc<Mutex<Vec<Injection>>>, wire: &[u8], kind: &str) {
    if let Ok(mut v) = injections.lock() {
        v.push(Injection {
            wire: wire.to_vec(),
            at: Instant::now(),
            kind: kind.into(),
        });
    }
}
// Scenario constructors carry the explicit protocol inputs.
#[allow(clippy::too_many_arguments)]
fn attack_envelope(
    keys: &StreamKeys,
    signer: &SigningKey,
    proof: &StandInRln,
    member: usize,
    index: u16,
    class: u8,
    now: u64,
    root: [u8; 32],
    rng: &mut ChaCha20Rng,
) -> Result<Vec<u8>> {
    let ev = EventIn {
        payload: vec![0xac; 16],
        lei: {
            let mut a = [0; 16];
            rng.fill_bytes(&mut a);
            a
        },
        seq: u64::from(index) + 1,
        schema: *b"mpe/data",
        schema_version: 1,
        key_index: 0,
    };
    let mut b = seal(keys, signer, &ev, Some(class), now, rng)?;
    proof.attach(&mut b, member, index, now / 60, MOCK_NETWORK, root)?;
    Ok(b)
}
#[allow(clippy::too_many_arguments)]
fn options(
    key: identity::Keypair,
    proof: Arc<StandInRln>,
    view: RegistryView,
    clock: Arc<SimClock>,
    mesh: MeshConfig,
    allowlist: HashSet<PeerId>,
    capture: Capture,
    gate: Arc<Semaphore>,
    cost: u64,
    subscribe: bool,
    open: bool,
    withholding: bool,
) -> NodeOptions {
    NodeOptions {
        key,
        proof,
        view,
        clock,
        mesh,
        subscribe,
        open,
        allowlist,
        withholding,
        verify_cost_us: cost,
        heartbeat_interval: Duration::from_secs(1),
        global_verify: gate,
        capture,
    }
}

pub async fn run(args: RunArgs) -> Result<Value> {
    if args.nodes < 3
        || args.nodes > 1000
        || !args.duration_secs.is_finite()
        || args.duration_secs <= 0.
        || args.duration_secs > 120.
    {
        bail!("nodes must be 3..=1000 and duration must be finite in (0,120]");
    }
    if !(1..=8).contains(&args.shards) {
        bail!("shards must be 1..=8");
    }
    let tuple: Vec<usize> = args
        .mesh
        .split(',')
        .map(str::parse)
        .collect::<std::result::Result<_, _>>()?;
    let mesh = MeshConfig {
        mesh: tuple
            .try_into()
            .map_err(|_| anyhow!("mesh needs four integers"))?,
        idontwant: args.idontwant == "on",
        eid_message_id: args.msgid == "eid",
        p3: false,
    };
    mpe_node::config::router_config(&mesh, MOCK_NETWORK).map_err(|e| anyhow!(e))?;
    let run_started = Instant::now();
    let mut rng = ChaCha20Rng::seed_from_u64(args.seed);
    let clock = Arc::new(SimClock::new(1_800_000_030));
    let mut keys = vec![];
    for _ in 0..20 {
        let mut k = StreamKeys::new(MOCK_NETWORK, bytes32(&mut rng), args.shards)?;
        k.destination = [3; 32];
        k.action = [4; 32];
        keys.push(k);
    }
    let signers: Vec<_> = (0..42)
        .map(|_| SigningKey::from_bytes(&bytes32(&mut rng)))
        .collect();
    let members: Vec<_> = (0..42).map(|_| Member::new(bytes32(&mut rng))).collect();
    let root = merkle_root(&members.iter().map(Member::leaf).collect::<Vec<_>>());
    let proof = Arc::new(StandInRln::new(members.clone()));
    let mut publishers: Vec<_> = (0..40)
        .map(|i| {
            Publisher::new(
                keys[i / 2].clone(),
                signers[i].clone(),
                AdmissionWitness {
                    secret: members[i].secret,
                    credit_index: 0,
                    limits: LIMITS,
                },
                root,
                proof.clone(),
            )
        })
        .collect();
    for (i, p) in publishers.iter_mut().enumerate() {
        p.key_index = (i % 2) as u16;
    }
    let capture = Capture::default();
    {
        let mut f = capture
            .forbidden
            .write()
            .map_err(|_| anyhow!("capture lock"))?;
        for k in &keys {
            f.extend([
                k.secret.to_vec(),
                k.recognition().to_vec(),
                k.stream_id().to_vec(),
            ]);
        }
        for m in &members {
            f.extend([m.secret.to_vec(), m.commitment().to_vec()]);
        }
        for s in &signers {
            f.push(s.verifying_key().to_bytes().to_vec());
        }
        f.push(b"mpe/data".to_vec());
    }
    let node_keys: Vec<_> = (0..args.nodes)
        .map(|_| peer_key(&mut rng))
        .collect::<Result<_>>()?;
    let client_keys: Vec<_> = (0..20).map(|_| peer_key(&mut rng)).collect::<Result<_>>()?;
    let attacker_count = if args.scenario == "malformed" { 5 } else { 1 };
    let attack_keys: Vec<_> = (0..attacker_count)
        .map(|_| peer_key(&mut rng))
        .collect::<Result<_>>()?;
    let mut allowlist: HashSet<_> = node_keys
        .iter()
        .chain(attack_keys.iter())
        .map(|k| k.public().to_peer_id())
        .collect();
    let attack_peers: HashSet<_> = if args.scenario == "eclipse" {
        node_keys
            .iter()
            .skip(args.nodes - args.nodes / 5)
            .map(|k| k.public().to_peer_id())
            .collect()
    } else {
        HashSet::new()
    };
    let cores = std::thread::available_parallelism().map_or(4, usize::from);
    let offered = if args.load == "rate50" { 50. } else { 10. };
    let cap_cost = ((cores as f64 / 2.) / (args.nodes as f64 * offered) * 1_000_000.) as u64;
    let cost = args.verify_cost_us.min(cap_cost);
    let gate = Arc::new(Semaphore::new(cores.saturating_sub(1).max(1)));
    let initial_view = RegistryView {
        network: MOCK_NETWORK,
        roots: vec![RootRecord {
            root,
            period_start: clock.now(),
            published_at: u64::MAX,
            superseded_at: None,
        }],
        finalized_time: clock.now(),
        shards: args.shards,
        bus_paused: false,
    };
    let mut nodes = vec![];
    let mut tasks = vec![];
    for key in node_keys {
        let withholding = attack_peers.contains(&key.public().to_peer_id());
        let (h, t) = node::start(options(
            key,
            proof.clone(),
            initial_view.clone(),
            clock.clone(),
            mesh.clone(),
            allowlist.clone(),
            capture.clone(),
            gate.clone(),
            cost,
            true,
            args.open || args.scenario == "eclipse",
            withholding,
        ))
        .await?;
        nodes.push(h);
        tasks.push(t);
    }
    let mut clients = vec![];
    for key in client_keys {
        let (h, t) = node::start(options(
            key,
            proof.clone(),
            initial_view.clone(),
            clock.clone(),
            mesh.clone(),
            allowlist.clone(),
            capture.clone(),
            gate.clone(),
            0,
            false,
            true,
            false,
        ))
        .await?;
        clients.push(h);
        tasks.push(t);
    }
    let mut attackers = vec![];
    for key in attack_keys {
        let (h, t) = node::start(options(
            key,
            proof.clone(),
            initial_view.clone(),
            clock.clone(),
            mesh.clone(),
            allowlist.clone(),
            capture.clone(),
            gate.clone(),
            0,
            true,
            true,
            false,
        ))
        .await?;
        attackers.push(h);
        tasks.push(t);
    }
    let published_root = clock.now() + 1;
    let roster: Vec<_> = nodes
        .iter()
        .enumerate()
        .map(|(i, n)| RelayEntry {
            peer_id: n.peer.to_string(),
            operator: [(i % 3 + 1) as u8; 32],
            relay: true,
            store: i < 3,
            bootstrapper: i == args.nodes - 1 || i == args.nodes - 2,
            gateway: true,
            anchorer: i == 3.min(args.nodes - 1),
        })
        .collect();
    let ledger = Arc::new(MockLedger::new(
        MOCK_NETWORK,
        clock.now(),
        vec![RootRecord {
            root,
            period_start: clock.now(),
            published_at: published_root,
            superseded_at: None,
        }],
        roster,
        args.shards,
    ));
    let mut view = ledger.view(clock.now())?;
    view.finalized_time = clock.now();
    for n in nodes.iter().chain(&clients).chain(&attackers) {
        n.update_view(view.clone()).await;
    }
    let operator_signers: Vec<_> = (0..3)
        .map(|_| SigningKey::from_bytes(&bytes32(&mut rng)))
        .collect();
    for i in 0..3 {
        nodes[i]
            .enable_store(MemStore::new(
                MOCK_NETWORK,
                [(i + 1) as u8; 32],
                operator_signers[i].clone(),
                256 * 1024 * 1024,
            ))
            .await?;
    }
    // Connected seeded topology; the two final nodes provide initial bootstrap dials and also relay in this bounded PoC.
    for i in 0..nodes.len() {
        let mut choices: Vec<_> = (0..nodes.len()).filter(|&j| j != i).collect();
        choices.shuffle(&mut rng);
        for j in choices.into_iter().take(10) {
            nodes[i].dial(nodes[j].address.clone()).await?;
        }
        if i > 0 {
            nodes[i].dial(nodes[i - 1].address.clone()).await?;
        }
    }
    for (i, client) in clients.iter().enumerate() {
        for j in [i % 10 % nodes.len(), (i % 10 + 1) % nodes.len()] {
            client.dial(nodes[j].address.clone()).await?;
        }
    }
    for client in clients.iter().skip(10) {
        for service in nodes.iter().take(4) {
            client.dial(service.address.clone()).await?;
        }
    }
    for attacker in &attackers {
        for n in &nodes[..nodes.len().min(12)] {
            attacker.dial(n.address.clone()).await?;
        }
    }
    if args.scenario == "eclipse" {
        for n in nodes.iter().filter(|n| attack_peers.contains(&n.peer)) {
            n.dial(nodes[0].address.clone()).await?;
        }
    }
    let stop = Arc::new(AtomicBool::new(false));
    let ledger_stop = stop.clone();
    let ledger_bg = ledger.clone();
    let clock_bg = clock.clone();
    let all_nodes = Arc::new(Mutex::new(nodes.clone()));
    let update_nodes = all_nodes.clone();
    let ledger_task = tokio::spawn(async move {
        while !ledger_stop.load(Ordering::Relaxed) {
            let _ = ledger_bg.advance_to(clock_bg.now());
            if let Ok(v) = ledger_bg.view(clock_bg.now()) {
                let list = update_nodes.lock().map(|n| n.clone()).unwrap_or_default();
                for node in list {
                    node.update_view(v.clone()).await;
                }
            }
            tokio::time::sleep(Duration::from_secs(1)).await;
        }
    });
    if args.scenario == "anchor" {
        nodes[3.min(nodes.len() - 1)]
            .enable_anchoring(ledger.clone())
            .await;
        ledger.add_contract(
            [3; 32],
            MockContract {
                publishers: signers[..40]
                    .iter()
                    .map(|s| s.verifying_key().to_bytes())
                    .collect(),
                action: [4; 32],
                nullifiers: HashSet::new(),
                effects: vec![],
            },
        );
    }
    tokio::time::sleep(Duration::from_secs(10)).await;
    let mut result = blank(&args.scenario, args.seed, args.nodes, args.duration_secs);
    let mut notes=vec![format!("warmup=10s; synthetic admission verification cost={cost}us; host available_parallelism={cores}; not measured RLN cost"),"Transport: real localhost TCP/Noise/Yamux; counters are below Noise and include control and client traffic; no WAN delay or bandwidth limit.".into(),"Stand-in verifiers possess member secrets; no admission unlinkability or production security claim.".into(),"Bootstrap fixtures relay too; standalone publisher/subscriber swarms: 10 each. Three store operators. Store and client state are volatile.".into()];
    let (attacker_peers, honest_peers) = nodes[0]
        .stats
        .lock()
        .map(|s| {
            (
                s.peers.iter().filter(|p| attack_peers.contains(p)).count(),
                s.peers.iter().filter(|p| !attack_peers.contains(p)).count(),
            )
        })
        .unwrap_or_default();
    let start = Instant::now();
    let start_unix = clock.now();
    let counter_start: Vec<_> = nodes.iter().map(|n| n.counters.snapshot()).collect();
    let class_start: Vec<_> = nodes.iter().map(|n| n.counters.egress_snapshot()).collect();
    let cpu_start: Vec<_> = nodes
        .iter()
        .map(|n| n.stats.lock().map(|s| s.cpu_ns).unwrap_or(0))
        .collect();
    let records = Arc::new(Mutex::new(Vec::<Published>::new()));
    let injections = Arc::new(Mutex::new(Vec::<Injection>::new()));
    let mut readers = vec![];
    let mut reader_tasks = vec![];
    let subscriber_count = if args.scenario == "fallback" { 3 } else { 10 };
    let mut interests = vec![];
    for i in 0..subscriber_count {
        let streams: Vec<_> = if args.scenario == "fallback" {
            (0..20).collect()
        } else {
            (0..4).map(|j| (i * 2 + j) % 20).collect()
        };
        let state = Arc::new(Mutex::new(make_sub(&keys, &signers, &streams, &mut rng)?));
        interests.push(streams);
        readers.push(state.clone());
        let client = clients[10 + i].clone();
        let mut source = nodes[i % nodes.len()].clone();
        let live_nodes = all_nodes.clone();
        let mut reconciler = Reconciler::new(
            RepairSource {
                peer: source.peer.to_string(),
                operator: [(i % 3 + 1) as u8; 32],
            },
            RepairSource {
                peer: nodes[(i + 1) % 3].peer.to_string(),
                operator: [((i + 1) % 3 + 1) as u8; 32],
            },
            start_unix,
        )?;
        let clock = clock.clone();
        let stop = stop.clone();
        let fallback = args.scenario == "fallback";
        let indexer = MockIndexer::new(ledger.clone());
        let embedded = i % 2 == 0;
        let shards = args.shards;
        reader_tasks.push(tokio::spawn(async move {
            let mut cursor = vec![0_u64; shards as usize];
            let mut local_cursor = 0_u64;
            let mut reconcile_due = clock.now() + 60;
            let mut feed = false;
            let mut fallback_client = Fallback::default();
            fallback_client.select_profile();
            while !stop.load(Ordering::Relaxed) {
                if fallback {
                    if let Ok(mut r) = state.lock() {
                        if let Ok(deliveries) =
                            fallback_client.poll(&indexer, &mut r.subscriber, clock.now())
                        {
                            for d in deliveries {
                                r.recognized.insert(d.eid, Instant::now());
                            }
                        }
                    }
                    tokio::time::sleep(Duration::from_secs(1)).await;
                    continue;
                }
                if source.is_stopped() {
                    let list = live_nodes.lock().map(|n| n.clone()).unwrap_or_default();
                    let Some(backup) = list
                        .iter()
                        .cycle()
                        .skip(i + 1)
                        .take(list.len())
                        .find(|n| !n.is_stopped() && n.feed_head() > 0)
                        .cloned()
                    else {
                        break;
                    };
                    let index = list.iter().position(|n| n.peer == backup.peer).unwrap_or(0);
                    source = backup;
                    reconciler.feed = RepairSource {
                        peer: source.peer.to_string(),
                        operator: [(index % 3 + 1) as u8; 32],
                    };
                    local_cursor = 0;
                    cursor.fill(0);
                    feed = true;
                    if let Ok(mut s) = state.lock() {
                        s.failovers += 1;
                    }
                }
                if clock.now() >= reconcile_due {
                    let list = live_nodes.lock().map(|n| n.clone()).unwrap_or_default();
                    let stores: Vec<_> = list.into_iter().take(3).collect();
                    if let Some((index, repair)) = stores.iter().enumerate().find(|(index, n)| {
                        !n.is_stopped() && [(*index + 1) as u8; 32] != reconciler.feed.operator
                    }) {
                        reconciler.repair = RepairSource {
                            peer: repair.peer.to_string(),
                            operator: [(index + 1) as u8; 32],
                        };
                        let transport = RpcRetrieval {
                            client: client.clone(),
                            sources: stores,
                        };
                        // Each shard has the same time window; advance the reconciliation clock only after all shards.
                        let previous = reconciler.last;
                        for shard in 0..shards {
                            reconciler.last = previous;
                            reconcile_reader(
                                &state,
                                &mut reconciler,
                                &transport,
                                shard,
                                clock.now(),
                            )
                            .await;
                        }
                    }
                    reconcile_due = clock.now() + 60;
                }
                if let Ok(mut r) = state.lock() {
                    r.subscriber.prune(clock.now());
                }
                if embedded && !feed {
                    let accepted = source.accepted_since(local_cursor);
                    if let Some(last) = accepted.last() {
                        local_cursor = last.cursor;
                    }
                    let envelopes: Vec<_> = accepted.into_iter().map(|a| a.wire).collect();
                    process(&state, &envelopes, Carrier::Overlay, clock.now());
                    tokio::time::sleep(Duration::from_millis(20)).await;
                } else {
                    for shard in 0..shards {
                        if let Ok(mut r) = state.lock() {
                            r.requests
                                .push(format!("feed:{shard}:{}", cursor[shard as usize]));
                        }
                        if let Ok((next, envelopes)) =
                            rpc_feed(&client, &source, shard, cursor[shard as usize]).await
                        {
                            cursor[shard as usize] = next;
                            process(&state, &envelopes, Carrier::Gateway, clock.now());
                        }
                    }
                    tokio::time::sleep(Duration::from_secs(1)).await;
                }
            }
        }));
    }
    let mut late = None;
    let backfill_expected = Arc::new(Mutex::new(BTreeSet::<Eid>::new()));
    if args.scenario == "backfill" {
        let streams = vec![0, 1, 2, 3];
        let state = Arc::new(Mutex::new(make_sub(&keys, &signers, &streams, &mut rng)?));
        interests.push(streams);
        readers.push(state.clone());
        late = Some(state.clone());
        let expected = backfill_expected.clone();
        let records = records.clone();
        let client = clients[19].clone();
        let sources = nodes[..3].to_vec();
        let clock = clock.clone();
        let duration = args.duration_secs;
        let stop = stop.clone();
        reader_tasks.push(tokio::spawn(async move {
            tokio::time::sleep_until(tokio::time::Instant::from_std(
                start + Duration::from_secs_f64(duration / 2.),
            ))
            .await;
            if let Ok(records) = records.lock() {
                if let Ok(mut e) = expected.lock() {
                    e.extend(records.iter().filter(|p| p.accepted).map(|p| p.eid));
                }
            }
            if let Ok(mut r) = state.lock() {
                r.join_at = Some(Instant::now());
            }
            let mut cursor = sources[1].feed_head();
            let recovery_client = client.clone();
            let recovery_state = state.clone();
            let recovery_clock = clock.clone();
            let recovery_sources = sources.clone();
            let join_until = clock.now();
            let recovery = tokio::spawn(async move {
                backfill(
                    &recovery_client,
                    &recovery_sources,
                    &recovery_state,
                    &*recovery_clock,
                    start_unix,
                    join_until,
                    true,
                )
                .await
            });
            while !stop.load(Ordering::Relaxed) {
                if let Ok((next, envelopes)) = rpc_feed(&client, &sources[1], 0, cursor).await {
                    cursor = next;
                    process(&state, &envelopes, Carrier::Gateway, clock.now());
                }
                tokio::time::sleep(Duration::from_secs(1)).await;
            }
            let _ = recovery.await;
        }));
    }
    let mut attack_tasks = vec![];
    if args.scenario == "spam" {
        let ingress = nodes[0].clone();
        let client = attackers[0].clone();
        let proof = proof.clone();
        let clock = clock.clone();
        let k = keys[0].clone();
        let signer = signers[40].clone();
        let injections = injections.clone();
        let duration = args.duration_secs;
        let mut arng = ChaCha20Rng::seed_from_u64(args.seed ^ 0xaaaa);
        attack_tasks.push(tokio::spawn(async move {
            for i in 0..(duration * 100.) as u32 {
                tokio::time::sleep_until(tokio::time::Instant::from_std(
                    start + Duration::from_secs_f64(i as f64 / 100.),
                ))
                .await;
                let epoch_index = (i % 128) as u16;
                let Ok(b) = attack_envelope(
                    &k,
                    &signer,
                    &proof,
                    40,
                    epoch_index,
                    0,
                    clock.now(),
                    root,
                    &mut arng,
                ) else {
                    continue;
                };
                record_injection(&injections, &b, "spam");
                let client = client.clone();
                let peer = ingress.peer;
                tokio::spawn(async move {
                    let _ = client.request(peer, Request::Publish(b)).await;
                });
            }
        }));
    }
    if args.scenario == "malformed" {
        for (i, attacker) in attackers.iter().cloned().enumerate() {
            let proof = proof.clone();
            let clock = clock.clone();
            let k = keys[0].clone();
            let signer = signers[40].clone();
            let injections = injections.clone();
            let duration = args.duration_secs;
            let mut arng = ChaCha20Rng::seed_from_u64(args.seed ^ i as u64 ^ 0xbbbb);
            attack_tasks.push(tokio::spawn(async move {
                for j in 0..(duration * 20.) as usize {
                    tokio::time::sleep_until(tokio::time::Instant::from_std(
                        start + Duration::from_secs_f64(j as f64 / 20.),
                    ))
                    .await;
                    let Ok(mut b) = attack_envelope(
                        &k,
                        &signer,
                        &proof,
                        40,
                        (j % 64) as u16,
                        0,
                        clock.now(),
                        root,
                        &mut arng,
                    ) else {
                        continue;
                    };
                    let kind = match j % 13 {
                        0 => {
                            b = vec![0xff; 20];
                            "garbage"
                        }
                        1 => {
                            b.truncate(775);
                            "truncated"
                        }
                        2 => {
                            b.push(0);
                            "oversize"
                        }
                        3 => {
                            b[0] = 2;
                            "version"
                        }
                        4 => {
                            b[3] = 1;
                            "reserved"
                        }
                        5 => {
                            b[1] = 4;
                            "class"
                        }
                        6 => {
                            b[2] = 7;
                            "shard"
                        }
                        7 => {
                            b[368] = 1;
                            "filler"
                        }
                        8 => {
                            b[112] ^= 1;
                            "proof"
                        }
                        9 => {
                            b[4..8].copy_from_slice(
                                &((clock.now() + LIFETIME + 61) as u32).to_be_bytes(),
                            );
                            "future"
                        }
                        10 => {
                            b[4..8].copy_from_slice(&((clock.now() - 61) as u32).to_be_bytes());
                            "expired"
                        }
                        11 => {
                            b.resize(65537, 0);
                            "oversize_rpc"
                        }
                        _ => {
                            let _ = proof.attach(
                                &mut b,
                                40,
                                (j % 64) as u16,
                                clock.now() / 60,
                                [1; 32],
                                root,
                            );
                            "network"
                        }
                    };
                    record_injection(&injections, &b, kind);
                    let _ = attacker.inject(b, 0, true).await;
                }
            }));
        }
    }
    if args.scenario == "replay" {
        let records = records.clone();
        let proof = proof.clone();
        let clock = clock.clone();
        let attacker = attackers[0].clone();
        let injections = injections.clone();
        attack_tasks.push(tokio::spawn(async move {
            tokio::time::sleep_until(tokio::time::Instant::from_std(
                start + Duration::from_secs(62),
            ))
            .await;
            let captured: Vec<_> = records
                .lock()
                .map(|v| {
                    v.iter()
                        .filter(|p| p.at.duration_since(start).as_secs_f64() < 2.)
                        .take(200)
                        .cloned()
                        .collect()
                })
                .unwrap_or_default();
            let mut list: Vec<(Vec<u8>, &str)> = captured
                .iter()
                .map(|p| (p.wire.clone(), "replay"))
                .collect();
            for (i, p) in captured.iter().take(50).enumerate() {
                let mut b = p.wire.clone();
                let _ = proof.attach(&mut b, 40, i as u16, clock.now() / 60, MOCK_NETWORK, root);
                list.push((b, "reslot_replay"));
            }
            for i in 0..200 {
                let mut b = captured
                    .first()
                    .map(|p| p.wire.clone())
                    .unwrap_or_else(|| vec![0; 776]);
                b[4..8].copy_from_slice(&((clock.now() - 61) as u32).to_be_bytes());
                b[700..704].copy_from_slice(&(i as u32).to_be_bytes());
                list.push((b, "expired"));
            }
            for (b, kind) in list {
                record_injection(&injections, &b, kind);
                let _ = attacker.inject(b, 0, true).await;
                tokio::time::sleep(Duration::from_millis(120)).await;
            }
        }));
    }
    let mut stopped_store = false;
    let mut churn_at = 10.;
    let mut churn_count = 0;
    let mut churn_order: Vec<_> = (0..nodes.len()).collect();
    churn_order.shuffle(&mut ChaCha20Rng::seed_from_u64(args.seed ^ 0xc817));
    let mut retired_nodes = vec![];
    let mut publication_tasks = vec![];
    let retry_notes = Arc::new(Mutex::new(Vec::new()));
    let mut fallback = Fallback::default();
    fallback.select_profile();
    let mut planned = vec![];
    let rate = if args.scenario == "fallback" {
        2.
    } else if args.load == "bytecap" {
        65536. / 16904.
    } else if args.load == "rate50" {
        50.
    } else {
        10.
    };
    let mut time = 0.;
    while time < args.duration_secs {
        time += -(1. - rng.gen::<f64>()).ln() / rate;
        if time > args.duration_secs {
            break;
        }
        let class = if args.load == "bytecap" {
            3
        } else if args.scenario == "fallback" {
            rng.gen_range(0..3)
        } else {
            match rng.gen_range(0..100) {
                0..=59 => 0,
                60..=84 => 1,
                85..=94 => 2,
                _ => 3,
            }
        };
        planned.push((
            time,
            class,
            rng.gen_range(0..40),
            rng.gen_range(16..=CAPACITIES[class as usize]),
        ));
    }
    if args.scenario == "fallback" && args.duration_secs >= 20. {
        for i in 0..200 {
            planned.push((20., (i % 3) as u8, i % 40, 16));
        }
        planned.sort_by(|a, b| a.0.total_cmp(&b.0));
    }
    for (time, class, mut member, len) in planned {
        tokio::time::sleep_until(tokio::time::Instant::from_std(
            start + Duration::from_secs_f64(time),
        ))
        .await;
        if args.scenario == "backfill" && !stopped_store && time >= args.duration_secs * 0.75 {
            nodes[0].stop().await;
            stopped_store = true;
            notes.push("First store stopped at 75% of publishing; late client resumes from an overlapping portable cursor on operator 2.".into());
        }
        if args.scenario == "churn" && time >= churn_at {
            let count = (args.nodes / 10).max(1);
            for j in 0..count {
                let index = churn_order[(j + churn_count) % churn_order.len()];
                nodes[index].stop().await;
                retired_nodes.push(nodes[index].clone());
                let key = peer_key(&mut rng)?;
                allowlist.insert(key.public().to_peer_id());
                let fresh_view = ledger.view(clock.now())?;
                let (h, t) = node::start(options(
                    key,
                    proof.clone(),
                    fresh_view,
                    clock.clone(),
                    mesh.clone(),
                    allowlist.clone(),
                    capture.clone(),
                    gate.clone(),
                    cost,
                    true,
                    args.open,
                    false,
                ))
                .await?;
                for old in &nodes[..nodes.len().min(10)] {
                    h.dial(old.address.clone()).await?;
                }
                if index < 3 {
                    h.enable_store(MemStore::new(
                        MOCK_NETWORK,
                        [(index + 1) as u8; 32],
                        operator_signers[index].clone(),
                        256 * 1024 * 1024,
                    ))
                    .await?;
                }
                notes.push(format!(
                    "Churn replaced node={index}, ingress_or_subscriber_source={}",
                    index < 10
                ));
                nodes[index] = h;
                tasks.push(t);
            }
            if let Ok(mut list) = all_nodes.lock() {
                *list = nodes.clone();
            }
            for node in nodes.iter().chain(&clients).chain(&attackers) {
                node.update_allowlist(allowlist.clone()).await;
            }
            churn_count += count;
            churn_at += 10.;
        }
        let mut payload = vec![0; len];
        rng.fill_bytes(&mut payload);
        let canary = payload[..16].to_vec();
        capture
            .forbidden
            .write()
            .map_err(|_| anyhow!("capture lock"))?
            .push(canary);
        let mut publication = None;
        for _ in 0..40 {
            match publishers[member].prepare(payload.clone(), Some(class), clock.now(), &mut rng) {
                Ok(p) => {
                    publication = Some(p);
                    break;
                }
                Err(mpe_core::outcome::ClientError::NotReady) => member = (member + 1) % 40,
                Err(e) => return Err(e.into()),
            }
        }
        let Some(p) = publication else {
            notes.push("Scheduled publication refused: all membership quotas exhausted.".into());
            continue;
        };
        capture
            .forbidden
            .write()
            .map_err(|_| anyhow!("capture lock"))?
            .extend([
                p.event.lei.to_vec(),
                keys[member / 2]
                    .encryption(&p.wire[520..536].try_into()?)
                    .to_vec(),
            ]);
        if args.scenario == "replay" && records.lock().map(|v| v.is_empty()).unwrap_or(false) {
            let mut bad = p.wire.clone();
            bad[112] ^= 1;
            attackers[0].inject(bad, 0, true).await?;
            tokio::time::sleep(Duration::from_millis(50)).await;
        }
        let at = Instant::now();
        let index = records.lock().map_err(|_| anyhow!("records lock"))?.len();
        records
            .lock()
            .map_err(|_| anyhow!("records lock"))?
            .push(Published {
                eid: p.eid,
                stream: member / 2,
                at,
                wire: p.wire.clone(),
                accepted: false,
                lei: p.event.lei,
            });
        if args.scenario == "fallback" {
            let accepted = fallback.publish(&*ledger, &p.wire, clock.now()).is_ok();
            records.lock().map_err(|_| anyhow!("records lock"))?[index].accepted = accepted;
        } else {
            let client = clients[member % 10].clone();
            let first = (member % 10) % nodes.len();
            let second = (first + 1) % nodes.len();
            let target = if rng.gen::<bool>() { first } else { second };
            let ingress = nodes[target].clone();
            let alternate = nodes[if target == first { second } else { first }].clone();
            let records = records.clone();
            let clock = clock.clone();
            let retry_notes = retry_notes.clone();
            let live_nodes = all_nodes.clone();
            publication_tasks.push(tokio::spawn(async move {
                let deadline = tokio::time::Instant::now() + Duration::from_secs(5);
                let first_result = client.request(ingress.peer,Request::Publish(p.wire.clone())).await;
                let accepted = if matches!(first_result,Ok(Response::Accepted { eid }) if eid == p.eid) { true } else {
                    if let Ok(mut notes) = retry_notes.lock() { notes.push(format!("Publisher retry: member={member}, target={target}, first_result={first_result:?}")); }
                    if !matches!(first_result,Ok(Response::Busy | Response::Refused)) { tokio::time::sleep_until(deadline).await; }
                    let response = client.request(alternate.peer,Request::Publish(p.wire.clone())).await;
                    if matches!(response,Ok(Response::Accepted { eid }) if eid == p.eid) { true } else {
                        // Both configured ingress identities may have restarted. Refresh from the live roster.
                        let list = live_nodes.lock().map(|n|n.clone()).unwrap_or_default();
                        let mut accepted = false;
                        for node in list.iter().filter(|n| !n.is_stopped() && n.peer != ingress.peer && n.peer != alternate.peer) {
                            if clock.now() >= p.epoch.saturating_mul(60).saturating_add(80) { break; }
                            if matches!(client.request(node.peer,Request::Publish(p.wire.clone())).await,Ok(Response::Accepted { eid }) if eid == p.eid) { accepted = true; break; }
                        }
                        accepted
                    }
                };
                if let Ok(mut records) = records.lock() { records[index].accepted = accepted; }
            }));
        }
    }
    tokio::time::sleep_until(tokio::time::Instant::from_std(
        start + Duration::from_secs_f64(args.duration_secs),
    ))
    .await;
    let schedule_elapsed = start.elapsed().as_secs_f64();
    for task in publication_tasks {
        task.await?;
    }
    if let Ok(retries) = retry_notes.lock() {
        notes.extend(retries.iter().cloned());
    }
    let counter_end: Vec<_> = nodes.iter().map(|n| n.counters.snapshot()).collect();
    let class_end: Vec<_> = nodes.iter().map(|n| n.counters.egress_snapshot()).collect();
    let cpu_end: Vec<_> = nodes
        .iter()
        .map(|n| n.stats.lock().map(|s| s.cpu_ns).unwrap_or(0))
        .collect();
    let drain = match args.scenario.as_str() {
        "churn" => 125.,
        "anchor" => 90.,
        "fallback" => 40.,
        "backfill" => 30.,
        "replay" => (105. - args.duration_secs).max(15.),
        _ => 15.,
    };
    notes.push(format!("publish_window={}s; actual_publish_elapsed={:.3}s; drain={drain}s; churn replacements={churn_count}",args.duration_secs,schedule_elapsed));
    if args.scenario == "spam" {
        let a = attack_envelope(
            &keys[0],
            &signers[0],
            &proof,
            40,
            0,
            3,
            clock.now(),
            root,
            &mut rng,
        )?;
        let b = attack_envelope(
            &keys[0],
            &signers[0],
            &proof,
            40,
            0,
            3,
            clock.now(),
            root,
            &mut rng,
        )?;
        let ids = [eid(&MOCK_NETWORK, &a)?, eid(&MOCK_NETWORK, &b)?];
        let ingress_a = &nodes[10.min(nodes.len() - 1)];
        let ingress_b = &nodes[11.min(nodes.len() - 1)];
        let (a_result, b_result) = tokio::join!(
            attackers[0].request(ingress_a.peer, Request::Publish(a)),
            attackers[0].request(ingress_b.peer, Request::Publish(b))
        );
        let first_accepts = usize::from(matches!(a_result, Ok(Response::Accepted { .. })))
            + usize::from(matches!(b_result, Ok(Response::Accepted { .. })));
        notes.push(format!("Spam phase B: two concurrent class-3 bodies under one nullifier, per-epoch class-3 limit=1, first-ingress accepts={first_accepts}, EIDs={:?}; aggregate-bound counterexample is also an integration test",ids.iter().map(|id|hex(id)).collect::<Vec<_>>()));
    }
    // Add admitted bad-tag and insider bad-signature envelopes without polluting the honest denominator.
    if args.scenario == "malformed" {
        for (kind, index) in [("bad_signature", 0_u16), ("bad_tag", 1_u16)] {
            let mut b = attack_envelope(
                &keys[0],
                &signers[41],
                &proof,
                41,
                index,
                0,
                clock.now(),
                root,
                &mut rng,
            )?;
            if kind == "bad_tag" {
                b[548..564].fill(0x66);
                proof.attach(&mut b, 41, index, clock.now() / 60, MOCK_NETWORK, root)?;
            }
            record_injection(&injections, &b, kind);
            let _ = clients[0].request(nodes[1].peer, Request::Publish(b)).await;
        }
    }
    tokio::time::sleep(Duration::from_secs_f64(drain)).await;
    for task in attack_tasks {
        if let Err(e) = task.await {
            notes.push(format!("attack task failed: {e}"));
        }
    }
    let records = records.lock().map_err(|_| anyhow!("records lock"))?.clone();
    let mut checked = 0;
    let mut valid = 0;
    if args.scenario == "anchor" {
        let anchorer = &nodes[3.min(nodes.len() - 1)];
        let anchors = ledger.anchors(0)?;
        result["anchor"]["batches"] = json!(anchors.len());
        for anchor in &anchors {
            let mut leaves = vec![];
            for shard in 0..args.shards {
                match clients[10]
                    .request(
                        anchorer.peer,
                        Request::AnchorLeaves {
                            window: anchor.payload.window,
                            shard,
                        },
                    )
                    .await
                {
                    Ok(Response::AnchorLeaves(ids)) => leaves.push(ids),
                    _ => leaves.push(vec![]),
                }
            }
            let batch = Batch::new(anchor.payload.window, leaves)?;
            for reader in readers.iter().take(2) {
                let mut r = reader.lock().map_err(|_| anyhow!("reader lock"))?;
                checked += 1;
                if verify_whole_window(&mut r.subscriber.deliveries, &batch, &anchor.payload) {
                    valid += 1;
                }
            }
        }
        if let Some(event) = records.iter().find(|p| {
            anchors.iter().any(|a| {
                a.payload.window
                    == mpe_core::anchor::window(
                        Envelope::parse(&p.wire)
                            .map(|e| e.header.expiry)
                            .unwrap_or(0),
                    )
            })
        }) {
            if let Ok(Response::Inclusion(proof)) = clients[10]
                .request(anchorer.peer, Request::Inclusion { eid: event.eid })
                .await
            {
                checked += 1;
                if anchors.iter().any(|a| proof.verify(&event.eid, &a.payload)) {
                    valid += 1;
                }
                let mut subscriber =
                    make_sub(&keys, &signers, &[event.stream], &mut rng)?.subscriber;
                let delivery = subscriber
                    .process(&event.wire, Carrier::Overlay, clock.now())
                    .ok_or_else(|| anyhow!("anchor recognition failed"))?;
                let tx =
                    reaction_transaction(&keys[event.stream], &delivery, Some(proof), clock.now())?;
                ledger.register_reaction_witness(
                    &delivery.event.statement,
                    delivery.eid,
                    mpe_client::consumer::consumption_nullifier(
                        &keys[event.stream],
                        &[3; 32],
                        &delivery.event.event.lei,
                    ),
                    u64::from(delivery.event.expiry),
                );
                for _ in 0..100 {
                    let _ = ledger.submit(tx.clone());
                }
                ledger.advance_to(clock.now() + 30)?;
                notes.push(format!(
                    "100 reacting consumers, effects={}; EID={} LEI={}",
                    ledger.effect_count(&[3; 32]),
                    hex(&event.eid),
                    hex(&event.lei)
                ));
                // Crash/resume is a new subscription store which retrieves through the real store RPC.
                let resumed = Arc::new(Mutex::new(make_sub(
                    &keys,
                    &signers,
                    &[event.stream],
                    &mut rng,
                )?));
                backfill(
                    &clients[19],
                    &nodes[..3],
                    &resumed,
                    &*clock,
                    start_unix,
                    clock.now(),
                    false,
                )
                .await?;
                notes.push(format!("E2e client crash/backfill resume: {} EIDs recovered; registry genesis members={}",resumed.lock().map(|r|r.subscriber.received.len()).unwrap_or(0),members.len()));
            }
        }
        result["anchor"]["inclusion_proofs_checked"] = json!(checked);
        result["anchor"]["inclusion_proofs_valid"] = json!(valid);
    }
    stop.store(true, Ordering::Relaxed);
    for task in reader_tasks {
        if let Err(e) = task.await {
            notes.push(format!("reader task failed: {e}"));
        }
    }
    ledger_task.await?;
    notes.push(format!(
        "Subscriber source failovers={}; reconciliation calls={}; repaired observations={}",
        readers
            .iter()
            .filter_map(|r| r.lock().ok().map(|r| r.failovers))
            .sum::<u64>(),
        readers
            .iter()
            .filter_map(|r| r.lock().ok().map(|r| r.reconciliations))
            .sum::<u64>(),
        readers
            .iter()
            .filter_map(|r| r.lock().ok().map(|r| r.repaired))
            .sum::<usize>()
    ));
    let mut expected = 0;
    let mut received = 0;
    let mut latencies = vec![];
    let mut minimum = 1_f64;
    let mut received_ids = HashSet::new();
    let mut network_bytes = 0;
    let mut duplicate_count = 0;
    for (i, reader) in readers.iter().enumerate() {
        let r = reader.lock().map_err(|_| anyhow!("reader lock"))?;
        let eligible: Vec<_> = records
            .iter()
            .filter(|p| interests[i].contains(&p.stream))
            .collect();
        let e = eligible.len();
        let got = eligible
            .iter()
            .filter(|p| r.recognized.contains_key(&p.eid))
            .count();
        expected += e;
        received += got;
        if e > 0 {
            minimum = minimum.min(got as f64 / e as f64);
        }
        for p in eligible {
            if let Some(at) = r.recognized.get(&p.eid) {
                latencies.push(at.saturating_duration_since(p.at).as_secs_f64() * 1000.);
                received_ids.insert(p.eid);
            }
        }
        network_bytes += r.subscriber.network_bytes;
        let mut logical = HashSet::new();
        for d in &r.subscriber.deliveries {
            if !logical.insert((d.event.publisher, d.event.event.lei)) {
                duplicate_count += 1;
            }
        }
    }
    result["published"] = json!(records.len());
    result["delivered"] = json!({"expected":expected,"received":received,"ratio":if expected>0{Some(received as f64/expected as f64)}else{None},"per_subscriber_min_ratio":minimum});
    result["latency_ms"] = json!({"p50":percentile(&latencies,0.5),"p95":percentile(&latencies,0.95),"p99":percentile(&latencies,0.99),"max":percentile(&latencies,1.)});
    result["duplicates"] = json!(duplicate_count);
    let unique_bytes: usize = records
        .iter()
        .filter(|p| p.accepted)
        .map(|p| p.wire.len())
        .sum();
    let incoming: Vec<_> = counter_end
        .iter()
        .zip(&counter_start)
        .map(|(end, start)| end.0.saturating_sub(start.0) as f64)
        .collect();
    let outgoing: Vec<_> = counter_end
        .iter()
        .zip(&counter_start)
        .map(|(end, start)| end.1.saturating_sub(start.1) as f64)
        .collect();
    let cpu: Vec<_> = cpu_end
        .iter()
        .zip(&cpu_start)
        .map(|(end, start)| end.saturating_sub(*start) as f64 / 1_000_000.)
        .collect();
    result["bandwidth"] = json!({"per_node_in_bytes_p50":percentile(&incoming,0.5).unwrap_or(0.)as u64,"per_node_out_bytes_p50":percentile(&outgoing,0.5).unwrap_or(0.)as u64,"max_in":percentile(&incoming,1.).unwrap_or(0.)as u64,"max_out":percentile(&outgoing,1.).unwrap_or(0.)as u64});
    result["bandwidth"]["gossipsub_payload_egress_per_class_p50"] = json!((0..4)
        .map(|class| {
            let samples: Vec<_> = class_end
                .iter()
                .zip(&class_start)
                .map(|(end, start)| end[class].saturating_sub(start[class]) as f64)
                .collect();
            percentile(&samples, 0.5).unwrap_or(0.) as u64
        })
        .collect::<Vec<_>>());
    notes.push(format!("IDONTWANT={}; network-scoped GossipSub 1.2; negotiated v1.2 peer observations={}; class egress counts envelope payload bytes after successful connection-handler flush, excludes protobuf/Noise/control/RPC overhead",args.idontwant,nodes.iter().filter_map(|n|n.stats.lock().ok().map(|s|s.v12_peers)).sum::<usize>()));
    result["cpu_ms_per_node_p50"] = json!(percentile(&cpu, 0.5));
    {
        let capture_stats = capture.stats.lock().map_err(|_| anyhow!("capture lock"))?;
        result["wire"] = json!({"envelope_sizes":capture_stats.sizes.iter().map(|(s,n)|(s.to_string(),*n)).collect::<BTreeMap<_,_>>(),"distinct_sizes":capture_stats.sizes.len(),"plaintext_leaks":capture_stats.leaks});
        notes.push(format!(
            "captured relay/client frames={}; unsigned GossipSub messages={}; signed={}",
            capture_stats.frames, capture_stats.unsigned_messages, capture_stats.signed_messages
        ));
    }
    let mut max_store = 0;
    let mut all_validations = vec![];
    let mut max_queue = 0;
    let mut max_peer_queue = 0;
    let mut seen_max = 0;
    let mut outcomes = HashMap::<String, u64>::new();
    for node in nodes.iter().chain(&retired_nodes) {
        if let Ok(s) = node.stats.lock() {
            if let Some(store) = &s.store {
                max_store = max_store.max(store.max_bytes);
            }
            all_validations.extend(s.validations.clone());
            max_queue = max_queue.max(s.max_queue);
            max_peer_queue = max_peer_queue.max(s.max_peer_queue);
            seen_max = seen_max.max(s.cache_len);
            for (k, v) in &s.outcomes {
                *outcomes.entry(k.clone()).or_default() += v;
            }
        }
    }
    result["store"]["max_bytes"] = json!(max_store);
    all_validations.sort_unstable_by_key(|(_, at, _)| *at);
    let injections = injections
        .lock()
        .map_err(|_| anyhow!("injections lock"))?
        .clone();
    let mut classified = 0;
    for injection in &injections {
        if injection.kind == "bad_signature" {
            let id = eid(&MOCK_NETWORK, &injection.wire)?;
            if readers.iter().any(|r| {
                r.lock().is_ok_and(|r| {
                    r.subscriber.rejected_eids.get(&id)
                        == Some(&mpe_core::wire::Error::BadSignature)
                })
            }) {
                result["rejected"]["bad_signature"] =
                    json!(result["rejected"]["bad_signature"].as_u64().unwrap_or(0) + 1);
                classified += 1;
            }
            continue;
        }
        let mid = message_id(&injection.wire);
        let found = all_validations
            .iter()
            .find(|(id, at, _)| *id == mid && *at >= injection.at);
        let category = found.and_then(|(_, _, out)| match out {
            Outcome::Reject(RejectReason::Oversize) => Some("oversize"),
            Outcome::Reject(RejectReason::BadAdmission) => Some("bad_admission"),
            Outcome::Reject(RejectReason::OverQuota) => Some("over_quota"),
            Outcome::Reject(_) => Some("malformed"),
            Outcome::Ignore(IgnoreReason::Replay) => Some("replay"),
            Outcome::Ignore(IgnoreReason::Expired) => Some("expired"),
            _ => None,
        });
        if let Some(category) = category {
            result["rejected"][category] =
                json!(result["rejected"][category].as_u64().unwrap_or(0) + 1);
            classified += 1;
        }
    }
    if args.scenario == "replay" {
        result["published"] = json!(injections.len());
        notes.push("Replay originals retransmitted at +62s after router duplicate cache; new slots preserve EID. One corrupted-slot front-run was sent before the first honest publication.".into());
    }
    if args.scenario == "spam" {
        let attack_ids: HashSet<_> = injections
            .iter()
            .filter_map(|i| eid(&MOCK_NETWORK, &i.wire).ok())
            .collect();
        let accepted: HashSet<_> = nodes
            .iter()
            .flat_map(|n| n.accepted_since(0))
            .filter(|a| attack_ids.contains(&a.eid))
            .map(|a| a.eid)
            .collect();
        let epochs: HashSet<_> = injections
            .iter()
            .filter_map(|i| {
                i.wire
                    .get(8..16)
                    .and_then(|b| b.try_into().ok())
                    .map(u64::from_be_bytes)
            })
            .collect();
        result["spam"] = json!({"attacker_published":injections.len(),"attacker_accepted":accepted.len(),"quota":64*epochs.len()});
        notes.push("Spam phase A uses one 100/s publisher into one ingress; phase B is separately reported and excluded from the phase A quota gate.".into());
    }
    if args.scenario == "eclipse" {
        let victim = nodes[0].accepted_since(0);
        let got = records
            .iter()
            .filter(|p| {
                victim.iter().any(|a| {
                    a.eid == p.eid
                        && a.at.saturating_duration_since(p.at) <= Duration::from_secs(10)
                })
            })
            .count();
        result["eclipse"] = json!({"attacker_peers":attacker_peers,"honest_peers":honest_peers,"victim_delivery_ratio":if records.is_empty(){0.}else{got as f64/records.len()as f64}});
        notes.push("20% listed withholding peers surround victim; scoring on; open mesh. No forged IHAVE generator or poisoned-dial-list variant.".into());
    }
    if let Some(late) = late {
        let expected_ids = backfill_expected
            .lock()
            .map_err(|_| anyhow!("backfill lock"))?;
        let reader = late.lock().map_err(|_| anyhow!("reader lock"))?;
        result["store"]["backfill_expected"] = json!(expected_ids.len());
        result["store"]["backfill_recovered"] = json!(expected_ids
            .iter()
            .filter(|eid| reader.backfill_eids.contains(*eid))
            .count());
        notes.push(format!(
            "Late subscriber store failovers={}; backfill-only recovery={}/{}",
            reader.failovers,
            expected_ids
                .iter()
                .filter(|id| reader.backfill_eids.contains(*id))
                .count(),
            expected_ids.len()
        ));
        let live: Vec<_> = records
            .iter()
            .filter(|p| {
                reader.join_at.is_some_and(|join| p.at >= join) && [0, 1, 2, 3].contains(&p.stream)
            })
            .collect();
        let got = live
            .iter()
            .filter(|p| reader.recognized.contains_key(&p.eid))
            .count();
        result["store"]["late_live_expected"] = json!(live.len());
        result["store"]["late_live_received"] = json!(got);
        result["store"]["late_live_ratio"] = json!(if live.is_empty() {
            1.
        } else {
            got as f64 / live.len() as f64
        });
        notes.push(format!("Late live delivery={got}/{}; feed starts at join head and runs during backfill; historical 0.427 minimum combined late-feed omissions with delayed sequential backfill.",live.len()));
    }
    if args.scenario == "fallback" {
        let (bytes, dropped) = ledger.metrics();
        result["fallback"] = json!({"published":records.len(),"delivered":received_ids.len(),"bytes_on_ledger":bytes,"events_dropped_over_limit":dropped});
        let mut f = Fallback::default();
        f.select_profile();
        let class3 = publishers[0].prepare(vec![0; 4000], Some(3), clock.now(), &mut rng)?;
        let refused = f.transaction(&class3.wire, clock.now()).is_err();
        notes.push(format!("Class 3 ledger attempt refused before transaction={refused}; burst=200 at +20s when duration>=20s; 6s blocks/3-block finality/1MB block usage/50KB state writes/1MiB tx/256B Misc payload/1KiB emitted-log cap."));
    }
    notes.push(format!("expected={expected}; received={received}; missing={}; completed latency observations={}; observation deadline={}s after publishing start",expected-received,latencies.len(),args.duration_secs+drain));
    notes.push(format!("first-honest-node adversarial outcomes classified={classified}/{}; unclassified includes router suppression, rate/backlog Ignore and valid bad-tag envelopes; honest+adversarial node outcomes={outcomes:?}",injections.len()));
    notes.push(format!("max outstanding verification jobs={max_queue}/128; max per peer={max_peer_queue}/8; largest application seen cache={seen_max}; cap=2000000; per-Shard feed cap=64MiB/50000 rows; expiry pruned; diagnostic validation ring cap=200000 (simulation feature only)"));
    notes.push(format!("unique Accepted honest bytes={unique_bytes}; receive amplification p50={:.3}; transmit amplification p50={:.3}",percentile(&incoming,0.5).unwrap_or(0.)/unique_bytes.max(1)as f64,percentile(&outgoing,0.5).unwrap_or(0.)/unique_bytes.max(1)as f64));
    notes.push(format!("Subscriber wire-envelope download bytes={network_bytes}; bytes/recognized pair={:.3}; daily per Subscriber extrapolation={:.0} B",network_bytes as f64/received.max(1)as f64,network_bytes as f64/subscriber_count as f64/args.duration_secs*86400.));
    if args.scenario == "leakage" {
        let a = readers[0].lock().map_err(|_| anyhow!("reader lock"))?;
        let trace = a.requests.clone();
        notes.push(format!("Recognition is a synchronous local API with no transport handle; interest-swapped request traces enforced by reconcile::repair_independent_of_keys unit test; this run captured {} gateway requests. No statistical paired timing test or log scanner.",trace.len()));
    }
    notes.push(format!(
        "wall_clock_run={:.3}s; ledger is a bounded mock, no Midnight devnet or fee measurement",
        run_started.elapsed().as_secs_f64()
    ));
    result["panics"] = json!(crate::PANICS.load(Ordering::Relaxed));
    result["notes"] = json!(notes);
    for node in nodes
        .iter()
        .chain(&retired_nodes)
        .chain(&clients)
        .chain(&attackers)
    {
        node.stop().await;
    }
    for task in tasks {
        if let Err(error) = task.await {
            if error.is_panic() {
                result["panics"] = json!(result["panics"].as_u64().unwrap_or(0) + 1);
            }
        }
    }
    Ok(result)
}

pub fn report_crypto() -> Result<Value> {
    let mut rng = ChaCha20Rng::seed_from_u64(42);
    let keys = StreamKeys::new(MOCK_NETWORK, bytes32(&mut rng), 1)?;
    let signer = SigningKey::from_bytes(&bytes32(&mut rng));
    let mut rows = vec![];
    for (class, &capacity) in CAPACITIES.iter().enumerate() {
        let event = EventIn {
            payload: vec![1; capacity],
            lei: [9; 16],
            seq: 1,
            schema: [1; 8],
            schema_version: 1,
            key_index: 0,
        };
        let mut seals = vec![];
        let mut opens = vec![];
        let mut tags = vec![];
        for _ in 0..100 {
            let t = Instant::now();
            let b = seal(&keys, &signer, &event, Some(class as u8), 100, &mut rng)?;
            seals.push(t.elapsed().as_secs_f64() * 1e6);
            let t = Instant::now();
            let _ = mpe_core::seal::open(&keys, &b, &[signer.verifying_key().to_bytes()], 100)?;
            opens.push(t.elapsed().as_secs_f64() * 1e6);
            let t = Instant::now();
            let _ = mpe_core::keys::matches(&keys.recognition(), &keys.network, &b[520..]);
            tags.push(t.elapsed().as_secs_f64() * 1e6);
        }
        rows.push(json!({"class":class,"body":mpe_core::wire::BODY_LENGTHS[class],"wire":520+mpe_core::wire::BODY_LENGTHS[class],"capacity":CAPACITIES[class],"seal_us_p50":percentile(&seals,0.5),"seal_us_p99":percentile(&seals,0.99),"open_us_p50":percentile(&opens,0.5),"open_us_p99":percentile(&opens,0.99),"tag_us_p50":percentile(&tags,0.5)}));
    }
    Ok(
        json!({"profile":"mpe-v1-sym","visible_fixed":8,"admission":512,"admission_fields":360,"salt":16,"nonce":12,"recognition_tag":16,"aead_authenticator":16,"sealed_prefix":40,"publisher_auth_block":70,"rows":rows,"notes":["100 operation samples per class; stand-in proof timing excluded; no allocator peak-state measurement; not Criterion."]}),
    )
}
