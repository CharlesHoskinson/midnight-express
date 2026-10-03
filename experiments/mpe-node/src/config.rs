use libp2p::gossipsub;
use mpe_core::wire::{hex, message_id, NetworkId};
use std::{
    collections::HashSet,
    net::{IpAddr, Ipv4Addr},
    time::Duration,
};
#[derive(Clone, Debug)]
pub struct MeshConfig {
    pub mesh: [usize; 4],
    pub idontwant: bool,
    pub eid_message_id: bool,
    pub p3: bool,
}
impl Default for MeshConfig {
    fn default() -> Self {
        Self {
            mesh: [8, 6, 12, 4],
            idontwant: true,
            eid_message_id: false,
            p3: false,
        }
    }
}
pub fn prefix(network: &NetworkId) -> String {
    format!("/mpe/{}/1", hex(&network[..8]))
}
pub fn topic(network: &NetworkId, shard: u8) -> gossipsub::IdentTopic {
    gossipsub::IdentTopic::new(format!("{}/shard/{shard}", prefix(network)))
}
pub fn router_config(
    options: &MeshConfig,
    network: NetworkId,
) -> Result<gossipsub::Config, String> {
    let [d, lo, hi, out] = options.mesh;
    if out >= lo || out > d / 2 {
        return Err("D_out must be below D_lo and at most D/2".into());
    }
    let eid_id = options.eid_message_id;
    let mut builder = gossipsub::ConfigBuilder::default();
    builder
        .protocol_id(
            format!("{}/gossipsub/1.2.0", prefix(&network)),
            gossipsub::Version::V1_2,
        )
        .mesh_n(d)
        .mesh_n_low(lo)
        .mesh_n_high(hi)
        .mesh_outbound_min(out)
        .heartbeat_interval(Duration::from_secs(1))
        .gossip_factor(0.25)
        .prune_backoff(Duration::from_secs(60))
        .flood_publish(false)
        .max_transmit_size(65536)
        .validation_mode(gossipsub::ValidationMode::Anonymous)
        .validate_messages()
        .idontwant_message_size_threshold(if options.idontwant { 1000 } else { 65537 })
        .message_id_fn(move |m| {
            let id = if eid_id {
                mpe_core::wire::eid(&network, &m.data).unwrap_or_else(|_| message_id(&m.data))
            } else {
                message_id(&m.data)
            };
            gossipsub::MessageId::from(id.to_vec())
        });
    builder.build().map_err(|e| e.to_string())
}
pub fn scoring(
    network: &NetworkId,
    shards: u8,
    p3: bool,
) -> (gossipsub::PeerScoreParams, gossipsub::PeerScoreThresholds) {
    let mut params = gossipsub::PeerScoreParams {
        topic_score_cap: 32.,
        app_specific_weight: 1.,
        ip_colocation_factor_weight: -10.,
        ip_colocation_factor_threshold: 10.,
        ip_colocation_factor_whitelist: HashSet::from([IpAddr::V4(Ipv4Addr::LOCALHOST)]),
        behaviour_penalty_weight: -10.,
        behaviour_penalty_threshold: 6.,
        behaviour_penalty_decay: 0.9,
        decay_interval: Duration::from_secs(1),
        decay_to_zero: 0.01,
        retain_score: Duration::from_secs(3600),
        ..Default::default()
    };
    for shard in 0..shards {
        params.topics.insert(
            topic(network, shard).hash(),
            gossipsub::TopicScoreParams {
                topic_weight: 1.,
                time_in_mesh_weight: 1. / 360.,
                time_in_mesh_quantum: Duration::from_secs(1),
                time_in_mesh_cap: 3600.,
                first_message_deliveries_weight: 1.,
                first_message_deliveries_decay: 0.99,
                first_message_deliveries_cap: 20.,
                mesh_message_deliveries_weight: if p3 { -1. } else { 0. },
                mesh_failure_penalty_weight: if p3 { -1. } else { 0. },
                invalid_message_deliveries_weight: -10.,
                invalid_message_deliveries_decay: 0.99,
                ..Default::default()
            },
        );
    }
    (
        params,
        gossipsub::PeerScoreThresholds {
            gossip_threshold: -10.,
            publish_threshold: -50.,
            graylist_threshold: -80.,
            accept_px_threshold: 100.,
            opportunistic_graft_threshold: 5.,
        },
    )
}
#[cfg(test)]
mod tests {
    use super::*;
    use mpe_core::wire::MOCK_NETWORK;
    #[test]
    fn mesh_tuple() {
        let c = router_config(&MeshConfig::default(), MOCK_NETWORK).unwrap();
        assert_eq!(
            (
                c.mesh_n(),
                c.mesh_n_low(),
                c.mesh_n_high(),
                c.mesh_outbound_min()
            ),
            (8, 6, 12, 4)
        );
        assert!(!c.flood_publish());
        assert_eq!(c.max_transmit_size(), 65536);
        assert!(matches!(
            c.validation_mode(),
            gossipsub::ValidationMode::Anonymous
        ));
    }
    #[test]
    fn reject_dout_ge_dlo() {
        let c = MeshConfig {
            mesh: [8, 4, 12, 4],
            ..Default::default()
        };
        assert!(router_config(&c, MOCK_NETWORK).is_err());
    }
    #[test]
    fn score_penalty_signs() {
        let (p, t) = scoring(&MOCK_NETWORK, 1, false);
        p.validate().unwrap();
        t.validate().unwrap();
        assert_eq!(p.ip_colocation_factor_weight, -10.);
        assert_eq!(p.ip_colocation_factor_threshold, 10.);
        let q = &p.topics[&topic(&MOCK_NETWORK, 0).hash()];
        assert_eq!(q.invalid_message_deliveries_weight, -10.);
        assert_eq!(q.mesh_message_deliveries_weight, 0.);
    }
    #[test]
    fn network_names_isolated() {
        assert_ne!(topic(&MOCK_NETWORK, 0).hash(), topic(&[1; 32], 0).hash());
    }
    #[test]
    fn msgid_distinct_for_slot_change() {
        let mut b = vec![0; 776];
        let a = message_id(&b);
        b[112] = 1;
        assert_ne!(a, message_id(&b));
        assert_eq!(message_id(&b), message_id(&b));
    }
}
