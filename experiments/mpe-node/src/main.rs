use clap::Parser;
use libp2p::identity;
use mpe_core::{
    admission::{Member, RegistryView, RootRecord, StandInRln},
    clock::SimClock,
    wire::MOCK_NETWORK,
};
use mpe_node::{
    config::MeshConfig,
    node::{start, NodeOptions},
    protocols::Capture,
};
use std::{
    collections::HashSet,
    sync::Arc,
    time::{SystemTime, UNIX_EPOCH},
};
#[derive(Parser)]
struct Args {
    #[arg(long)]
    dial: Vec<String>,
    #[arg(long, default_value_t = 1)]
    shards: u8,
    #[arg(long)]
    open: bool,
}
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let a = Args::parse();
    let now = SystemTime::now().duration_since(UNIX_EPOCH)?.as_secs();
    let p = Arc::new(StandInRln::new(vec![Member::new([7; 32])]));
    let view = RegistryView {
        network: MOCK_NETWORK,
        roots: vec![RootRecord {
            root: [1; 32],
            period_start: now / 86400 * 86400,
            published_at: now.saturating_sub(1),
            superseded_at: None,
        }],
        finalized_time: now,
        shards: a.shards,
        bus_paused: false,
    };
    let (h, t) = start(NodeOptions {
        key: identity::Keypair::generate_ed25519(),
        proof: p,
        view,
        clock: Arc::new(SimClock::new(now)),
        mesh: MeshConfig::default(),
        subscribe: true,
        open: a.open,
        allowlist: HashSet::new(),
        withholding: false,
        heartbeat_interval: std::time::Duration::from_secs(1),
        verify_cost_us: 4500,
        global_verify: Arc::new(tokio::sync::Semaphore::new(1)),
        capture: Capture::default(),
    })
    .await?;
    println!(
        "peer={} listen={} restart_barrier=140s standin=true",
        h.peer, h.address
    );
    for addr in a.dial {
        h.dial(addr.parse()?).await?;
    }
    tokio::signal::ctrl_c().await?;
    h.stop().await;
    t.await?;
    Ok(())
}
