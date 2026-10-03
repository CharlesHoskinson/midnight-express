use crate::{
    config::{self, MeshConfig},
    protocols::{Capture, Codec, Request, Response},
    transport::{CountIo, Counters},
};
use anyhow::{anyhow, Result};
use futures::{future::poll_fn, StreamExt};
use libp2p::{
    core::upgrade,
    gossipsub, identity, noise, request_response,
    swarm::{NetworkBehaviour, SwarmEvent},
    tcp, yamux, Multiaddr, PeerId, StreamProtocol, Swarm, Transport,
};
use mpe_core::{
    admission::{AdmissionProof, RegistryView},
    anchor::{window, Batch},
    clock::Clock,
    ledger::{Action, Intent, LedgerAdapter, Misc, MockLedger, MockTx, TxStatus},
    scheduler::FairQueue,
    store::{MemStore, Store},
    validator::{IgnoreReason, Job, Outcome, Precheck, Validator},
    wire::Eid,
};
use std::{
    collections::{HashMap, HashSet, VecDeque},
    sync::{Arc, Mutex},
    time::{Duration, Instant},
};
use tokio::sync::{mpsc, oneshot, Semaphore};
#[derive(NetworkBehaviour)]
pub struct Behaviour {
    pub gossip: gossipsub::Behaviour,
    pub rpc: request_response::Behaviour<Codec>,
}
#[derive(Clone, Debug)]
pub struct Accepted {
    pub eid: Eid,
    pub wire: Vec<u8>,
    pub at: Instant,
    pub source: Option<PeerId>,
    pub cursor: u64,
}
#[derive(Default)]
pub struct NodeStats {
    pub accepted: FeedBuffer,
    pub outcomes: HashMap<String, u64>,
    pub cpu_ns: u64,
    pub scores: HashMap<PeerId, f64>,
    pub peers: HashSet<PeerId>,
    pub mesh: HashSet<PeerId>,
    pub max_queue: usize,
    pub max_peer_queue: usize,
    pub evidence: usize,
    #[cfg(feature = "diagnostics")]
    pub validations: VecDeque<(Eid, Instant, Outcome)>,
    pub cache_len: usize,
    pub publish_errors: u64,
    pub egress_by_class: [u64; 4],
    pub v12_peers: usize,
    pub store: Option<MemStore>,
}
#[derive(Clone)]
pub struct NodeHandle {
    pub peer: PeerId,
    pub address: Multiaddr,
    pub stats: Arc<Mutex<NodeStats>>,
    pub counters: Arc<Counters>,
    pub capture: Capture,
    commands: mpsc::Sender<Command>,
}
pub struct NodeOptions {
    pub key: identity::Keypair,
    pub proof: Arc<dyn AdmissionProof>,
    pub view: RegistryView,
    pub clock: Arc<dyn Clock>,
    pub mesh: MeshConfig,
    pub subscribe: bool,
    pub open: bool,
    pub allowlist: HashSet<PeerId>,
    pub withholding: bool,
    pub verify_cost_us: u64,
    pub heartbeat_interval: Duration,
    pub global_verify: Arc<Semaphore>,
    pub capture: Capture,
}
enum Command {
    Dial(Multiaddr),
    Rpc(PeerId, Request, oneshot::Sender<Result<Response, String>>),
    Inject(Vec<u8>, u8, bool, oneshot::Sender<Outcome>),
    Stop,
    UpdateView(RegistryView),
    Withhold(bool),
    UpdateAllowlist(HashSet<PeerId>),
    EnableStore(Box<MemStore>, oneshot::Sender<()>),
    EnableAnchoring(Arc<MockLedger>),
}
enum Source {
    Gossip(gossipsub::MessageId, PeerId),
    Publish(request_response::ResponseChannel<Response>),
    Local(oneshot::Sender<Outcome>, bool),
}
struct Pending {
    job: Job,
    source: Source,
}
struct Verified {
    pending: Pending,
    verdict: Option<mpe_core::admission::ProofVerdict>,
    cpu_ns: u64,
}
impl NodeHandle {
    pub fn is_stopped(&self) -> bool {
        self.commands.is_closed()
    }
    pub async fn dial(&self, address: Multiaddr) -> Result<()> {
        self.commands
            .send(Command::Dial(address))
            .await
            .map_err(|_| anyhow!("node stopped"))
    }
    pub async fn request(&self, peer: PeerId, r: Request) -> Result<Response, String> {
        let (tx, rx) = oneshot::channel();
        self.commands
            .send(Command::Rpc(peer, r, tx))
            .await
            .map_err(|_| "node stopped".to_string())?;
        tokio::time::timeout(Duration::from_secs(6), rx)
            .await
            .map_err(|_| "request timeout".to_string())?
            .map_err(|_| "node stopped".to_string())?
    }
    pub async fn inject(&self, bytes: Vec<u8>, shard: u8, raw: bool) -> Result<Outcome> {
        let (tx, rx) = oneshot::channel();
        self.commands
            .send(Command::Inject(bytes, shard, raw, tx))
            .await?;
        Ok(rx.await?)
    }
    pub async fn enable_store(&self, store: MemStore) -> Result<()> {
        let (tx, rx) = oneshot::channel();
        self.commands
            .send(Command::EnableStore(Box::new(store), tx))
            .await?;
        rx.await?;
        Ok(())
    }
    pub async fn enable_anchoring(&self, ledger: Arc<MockLedger>) {
        let _ = self.commands.send(Command::EnableAnchoring(ledger)).await;
    }
    pub async fn stop(&self) {
        let _ = self.commands.send(Command::Stop).await;
    }
    pub async fn update_view(&self, view: RegistryView) {
        let _ = self.commands.send(Command::UpdateView(view)).await;
    }
    pub async fn withhold(&self, value: bool) {
        let _ = self.commands.send(Command::Withhold(value)).await;
    }
    pub async fn update_allowlist(&self, peers: HashSet<PeerId>) {
        let _ = self.commands.send(Command::UpdateAllowlist(peers)).await;
    }
    pub fn feed_head(&self) -> u64 {
        self.stats.lock().map(|s| s.accepted.head).unwrap_or(0)
    }
    pub fn accepted_since(&self, after: u64) -> Vec<Accepted> {
        self.stats
            .lock()
            .map(|s| s.accepted.since(after))
            .unwrap_or_default()
    }
}
fn record(stats: &Arc<Mutex<NodeStats>>, out: &Outcome, _wire: &[u8]) {
    let key = match out {
        Outcome::Accept(_) => "Accept:ok".to_string(),
        Outcome::Reject(r) => format!("Reject:{r:?}"),
        Outcome::Ignore(r) => format!("Ignore:{r:?}"),
    };
    if let Ok(mut s) = stats.lock() {
        *s.outcomes.entry(key).or_default() += 1;
        #[cfg(feature = "diagnostics")]
        {
            if s.validations.len() == 200_000 {
                s.validations.pop_front();
            }
            s.validations.push_back((
                mpe_core::wire::message_id(_wire),
                Instant::now(),
                out.clone(),
            ));
        }
    }
}
fn outcome_to_gossip(out: &Outcome) -> gossipsub::MessageAcceptance {
    match out {
        Outcome::Accept(_) => gossipsub::MessageAcceptance::Accept,
        Outcome::Reject(_) => gossipsub::MessageAcceptance::Reject,
        Outcome::Ignore(_) => gossipsub::MessageAcceptance::Ignore,
    }
}
fn complete(
    swarm: &mut Swarm<Behaviour>,
    stats: &Arc<Mutex<NodeStats>>,
    capture: &Capture,
    network: &[u8; 32],
    pending: Pending,
    out: Outcome,
) {
    record(stats, &out, &pending.job.wire);
    let eid = match out {
        Outcome::Accept(eid) => Some(eid),
        _ => None,
    };
    if let Some(eid) = eid {
        if let Ok(mut s) = stats.lock() {
            if let Some(store) = &mut s.store {
                let _ = store.admit(
                    &pending.job.wire,
                    &eid,
                    pending.job.expiry.saturating_sub(mpe_core::wire::LIFETIME),
                );
            }
            s.accepted.push(Accepted {
                cursor: 0,
                eid,
                wire: pending.job.wire.clone(),
                at: Instant::now(),
                source: match &pending.source {
                    Source::Gossip(_, p) => Some(*p),
                    _ => None,
                },
            });
        }
    }
    match pending.source {
        Source::Gossip(mid, peer) => {
            let _ = swarm
                .behaviour_mut()
                .gossip
                .report_message_validation_result(&mid, &peer, outcome_to_gossip(&out));
        }
        Source::Publish(channel) => {
            if let Some(eid) = eid {
                let shard = pending.job.wire.get(2).copied().unwrap_or(0);
                capture.envelope(&pending.job.wire);
                if swarm
                    .behaviour_mut()
                    .gossip
                    .publish(config::topic(network, shard), pending.job.wire)
                    .is_err()
                {
                    if let Ok(mut s) = stats.lock() {
                        s.publish_errors += 1;
                    }
                }
                let _ = swarm
                    .behaviour_mut()
                    .rpc
                    .send_response(channel, Response::Accepted { eid });
            } else {
                let response = publish_refusal(&out);
                let _ = swarm.behaviour_mut().rpc.send_response(channel, response);
            }
        }
        Source::Local(tx, raw) => {
            if eid.is_some() || raw {
                let shard = pending.job.wire.get(2).copied().unwrap_or(0);
                capture.envelope(&pending.job.wire);
                let _ = swarm
                    .behaviour_mut()
                    .gossip
                    .publish(config::topic(network, shard), pending.job.wire);
            }
            let _ = tx.send(out);
        }
    }
}
pub async fn start(options: NodeOptions) -> Result<(NodeHandle, tokio::task::JoinHandle<()>)> {
    let peer = options.key.public().to_peer_id();
    let counters = Arc::new(Counters::default());
    let counted = counters.clone();
    let transport = tcp::tokio::Transport::new(tcp::Config::default().nodelay(true))
        .map(move |inner, _| CountIo {
            inner,
            counters: counted.clone(),
        })
        .upgrade(upgrade::Version::V1Lazy)
        .authenticate(noise::Config::new(&options.key)?)
        .multiplex(yamux::Config::default())
        .boxed();
    let mut router = gossipsub::ConfigBuilder::from(
        config::router_config(&options.mesh, options.view.network).map_err(|e| anyhow!(e))?,
    );
    router.mpe_egress_counters(counters.egress.clone());
    let mut gossip = gossipsub::Behaviour::new(
        gossipsub::MessageAuthenticity::Anonymous,
        router.build().map_err(|e| anyhow!(e))?,
    )
    .map_err(|e| anyhow!(e))?;
    let (params, thresholds) =
        config::scoring(&options.view.network, options.view.shards, options.mesh.p3);
    gossip
        .with_peer_score(params, thresholds)
        .map_err(|e| anyhow!(e))?;
    if options.subscribe {
        for shard in 0..options.view.shards {
            gossip.subscribe(&config::topic(&options.view.network, shard))?;
        }
    }
    let protocols = [
        "publish",
        "feed",
        "backfill",
        "inventory",
        "receipts",
        "anchor-leaves",
        "inclusion",
    ]
    .map(|suffix| {
        (
            StreamProtocol::try_from_owned(format!(
                "{}/{suffix}",
                config::prefix(&options.view.network)
            ))
            .expect("valid protocol literal"),
            request_response::ProtocolSupport::Full,
        )
    });
    let rpc = request_response::Behaviour::with_codec(
        Codec {
            capture: options.capture.clone(),
        },
        protocols,
        request_response::Config::default().with_request_timeout(Duration::from_secs(5)),
    );
    let mut swarm = Swarm::new(
        transport,
        Behaviour { gossip, rpc },
        peer,
        libp2p::swarm::Config::with_tokio_executor()
            .with_idle_connection_timeout(Duration::from_secs(600)),
    );
    swarm.listen_on("/ip4/127.0.0.1/tcp/0".parse()?)?;
    let (stats, commands) = (
        Arc::new(Mutex::new(NodeStats::default())),
        mpsc::channel(256),
    );
    let stats_task = stats.clone();
    let (tx, mut rx) = commands;
    let (ready_tx, ready_rx) = oneshot::channel();
    let capture = options.capture.clone();
    let handle_capture = capture.clone();
    let task = tokio::spawn(async move {
        let mut runtime = Runtime::new(options, stats_task, capture);
        let mut ready = Some(ready_tx);
        let mut heartbeat = tokio::time::interval(runtime.options.heartbeat_interval);
        loop {
            runtime.dispatch();
            tokio::select! {
                cmd = rx.recv() => {
                    if !runtime.command(&mut swarm, cmd) { break; }
                }
                Some(verified) = runtime.done_rx.recv() => runtime.verified(&mut swarm, verified),
                _ = heartbeat.tick() => runtime.heartbeat(&mut swarm),
                event = poll_fn(|cx| {
                    let t = Instant::now();
                    let polled = swarm.poll_next_unpin(cx);
                    if let Ok(mut s) = runtime.stats.lock() { s.cpu_ns += t.elapsed().as_nanos() as u64; }
                    polled
                }) => {
                    let Some(event) = event else { break; };
                    match event {
                        SwarmEvent::NewListenAddr { address, .. } => {
                            if let Some(tx) = ready.take() { let _ = tx.send(address); }
                        }
                        SwarmEvent::Behaviour(BehaviourEvent::Gossip(event)) => runtime.gossip(&mut swarm, event),
                        SwarmEvent::Behaviour(BehaviourEvent::Rpc(event)) => runtime.rpc(&mut swarm, event),
                        _ => {}
                    }
                }
            }
        }
    });
    let address = ready_rx.await.map_err(|_| anyhow!("listener failed"))?;
    Ok((
        NodeHandle {
            peer,
            address,
            stats,
            counters,
            capture: handle_capture,
            commands: tx,
        },
        task,
    ))
}

