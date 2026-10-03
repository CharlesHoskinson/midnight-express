use serde_json::{json, Value};
pub fn percentile(values: &[f64], p: f64) -> Option<f64> {
    if values.is_empty() {
        return None;
    }
    let mut v = values.to_vec();
    v.sort_by(f64::total_cmp);
    let i = ((v.len() as f64 * p).ceil() as usize)
        .saturating_sub(1)
        .min(v.len() - 1);
    Some(v[i])
}
pub fn blank(scenario: &str, seed: u64, nodes: usize, duration: f64) -> Value {
    json!({"scenario":scenario,"seed":seed,"nodes":nodes,"duration_secs":duration,"published":0,"delivered":{"expected":0,"received":0,"ratio":null,"per_subscriber_min_ratio":null},"latency_ms":{"p50":null,"p95":null,"p99":null,"max":null},"duplicates":0,"rejected":{"malformed":0,"oversize":0,"bad_admission":0,"over_quota":0,"replay":0,"expired":0,"bad_signature":0},"panics":0,"wire":{"envelope_sizes":{},"distinct_sizes":0,"plaintext_leaks":0},"bandwidth":{"per_node_in_bytes_p50":0,"per_node_out_bytes_p50":0,"max_in":0,"max_out":0},"cpu_ms_per_node_p50":0.,"store":{"max_bytes":0,"backfill_expected":null,"backfill_recovered":null},"anchor":{"batches":null,"inclusion_proofs_checked":null,"inclusion_proofs_valid":null},"eclipse":{"attacker_peers":null,"honest_peers":null,"victim_delivery_ratio":null},"spam":{"attacker_published":null,"attacker_accepted":null,"quota":null},"fallback":{"published":null,"delivered":null,"bytes_on_ledger":null,"events_dropped_over_limit":null},"notes":[]})
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn percentiles_use_observations() {
        assert_eq!(percentile(&[1., 2., 3.], 0.99), Some(3.));
        assert_eq!(percentile(&[], 0.5), None);
    }
    #[test]
    fn fixed_schema() {
        let v = blank("baseline", 42, 50, 10.);
        for k in [
            "scenario",
            "seed",
            "nodes",
            "duration_secs",
            "published",
            "delivered",
            "latency_ms",
            "duplicates",
            "rejected",
            "panics",
            "wire",
            "bandwidth",
            "cpu_ms_per_node_p50",
            "store",
            "anchor",
            "eclipse",
            "spam",
            "fallback",
            "notes",
        ] {
            assert!(v.get(k).is_some(), "{k}");
        }
    }
}
