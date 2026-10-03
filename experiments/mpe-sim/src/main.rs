mod harness;
mod metrics;
use clap::{Parser, Subcommand};
use std::path::PathBuf;
#[derive(Parser)]
#[command(about = "MPE real-swarm proof of concept; admission and ledger are explicit mocks")]
struct Cli {
    #[command(subcommand)]
    command: Command,
}
#[derive(Subcommand)]
enum Command {
    Run(RunArgs),
    ReportCrypto {
        #[arg(long, default_value = "results/crypto.json")]
        out: PathBuf,
    },
    E2e {
        #[arg(long, default_value = "results/e2e.json")]
        out: PathBuf,
    },
}
#[derive(clap::Args, Clone, Debug)]
pub struct RunArgs {
    #[arg(long,value_parser=["baseline","spam","malformed","replay","eclipse","churn","backfill","anchor","leakage","fallback"])]
    pub scenario: String,
    #[arg(long, default_value_t = 50)]
    pub nodes: usize,
    #[arg(long, default_value_t = 42)]
    pub seed: u64,
    #[arg(long, default_value_t = 20.)]
    pub duration_secs: f64,
    #[arg(long)]
    pub out: PathBuf,
    #[arg(long, default_value = "8,6,12,4")]
    pub mesh: String,
    #[arg(long,default_value="on",value_parser=["on","off"])]
    pub idontwant: String,
    #[arg(long,default_value="wire",value_parser=["wire","eid"])]
    pub msgid: String,
    #[arg(long, default_value_t = 1)]
    pub shards: u8,
    #[arg(long, default_value_t = 4500)]
    pub verify_cost_us: u64,
    #[arg(long,default_value="nominal",value_parser=["nominal","bytecap","rate50"])]
    pub load: String,
    #[arg(long)]
    pub open: bool,
}
static PANICS: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);
#[tokio::main(flavor = "multi_thread")]
async fn main() -> anyhow::Result<()> {
    let previous = std::panic::take_hook();
    std::panic::set_hook(Box::new(move |info| {
        PANICS.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
        previous(info);
    }));
    let cli = Cli::parse();
    match cli.command {
        Command::Run(a) => {
            let out = a.out.clone();
            let result = harness::run(a).await?;
            write(out, result)?;
        }
        Command::ReportCrypto { out } => write(out, harness::report_crypto()?)?,
        Command::E2e { out } => {
            let args = RunArgs {
                scenario: "anchor".into(),
                nodes: 16,
                seed: 42,
                duration_secs: 20.,
                out: out.clone(),
                mesh: "8,6,12,4".into(),
                idontwant: "on".into(),
                msgid: "wire".into(),
                shards: 1,
                verify_cost_us: 4500,
                load: "nominal".into(),
                open: false,
            };
            let mut result = harness::run(args).await?;
            result["notes"].as_array_mut().unwrap().push(serde_json::json!("E2e runs genesis membership registration, publication, local recognition, restart/backfill roundtrip, finalized anchor and one contract reaction; see EID/LEI log entries."));
            write(out, result)?;
        }
    }
    Ok(())
}
fn write(out: PathBuf, result: serde_json::Value) -> anyhow::Result<()> {
    if let Some(parent) = out.parent() {
        if !parent.as_os_str().is_empty() {
            std::fs::create_dir_all(parent)?;
        }
    }
    std::fs::write(&out, serde_json::to_vec_pretty(&result)?)?;
    println!("{}", serde_json::to_string(&result)?);
    Ok(())
}