const FEED_BYTES_PER_SHARD: usize = 64 * 1024 * 1024;
const FEED_ROWS_PER_SHARD: usize = 50_000;
/// Absolute cursors survive ring eviction; the simulator never treats a cursor as a row offset.
#[derive(Default)]
pub struct FeedBuffer {
    shards: HashMap<u8, VecDeque<Accepted>>,
    bytes: HashMap<u8, usize>,
    head: u64,
}
impl FeedBuffer {
    fn push(&mut self, mut accepted: Accepted) {
        let Some(&shard) = accepted.wire.get(2) else {
            return;
        };
        self.head += 1;
        accepted.cursor = self.head;
        let size = self.bytes.entry(shard).or_default();
        let ring = self.shards.entry(shard).or_default();
        *size += accepted.wire.len();
        ring.push_back(accepted);
        while *size > FEED_BYTES_PER_SHARD || ring.len() > FEED_ROWS_PER_SHARD {
            if let Some(old) = ring.pop_front() {
                *size -= old.wire.len();
            }
        }
    }
    fn prune(&mut self, now: u64) {
        for (shard, ring) in &mut self.shards {
            ring.retain(|a| {
                a.wire
                    .get(4..8)
                    .and_then(|b| b.try_into().ok())
                    .is_some_and(|b| u64::from(u32::from_be_bytes(b)) >= now)
            });
            self.bytes
                .insert(*shard, ring.iter().map(|a| a.wire.len()).sum());
        }
    }
    fn since(&self, after: u64) -> Vec<Accepted> {
        let mut rows: Vec<_> = self
            .shards
            .values()
            .flatten()
            .filter(|a| a.cursor > after)
            .cloned()
            .collect();
        rows.sort_unstable_by_key(|a| a.cursor);
        rows
    }
    fn page(&self, shard: u8, after: u64) -> Response {
        let mut cursor = after;
        let mut size = 0;
        let mut envelopes = vec![];
        if let Some(ring) = self.shards.get(&shard) {
            for a in ring.iter().filter(|a| a.cursor > after) {
                if size + a.wire.len() * 2 > 60_000 {
                    break;
                }
                size += a.wire.len() * 2;
                cursor = a.cursor;
                envelopes.push(a.wire.clone());
            }
        }
        Response::Feed { cursor, envelopes }
    }
}
fn publish_refusal(out: &Outcome) -> Response {
    match out {
        Outcome::Ignore(
            IgnoreReason::Busy | IgnoreReason::Restart | IgnoreReason::Rate | IgnoreReason::Stale,
        ) => Response::Busy,
        _ => Response::Refused,
    }
}
#[derive(Default)]
struct Eviction {
    loaded_without_delivery: HashMap<PeerId, u32>,
    until: HashMap<PeerId, Instant>,
}
impl Eviction {
    fn tick(&mut self, mesh: &[PeerId], firsts: &HashSet<PeerId>, loaded: bool, now: Instant) {
        self.until.retain(|_, until| *until > now);
        self.loaded_without_delivery
            .retain(|peer, _| mesh.contains(peer));
        if !loaded {
            return;
        }
        for peer in mesh {
            let count = self.loaded_without_delivery.entry(*peer).or_default();
            if firsts.contains(peer) {
                *count = 0;
            } else {
                *count += 1;
            }
            if *count >= 90 {
                self.until
                    .entry(*peer)
                    .or_insert(now + Duration::from_secs(60));
                *count = 0;
            }
        }
    }
    fn application_score(&self, peer: &PeerId, listed: bool, now: Instant) -> f64 {
        if !listed || self.until.get(peer).is_some_and(|until| *until > now) {
            -20.
        } else {
            0.
        }
    }
}
/// Keeps ownership of the pending job outside spawn_blocking. Drop posts completion even on panic/abort.
struct CompletionGuard {
    completion: Option<Verified>,
    done: mpsc::UnboundedSender<Verified>,
}
impl Drop for CompletionGuard {
    fn drop(&mut self) {
        if let Some(completion) = self.completion.take() {
            let _ = self.done.send(completion);
        }
    }
}
struct Runtime {
    options: NodeOptions,
    stats: Arc<Mutex<NodeStats>>,
    capture: Capture,
    validator: Validator,
    queue: FairQueue<Pending>,
    done_tx: mpsc::UnboundedSender<Verified>,
    done_rx: mpsc::UnboundedReceiver<Verified>,
    waiting:
        HashMap<request_response::OutboundRequestId, oneshot::Sender<Result<Response, String>>>,
    busy: bool,
    loaded: bool,
    firsts: HashSet<PeerId>,
    eviction: Eviction,
    ledger: Option<Arc<MockLedger>>,
    batches: HashMap<u64, Batch>,
    anchor_tickets: HashMap<u64, u64>,
    anchor_leaves: HashMap<u64, Vec<Vec<Eid>>>,
}
impl Runtime {
    fn new(options: NodeOptions, stats: Arc<Mutex<NodeStats>>, capture: Capture) -> Self {
        let validator = Validator::new(
            options.proof.clone(),
            options.view.clone(),
            options.clock.now(),
        );
        let (done_tx, done_rx) = mpsc::unbounded_channel();
        Self {
            options,
            stats,
            capture,
            validator,
            queue: FairQueue::default(),
            done_tx,
            done_rx,
            waiting: HashMap::new(),
            busy: false,
            loaded: false,
            firsts: HashSet::new(),
            eviction: Eviction::default(),
            ledger: None,
            batches: HashMap::new(),
            anchor_tickets: HashMap::new(),
            anchor_leaves: HashMap::new(),
        }
    }
    fn dispatch(&mut self) {
        if self.busy {
            return;
        }
        let Some((_, pending)) = self.queue.dispatch() else {
            return;
        };
        self.busy = true;
        let proof = self.options.proof.clone();
        let view = self.validator.view.clone();
        let cost = self.options.verify_cost_us;
        let gate = self.options.global_verify.clone();
        let guard = CompletionGuard {
            completion: Some(Verified {
                pending,
                verdict: None,
                cpu_ns: 0,
            }),
            done: self.done_tx.clone(),
        };
        tokio::spawn(async move {
            let mut guard = guard;
            let Ok(_permit) = gate.acquire_owned().await else {
                return;
            };
            let job = guard
                .completion
                .as_ref()
                .expect("completion owned until drop")
                .pending
                .job
                .clone();
            let result = tokio::task::spawn_blocking(move || {
                let t = Instant::now();
                let verdict = proof.verify(&job.public, &job.wire[112..368], &view);
                while t.elapsed().as_micros() < cost as u128 {
                    std::hint::spin_loop();
                }
                (verdict, t.elapsed().as_nanos() as u64)
            })
            .await;
            if let Ok((verdict, cpu_ns)) = result {
                if let Some(completion) = &mut guard.completion {
                    completion.verdict = Some(verdict);
                    completion.cpu_ns = cpu_ns;
                }
            }
        });
    }
    fn command(&mut self, swarm: &mut Swarm<Behaviour>, command: Option<Command>) -> bool {
        match command {
            Some(Command::Stop) | None => return false,
            Some(Command::Dial(addr)) => {
                let _ = swarm.dial(addr);
            }
            Some(Command::UpdateView(view)) => self.validator.view = view,
            Some(Command::UpdateAllowlist(peers)) => self.options.allowlist = peers,
            Some(Command::Withhold(value)) => self.options.withholding = value,
            Some(Command::EnableAnchoring(ledger)) => self.ledger = Some(ledger),
            Some(Command::EnableStore(store, tx)) => {
                if let Ok(mut s) = self.stats.lock() {
                    s.store = Some(*store);
                }
                let _ = tx.send(());
            }
            Some(Command::Rpc(peer, request, tx)) => {
                let id = swarm.behaviour_mut().rpc.send_request(&peer, request);
                self.waiting.insert(id, tx);
            }
            Some(Command::Inject(bytes, shard, raw, tx)) => {
                if raw {
                    self.capture.envelope(&bytes);
                    let result = swarm
                        .behaviour_mut()
                        .gossip
                        .publish(config::topic(&self.validator.view.network, shard), bytes);
                    let _ = tx.send(if result.is_ok() {
                        Outcome::Accept([0; 32])
                    } else {
                        Outcome::Ignore(IgnoreReason::Busy)
                    });
                } else {
                    self.offer(
                        swarm,
                        bytes,
                        shard,
                        "local".into(),
                        Source::Local(tx, false),
                    );
                }
            }
        }
        true
    }
    fn offer(
        &mut self,
        swarm: &mut Swarm<Behaviour>,
        bytes: Vec<u8>,
        shard: u8,
        peer: String,
        source: Source,
    ) {
        match self
            .validator
            .precheck(&bytes, 1, shard, &peer, self.options.clock.now())
        {
            Precheck::Done(out) => {
                record(&self.stats, &out, &bytes);
                match source {
                    Source::Gossip(mid, peer) => {
                        let _ = swarm
                            .behaviour_mut()
                            .gossip
                            .report_message_validation_result(&mid, &peer, outcome_to_gossip(&out));
                    }
                    Source::Publish(channel) => {
                        let _ = swarm
                            .behaviour_mut()
                            .rpc
                            .send_response(channel, publish_refusal(&out));
                    }
                    Source::Local(tx, _) => {
                        let _ = tx.send(out);
                    }
                }
            }
            Precheck::NeedsProof(job) => {
                let pending = Pending { job, source };
                if let Err(pending) = self.queue.enqueue(peer, pending) {
                    complete(
                        swarm,
                        &self.stats,
                        &self.capture,
                        &self.validator.view.network,
                        pending,
                        Outcome::Ignore(IgnoreReason::Busy),
                    );
                }
            }
        }
    }
    fn verified(&mut self, swarm: &mut Swarm<Behaviour>, verified: Verified) {
        self.busy = false;
        self.queue.complete(&verified.pending.job.peer);
        if let Ok(mut s) = self.stats.lock() {
            s.cpu_ns += verified.cpu_ns;
        }
        let out = if let Some(verdict) = verified.verdict {
            self.validator.finish(
                verified.pending.job.clone(),
                verdict,
                self.options.clock.now(),
            )
        } else {
            Outcome::Ignore(IgnoreReason::Busy)
        };
        if let Outcome::Accept(eid) = &out {
            self.loaded = true;
            if let Source::Gossip(_, peer) = &verified.pending.source {
                self.firsts.insert(*peer);
            }
            if self.ledger.is_some() {
                if let Ok(env) = mpe_core::wire::Envelope::parse(&verified.pending.job.wire) {
                    let w = window(env.header.expiry);
                    if !self.anchor_tickets.contains_key(&w) {
                        let leaves = self
                            .anchor_leaves
                            .entry(w)
                            .or_insert_with(|| vec![vec![]; self.validator.view.shards as usize]);
                        if let Some(shard) = leaves.get_mut(env.header.shard as usize) {
                            shard.push(*eid);
                        }
                    }
                }
            }
        }
        complete(
            swarm,
            &self.stats,
            &self.capture,
            &self.validator.view.network,
            verified.pending,
            out,
        );
    }
    fn anchor(&mut self) {
        let Some(adapter) = &self.ledger else {
            return;
        };
        let now = self.options.clock.now();
        let ready: Vec<_> = self
            .anchor_leaves
            .keys()
            .copied()
            .filter(|w| now >= (w + 1) * 60 + 20)
            .collect();
        for w in ready {
            let Some(leaves) = self.anchor_leaves.remove(&w) else {
                continue;
            };
            let Ok(batch) = Batch::new(w, leaves) else {
                continue;
            };
            let Ok(payload) = batch.payload.encode() else {
                continue;
            };
            let Ok(misc) = Misc::new(b"mpe/anchor/v1", payload) else {
                continue;
            };
            let tx = MockTx {
                contract: [0x42; 32],
                intents: vec![Intent {
                    id: 0,
                    guaranteed: true,
                    succeeds: true,
                    events: vec![misc],
                }],
                action: Action::Anchor(batch.payload.clone()),
                ttl: now + 600,
                fee: 1,
            };
            if let Ok(ticket) = adapter.submit(tx) {
                self.anchor_tickets.insert(w, ticket);
                self.batches.insert(w, batch);
            }
        }
        self.batches
            .retain(|w, _| now.saturating_sub(w * 60) <= 176400);
        self.anchor_tickets
            .retain(|w, _| now.saturating_sub(w * 60) <= 176400);
    }
    fn heartbeat(&mut self, swarm: &mut Swarm<Behaviour>) {
        self.anchor();
        self.validator.prune(self.options.clock.now());
        let peers: Vec<_> = swarm.connected_peers().copied().collect();
        let mesh: Vec<_> = swarm
            .behaviour()
            .gossip
            .mesh_peers(&config::topic(&self.validator.view.network, 0).hash())
            .copied()
            .collect();
        self.eviction
            .tick(&mesh, &self.firsts, self.loaded, Instant::now());
        for peer in &peers {
            let listed = self.options.open || self.options.allowlist.contains(peer);
            let score = self
                .eviction
                .application_score(peer, listed, Instant::now());
            let _ = swarm
                .behaviour_mut()
                .gossip
                .set_application_score(peer, score);
        }
        self.loaded = false;
        self.firsts.clear();
        if let Ok(mut s) = self.stats.lock() {
            if let Some(store) = &mut s.store {
                store.prune(self.options.clock.now());
            }
            s.accepted.prune(self.options.clock.now());
            s.v12_peers = swarm
                .behaviour()
                .gossip
                .peer_protocol()
                .filter(|(_, kind)| **kind == gossipsub::PeerKind::Gossipsubv1_2)
                .count();
            s.peers = peers.into_iter().collect();
            s.mesh = mesh.into_iter().collect();
            s.scores = s
                .peers
                .iter()
                .filter_map(|p| {
                    swarm
                        .behaviour()
                        .gossip
                        .peer_score(p)
                        .map(|score| (*p, score))
                })
                .collect();
            s.max_queue = self.queue.max_total;
            s.max_peer_queue = self.queue.max_peer;
            s.evidence = self.validator.evidence.len();
            s.cache_len = self.validator.cache_len();
        }
    }
    fn gossip(&mut self, swarm: &mut Swarm<Behaviour>, event: gossipsub::Event) {
        if let gossipsub::Event::Message {
            propagation_source,
            message_id,
            message,
        } = event
        {
            self.capture.envelope(&message.data);
            if let Ok(mut s) = self.capture.stats.lock() {
                if message.source.is_none() && message.sequence_number.is_none() {
                    s.unsigned_messages += 1;
                } else {
                    s.signed_messages += 1;
                }
            }
            if self.options.withholding {
                let _ = swarm
                    .behaviour_mut()
                    .gossip
                    .report_message_validation_result(
                        &message_id,
                        &propagation_source,
                        gossipsub::MessageAcceptance::Ignore,
                    );
                return;
            }
            let shard = (0..self.validator.view.shards)
                .find(|s| config::topic(&self.validator.view.network, *s).hash() == message.topic)
                .unwrap_or(u8::MAX);
            self.offer(
                swarm,
                message.data,
                shard,
                propagation_source.to_string(),
                Source::Gossip(message_id, propagation_source),
            );
        }
    }
    fn rpc(
        &mut self,
        swarm: &mut Swarm<Behaviour>,
        event: request_response::Event<Request, Response>,
    ) {
        match event {
            request_response::Event::Message { peer, message, .. } => match message {
                request_response::Message::Request {
                    request, channel, ..
                } => {
                    if let Request::Publish(bytes) = request {
                        let shard = bytes.get(2).copied().unwrap_or(u8::MAX);
                        self.offer(
                            swarm,
                            bytes,
                            shard,
                            peer.to_string(),
                            Source::Publish(channel),
                        );
                        return;
                    }
                    let response = self.service(request);
                    let _ = swarm.behaviour_mut().rpc.send_response(channel, response);
                }
                request_response::Message::Response {
                    request_id,
                    response,
                } => {
                    if let Some(tx) = self.waiting.remove(&request_id) {
                        let _ = tx.send(Ok(response));
                    }
                }
            },
            request_response::Event::OutboundFailure {
                request_id, error, ..
            } => {
                if let Some(tx) = self.waiting.remove(&request_id) {
                    let _ = tx.send(Err(error.to_string()));
                }
            }
            _ => {}
        }
    }
    fn service(&self, request: Request) -> Response {
        match request {
            Request::AnchorLeaves { window, shard } => self
                .batches
                .get(&window)
                .and_then(|b| b.leaves.get(shard as usize))
                .cloned()
                .map(Response::AnchorLeaves)
                .unwrap_or(Response::Refused),
            Request::Inclusion { eid } => self
                .batches
                .iter()
                .find_map(|(w, b)| {
                    let ticket = self.anchor_tickets.get(w)?;
                    if !self
                        .ledger
                        .as_ref()
                        .is_some_and(|l| matches!(l.tx_status(ticket), Ok(TxStatus::Final(_))))
                    {
                        return None;
                    }
                    b.inclusion(&eid).ok()
                })
                .map(Response::Inclusion)
                .unwrap_or(Response::Refused),
            Request::Backfill { shard, from, until } => self
                .stats
                .lock()
                .ok()
                .and_then(|s| {
                    s.store
                        .as_ref()
                        .and_then(|store| store.page(shard, from, until, 64).ok())
                })
                .map(Response::Backfill)
                .unwrap_or(Response::Refused),
            Request::Inventory {
                shard,
                window,
                after,
            } => self
                .stats
                .lock()
                .ok()
                .and_then(|s| {
                    s.store
                        .as_ref()
                        .and_then(|store| store.inventory(shard, window, after, 64).ok())
                })
                .map(Response::Inventory)
                .unwrap_or(Response::Refused),
            Request::Receipts {
                shard,
                window,
                after,
            } => self
                .stats
                .lock()
                .ok()
                .and_then(|s| {
                    s.store.as_ref().map(|store| {
                        let (receipts, next) = store.receipts_page(shard, window, after, 64);
                        Response::Receipts { receipts, next }
                    })
                })
                .unwrap_or(Response::Refused),
            Request::Feed { shard, after } => self
                .stats
                .lock()
                .ok()
                .map(|s| s.accepted.page(shard, after))
                .unwrap_or(Response::Refused),
            Request::Publish(_) => Response::Refused,
        }
    }
}

#[cfg(test)]
mod repair_tests {
    use super::*;
    #[test]
    fn eviction_deadline_survives_allowlist_heartbeats() {
        let silent = PeerId::random();
        let useful = PeerId::random();
        let now = Instant::now();
        let mut eviction = Eviction::default();
        for tick in 0..300 {
            eviction.tick(
                &[silent, useful],
                &HashSet::from([useful]),
                true,
                now + Duration::from_millis(tick),
            );
        }
        assert_eq!(
            eviction.application_score(&silent, true, now + Duration::from_secs(1)),
            -20.
        );
        assert_eq!(
            eviction.application_score(&useful, true, now + Duration::from_secs(1)),
            0.
        );
        eviction.tick(
            &[silent, useful],
            &HashSet::new(),
            false,
            now + Duration::from_secs(59),
        );
        assert_eq!(
            eviction.application_score(&silent, true, now + Duration::from_secs(59)),
            -20.
        );
        assert_eq!(
            eviction.application_score(&silent, true, now + Duration::from_secs(61)),
            0.
        );
    }
    #[test]
    fn feed_ring_caps_and_expiry_preserve_absolute_cursors() {
        let mut feed = FeedBuffer::default();
        for n in 0..50_010 {
            let mut wire = vec![0; 776];
            wire[2] = 0;
            wire[4..8].copy_from_slice(&1000_u32.to_be_bytes());
            feed.push(Accepted {
                eid: [0; 32],
                wire,
                at: Instant::now(),
                source: None,
                cursor: n,
            });
        }
        assert_eq!(feed.shards[&0].len(), 50_000);
        assert_eq!(
            feed.since(50_008)
                .iter()
                .map(|a| a.cursor)
                .collect::<Vec<_>>(),
            vec![50_009, 50_010]
        );
        feed.prune(1001);
        assert!(feed.since(0).is_empty());
        assert_eq!(feed.head, 50_010);
    }
    #[tokio::test]
    async fn completion_guard_posts_busy_when_verifier_is_aborted() {
        let (tx, mut rx) = mpsc::unbounded_channel();
        let (reply, _) = oneshot::channel();
        let public = mpe_core::admission::AdmissionPublic {
            network: [0; 32],
            root: [0; 32],
            epoch: 0,
            size_class: 0,
            eid: [0; 32],
            nullifier: [0; 32],
            share_y: [0; 32],
        };
        let pending = Pending {
            job: Job {
                public,
                wire: vec![],
                expiry: 0,
                peer: "p".into(),
            },
            source: Source::Local(reply, false),
        };
        let guard = CompletionGuard {
            completion: Some(Verified {
                pending,
                verdict: None,
                cpu_ns: 0,
            }),
            done: tx,
        };
        let task = tokio::spawn(async move {
            let _guard = guard;
            std::future::pending::<()>().await;
        });
        tokio::task::yield_now().await;
        task.abort();
        let _ = task.await;
        let completion = tokio::time::timeout(Duration::from_secs(1), rx.recv())
            .await
            .unwrap()
            .unwrap();
        assert!(completion.verdict.is_none());
        assert_eq!(completion.pending.job.peer, "p");
    }
}
