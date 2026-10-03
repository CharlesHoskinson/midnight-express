use crate::{
    admission::{RegistryView, RootRecord},
    anchor::{AnchorPayload, InclusionProof},
    wire::{hash, Eid, Error, NetworkId},
};
use ed25519_dalek::{Signature, VerifyingKey};
use serde::{Deserialize, Serialize};
use std::{
    collections::{HashMap, HashSet, VecDeque},
    sync::Mutex,
};
pub type ContractAddress = [u8; 32];
pub type TxTicket = u64;
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct RelayEntry {
    pub peer_id: String,
    pub operator: [u8; 32],
    pub relay: bool,
    pub store: bool,
    pub bootstrapper: bool,
    pub gateway: bool,
    pub anchorer: bool,
}
#[derive(Clone, Debug)]
pub struct RegistryParams {
    pub shards: u8,
    pub max_version: u8,
    pub bootstrap_hash: [u8; 32],
}
#[derive(Clone, Debug)]
pub struct LedgerParams {
    pub block_secs: u64,
    pub finality_blocks: u64,
    pub block_usage: usize,
    pub bytes_written: usize,
    pub tx_limit: usize,
    pub log_limit: usize,
    pub intent_ttl: u64,
    pub pool_longevity: u64,
}
impl Default for LedgerParams {
    fn default() -> Self {
        Self {
            block_secs: 6,
            finality_blocks: 3,
            block_usage: 1_000_000,
            bytes_written: 50_000,
            tx_limit: 1_048_576,
            log_limit: 1024,
            intent_ttl: 1_209_600,
            pool_longevity: 600,
        }
    }
}
#[derive(Clone, Debug)]
pub struct BlockRef {
    pub height: u64,
    pub time: u64,
    pub hash: [u8; 32],
}
#[derive(Clone, Debug)]
pub struct AnchorRecord {
    pub payload: AnchorPayload,
    pub height: u64,
    pub time: u64,
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Misc {
    pub name: [u8; 32],
    pub payload: Vec<u8>,
}
impl Misc {
    pub fn new(name: &[u8], payload: Vec<u8>) -> Result<Self, Error> {
        if name.len() > 32 || payload.len() > 256 {
            return Err(Error::Malformed);
        }
        let mut n = [0; 32];
        n[..name.len()].copy_from_slice(name);
        Ok(Self { name: n, payload })
    }
}
#[derive(Clone, Debug)]
pub struct Intent {
    pub id: u32,
    pub guaranteed: bool,
    pub succeeds: bool,
    pub events: Vec<Misc>,
}
#[derive(Clone, Debug)]
pub struct ContractEvent {
    pub id: u64,
    pub contract: ContractAddress,
    pub tx: u64,
    pub intent: u32,
    pub ordinal: u32,
    pub misc: Misc,
    pub height: u64,
}
#[derive(Clone, Debug)]
pub struct Reaction {
    pub statement: Vec<u8>,
    pub signature: Vec<u8>,
    pub nullifier: Eid,
    pub inclusion: Option<InclusionProof>,
}

#[derive(Clone, Debug)]
pub enum RegistryWrite {
    Root(RootRecord),
    Relays(Vec<RelayEntry>),
    Params(RegistryParams),
    Pause(bool),
}
#[derive(Clone, Debug)]
pub enum Action {
    Events,
    Registry(RegistryWrite),
    Anchor(AnchorPayload),
    Reaction(Box<Reaction>),
}
#[derive(Clone, Debug)]
pub struct MockTx {
    pub contract: ContractAddress,
    pub intents: Vec<Intent>,
    pub action: Action,
    pub ttl: u64,
    pub fee: u64,
}
impl MockTx {
    pub fn size(&self) -> usize {
        8192 + 288 * self.intents.iter().map(|i| i.events.len()).sum::<usize>()
    }
    pub fn state_bytes(&self) -> usize {
        match &self.action {
            Action::Registry(RegistryWrite::Root(_)) => 64,
            Action::Registry(RegistryWrite::Relays(r)) => r.len() * 128,
            Action::Registry(_) => 64,
            Action::Anchor(a) => 40 + a.counts.len() * 4,
            Action::Reaction(_) => 64,
            Action::Events => 0,
        }
    }
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum TxStatus {
    Pending,
    Included(u64),
    Final(u64),
    Failed,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq, thiserror::Error)]
pub enum LedgerError {
    #[error("ledger unavailable")]
    Unavailable,
    #[error("ledger paused")]
    Paused,
    #[error("transaction limit exceeded")]
    Limit,
    #[error("invalid transaction")]
    Invalid,
}
pub trait LedgerAdapter: Send + Sync {
    fn finalized_head(&self) -> Result<BlockRef, LedgerError>;
    fn membership_roots(&self) -> Result<Vec<RootRecord>, LedgerError>;
    fn historic_root(&self, root: &[u8; 32], now: u64) -> Result<Option<RootRecord>, LedgerError>;
    fn relay_list(&self) -> Result<Vec<RelayEntry>, LedgerError>;
    fn registry_params(&self) -> Result<RegistryParams, LedgerError>;
    fn anchors(&self, from: u64) -> Result<Vec<AnchorRecord>, LedgerError>;
    fn bus_paused(&self) -> Result<bool, LedgerError>;
    fn ledger_parameters(&self) -> Result<LedgerParams, LedgerError>;
    fn submit(&self, tx: MockTx) -> Result<TxTicket, LedgerError>;
    fn tx_status(&self, t: &TxTicket) -> Result<TxStatus, LedgerError>;
    fn staleness(&self, now: u64) -> Result<bool, LedgerError> {
        Ok(now.abs_diff(self.finalized_head()?.time) > 60)
    }
}
#[derive(Clone)]
pub struct RegistryState {
    pub roots: Vec<RootRecord>,
    pub relays: Vec<RelayEntry>,
    pub params: RegistryParams,
    pub anchors: Vec<AnchorRecord>,
    pub paused: bool,
}
struct PendingTx {
    ticket: u64,
    tx: MockTx,
    submitted: u64,
}
struct Block {
    height: u64,
    time: u64,
    writes: Vec<RegistryWrite>,
    anchors: Vec<AnchorPayload>,
}
pub struct MockContract {
    pub publishers: HashSet<[u8; 32]>,
    pub action: [u8; 32],
    pub nullifiers: HashSet<Eid>,
    pub effects: Vec<Eid>,
}
struct State {
    network: NetworkId,
    head: u64,
    base: u64,
    last_block: u64,
    registry: RegistryState,
    params: LedgerParams,
    pool: VecDeque<PendingTx>,
    blocks: Vec<Block>,
    statuses: HashMap<u64, TxStatus>,
    next_tx: u64,
    events: Vec<ContractEvent>,
    contracts: HashMap<ContractAddress, MockContract>,
    reaction_witnesses: HashMap<Eid, (Eid, Eid, u64)>,
    freeze: bool,
    pub bytes_on_ledger: u64,
    pub dropped: u64,
}
pub struct MockLedger {
    state: Mutex<State>,
}
impl MockLedger {
    pub fn new(
        network: NetworkId,
        base: u64,
        roots: Vec<RootRecord>,
        relays: Vec<RelayEntry>,
        shards: u8,
    ) -> Self {
        Self {
            state: Mutex::new(State {
                network,
                head: 0,
                base,
                last_block: base,
                registry: RegistryState {
                    roots,
                    relays,
                    params: RegistryParams {
                        shards,
                        max_version: 1,
                        bootstrap_hash: [0; 32],
                    },
                    anchors: vec![],
                    paused: false,
                },
                params: LedgerParams::default(),
                pool: VecDeque::new(),
                blocks: vec![],
                statuses: HashMap::new(),
                next_tx: 1,
                events: vec![],
                contracts: HashMap::new(),
                reaction_witnesses: HashMap::new(),
                freeze: false,
                bytes_on_ledger: 0,
                dropped: 0,
            }),
        }
    }
    /// Trusted mock setup, outside the transaction. A real contract needs a ZK nullifier/body relation proof.
    pub fn register_reaction_witness(
        &self,
        statement: &[u8],
        eid: Eid,
        nullifier: Eid,
        expiry: u64,
    ) {
        if let Ok(mut s) = self.state.lock() {
            let now = s.last_block;
            s.reaction_witnesses
                .retain(|_, (_, _, until)| *until >= now);
            if s.reaction_witnesses.len() < 10_000 {
                s.reaction_witnesses
                    .insert(hash(&[statement]), (eid, nullifier, expiry));
            }
        }
    }
    pub fn freeze(&self, value: bool) {
        if let Ok(mut s) = self.state.lock() {
            s.freeze = value;
        }
    }
    pub fn add_contract(&self, address: ContractAddress, contract: MockContract) {
        if let Ok(mut s) = self.state.lock() {
            s.contracts.insert(address, contract);
        }
    }
    pub fn effect_count(&self, address: &ContractAddress) -> usize {
        self.state
            .lock()
            .ok()
            .and_then(|s| s.contracts.get(address).map(|c| c.effects.len()))
            .unwrap_or(0)
    }
    pub fn metrics(&self) -> (u64, u64) {
        self.state
            .lock()
            .map(|s| (s.bytes_on_ledger, s.dropped))
            .unwrap_or((0, 0))
    }
    pub fn view(&self, _now: u64) -> Result<RegistryView, LedgerError> {
        let s = self.state.lock().map_err(|_| LedgerError::Unavailable)?;
        Ok(RegistryView {
            network: s.network,
            roots: s.registry.roots.clone(),
            finalized_time: s.base + s.head.saturating_sub(3) * 6,
            shards: s.registry.params.shards,
            bus_paused: s.registry.paused,
        })
    }
    pub fn advance_to(&self, now: u64) -> Result<(), LedgerError> {
        let mut s = self.state.lock().map_err(|_| LedgerError::Unavailable)?;
        if s.freeze {
            return Ok(());
        }
        while s.last_block.saturating_add(s.params.block_secs) <= now {
            let time = s.last_block + s.params.block_secs;
            Self::produce(&mut s, time);
        }
        Ok(())
    }
    fn produce(s: &mut State, time: u64) {
        s.head += 1;
        s.last_block = time;
        let height = s.head;
        let mut usage = 0;
        let mut writes_bytes = 0;
        let mut block = Block {
            height,
            time,
            writes: vec![],
            anchors: vec![],
        };
        let count = s.pool.len();
        for _ in 0..count {
            let Some(p) = s.pool.pop_front() else {
                break;
            };
            if height.saturating_sub(p.submitted) > s.params.pool_longevity || p.tx.ttl < time {
                s.statuses.insert(p.ticket, TxStatus::Failed);
                s.dropped += 1;
                continue;
            }
            if usage + p.tx.size() > s.params.block_usage
                || writes_bytes + p.tx.state_bytes() > s.params.bytes_written
            {
                s.pool.push_back(p);
                continue;
            }
            if let Action::Reaction(r) = &p.tx.action {
                if !Self::react(s, r, time) {
                    s.statuses.insert(p.ticket, TxStatus::Failed);
                    continue;
                }
            }
            usage += p.tx.size();
            writes_bytes += p.tx.state_bytes();
            s.bytes_on_ledger += p.tx.size() as u64;
            s.statuses.insert(p.ticket, TxStatus::Included(height));
            match p.tx.action {
                Action::Registry(w) => block.writes.push(w),
                Action::Anchor(a) => block.anchors.push(a),
                _ => {}
            }
            for intent in p.tx.intents {
                if !intent.guaranteed && !intent.succeeds {
                    continue;
                }
                for (ordinal, misc) in intent.events.into_iter().enumerate() {
                    if misc.payload.len() + 32 > s.params.log_limit {
                        s.dropped += 1;
                        continue;
                    }
                    let id = s.events.len() as u64 + 1;
                    s.events.push(ContractEvent {
                        id,
                        contract: p.tx.contract,
                        tx: p.ticket,
                        intent: intent.id,
                        ordinal: ordinal as u32,
                        misc,
                        height,
                    });
                }
            }
        }
        s.blocks.push(block);
        let finalized = height.saturating_sub(s.params.finality_blocks);
        if finalized > 0 {
            let b = &s.blocks[finalized as usize - 1];
            for w in &b.writes {
                match w {
                    RegistryWrite::Root(root) => {
                        for r in &mut s.registry.roots {
                            if r.superseded_at.is_none() {
                                r.superseded_at = Some(root.published_at);
                            }
                        }
                        s.registry.roots.push(root.clone());
                    }
                    RegistryWrite::Relays(r) => s.registry.relays = r.clone(),
                    RegistryWrite::Params(p) => s.registry.params = p.clone(),
                    RegistryWrite::Pause(p) => s.registry.paused = *p,
                }
            }
            for a in &b.anchors {
                s.registry.anchors.push(AnchorRecord {
                    payload: a.clone(),
                    height: b.height,
                    time: b.time,
                });
            }
        }
        s.registry
            .anchors
            .retain(|a| time.saturating_sub(a.time) <= 176400);
        if s.registry.anchors.len() > 2940 {
            s.registry.anchors.drain(..s.registry.anchors.len() - 2940);
        }
        for status in s.statuses.values_mut() {
            if let TxStatus::Included(h) = status {
                if *h <= finalized {
                    *status = TxStatus::Final(*h);
                }
            }
        }
    }
    fn react(s: &mut State, r: &Reaction, time: u64) -> bool {
        // Fixed signed statement layout from seal::statement. No decryption key or body is carried.
        if r.statement.len() != 244
            || &r.statement[..10] != b"mpe/v1/sig"
            || r.statement[10..42] != s.network
        {
            return false;
        }
        let Ok(address) = <[u8; 32]>::try_from(&r.statement[180..212]) else {
            return false;
        };
        let Some(contract) = s.contracts.get(&address) else {
            return false;
        };
        if r.statement[212..244] != contract.action {
            return false;
        }
        let Ok(creation) = <[u8; 4]>::try_from(&r.statement[140..144]) else {
            return false;
        };
        let Ok(expiry) = <[u8; 4]>::try_from(&r.statement[144..148]) else {
            return false;
        };
        let creation = u64::from(u32::from_be_bytes(creation));
        let expiry = u64::from(u32::from_be_bytes(expiry));
        if expiry != creation.saturating_add(crate::wire::LIFETIME)
            || time > expiry
            || creation > time.saturating_add(60)
        {
            return false;
        }
        let Ok(signature) = Signature::from_slice(&r.signature) else {
            return false;
        };
        if !contract.publishers.iter().any(|key| {
            VerifyingKey::from_bytes(key)
                .is_ok_and(|key| key.verify_strict(&r.statement, &signature).is_ok())
        }) {
            return false;
        }
        let Some((eid, expected, _)) = s.reaction_witnesses.get(&hash(&[&r.statement])).copied()
        else {
            return false;
        };
        if r.nullifier != expected || contract.nullifiers.contains(&r.nullifier) {
            return false;
        }
        if let Some(proof) = &r.inclusion {
            if !s
                .registry
                .anchors
                .iter()
                .any(|a| proof.verify(&eid, &a.payload))
            {
                return false;
            }
        }
        let Some(contract) = s.contracts.get_mut(&address) else {
            return false;
        };
        contract.nullifiers.insert(r.nullifier);
        contract.effects.push(eid);
        true
    }
    pub fn finalized_events(
        &self,
        contract: &ContractAddress,
        from: u64,
        limit: u16,
    ) -> Result<Vec<ContractEvent>, LedgerError> {
        let s = self.state.lock().map_err(|_| LedgerError::Unavailable)?;
        let final_height = s.head.saturating_sub(s.params.finality_blocks);
        Ok(s.events
            .iter()
            .filter(|e| e.contract == *contract && e.id >= from && e.height <= final_height)
            .take(limit.clamp(1, 500) as usize)
            .cloned()
            .collect())
    }
}
impl LedgerAdapter for MockLedger {
    fn finalized_head(&self) -> Result<BlockRef, LedgerError> {
        let s = self.state.lock().map_err(|_| LedgerError::Unavailable)?;
        let height = s.head.saturating_sub(s.params.finality_blocks);
        let time = s.base + height * s.params.block_secs;
        Ok(BlockRef {
            height,
            time,
            hash: hash(&[&s.network, &height.to_be_bytes()]),
        })
    }
    fn membership_roots(&self) -> Result<Vec<RootRecord>, LedgerError> {
        Ok(self
            .state
            .lock()
            .map_err(|_| LedgerError::Unavailable)?
            .registry
            .roots
            .clone())
    }
    fn historic_root(&self, root: &[u8; 32], now: u64) -> Result<Option<RootRecord>, LedgerError> {
        Ok(self
            .membership_roots()?
            .into_iter()
            .find(|r| r.root == *root && now.saturating_sub(r.published_at) <= 176400))
    }
    fn relay_list(&self) -> Result<Vec<RelayEntry>, LedgerError> {
        Ok(self
            .state
            .lock()
            .map_err(|_| LedgerError::Unavailable)?
            .registry
            .relays
            .clone())
    }
    fn registry_params(&self) -> Result<RegistryParams, LedgerError> {
        Ok(self
            .state
            .lock()
            .map_err(|_| LedgerError::Unavailable)?
            .registry
            .params
            .clone())
    }
    fn anchors(&self, from: u64) -> Result<Vec<AnchorRecord>, LedgerError> {
        Ok(self
            .state
            .lock()
            .map_err(|_| LedgerError::Unavailable)?
            .registry
            .anchors
            .iter()
            .filter(|a| a.payload.window >= from)
            .cloned()
            .collect())
    }
    fn bus_paused(&self) -> Result<bool, LedgerError> {
        Ok(self
            .state
            .lock()
            .map_err(|_| LedgerError::Unavailable)?
            .registry
            .paused)
    }
    fn ledger_parameters(&self) -> Result<LedgerParams, LedgerError> {
        Ok(self
            .state
            .lock()
            .map_err(|_| LedgerError::Unavailable)?
            .params
            .clone())
    }
    fn submit(&self, tx: MockTx) -> Result<TxTicket, LedgerError> {
        let mut s = self.state.lock().map_err(|_| LedgerError::Unavailable)?;
        if s.freeze {
            return Err(LedgerError::Unavailable);
        }
        if s.registry.paused {
            return Err(LedgerError::Paused);
        }
        if tx.size() > s.params.tx_limit || tx.state_bytes() > s.params.bytes_written {
            return Err(LedgerError::Limit);
        }
        if tx.ttl < s.last_block
            || tx.ttl > s.last_block + s.params.intent_ttl
            || tx
                .intents
                .iter()
                .any(|i| i.events.iter().any(|e| e.payload.len() > 256))
        {
            return Err(LedgerError::Invalid);
        }
        let ticket = s.next_tx;
        s.next_tx += 1;
        let submitted = s.head;
        s.pool.push_back(PendingTx {
            ticket,
            tx,
            submitted,
        });
        s.statuses.insert(ticket, TxStatus::Pending);
        Ok(ticket)
    }
    fn tx_status(&self, t: &TxTicket) -> Result<TxStatus, LedgerError> {
        Ok(self
            .state
            .lock()
            .map_err(|_| LedgerError::Unavailable)?
            .statuses
            .get(t)
            .cloned()
            .unwrap_or(TxStatus::Failed))
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use crate::wire::MOCK_NETWORK;
    fn ledger() -> MockLedger {
        MockLedger::new(MOCK_NETWORK, 0, vec![], vec![], 1)
    }
    #[test]
    fn unfinalized_invisible() {
        let l = ledger();
        let tx = MockTx {
            contract: [1; 32],
            intents: vec![],
            action: Action::Registry(RegistryWrite::Pause(true)),
            ttl: 1000,
            fee: 1,
        };
        let t = l.submit(tx).unwrap();
        l.advance_to(6).unwrap();
        assert_eq!(l.tx_status(&t).unwrap(), TxStatus::Included(1));
        assert!(!l.bus_paused().unwrap());
        l.advance_to(18).unwrap();
        assert!(!l.bus_paused().unwrap());
        l.advance_to(24).unwrap();
        assert!(l.bus_paused().unwrap());
        assert_eq!(l.tx_status(&t).unwrap(), TxStatus::Final(1));
    }
    #[test]
    fn block_budget_and_event_finality() {
        let l = ledger();
        for _ in 0..200 {
            let misc = Misc::new(b"mpe/env/v1", vec![0; 256]).unwrap();
            l.submit(MockTx {
                contract: [1; 32],
                intents: vec![Intent {
                    id: 0,
                    guaranteed: true,
                    succeeds: true,
                    events: vec![misc],
                }],
                action: Action::Events,
                ttl: 1000,
                fee: 1,
            })
            .unwrap();
        }
        l.advance_to(6).unwrap();
        assert_eq!(l.metrics().0, 117 * 8480);
        assert!(l.finalized_events(&[1; 32], 0, 500).unwrap().is_empty());
        l.advance_to(24).unwrap();
        assert_eq!(l.finalized_events(&[1; 32], 0, 500).unwrap().len(), 117);
        l.advance_to(30).unwrap();
        assert_eq!(l.finalized_events(&[1; 32], 0, 500).unwrap().len(), 200);
    }
    #[test]
    fn reads_and_relay_entry_fields() {
        let l = MockLedger::new(
            MOCK_NETWORK,
            0,
            vec![RootRecord {
                root: [1; 32],
                period_start: 0,
                published_at: 0,
                superseded_at: None,
            }],
            vec![RelayEntry {
                peer_id: "peer".into(),
                operator: [1; 32],
                relay: true,
                store: true,
                bootstrapper: false,
                gateway: false,
                anchorer: true,
            }],
            1,
        );
        let a: &dyn LedgerAdapter = &l;
        assert_eq!(a.membership_roots().unwrap().len(), 1);
        assert!(a.historic_root(&[1; 32], 100).unwrap().is_some());
        assert_eq!(a.relay_list().unwrap()[0].operator, [1; 32]);
        assert_eq!(a.registry_params().unwrap().shards, 1);
        assert_eq!(a.ledger_parameters().unwrap().tx_limit, 1048576);
        assert!(a.anchors(0).unwrap().is_empty());
        assert!(!a.bus_paused().unwrap());
    }
    #[test]
    fn failing_fallible_discards_events() {
        let l = ledger();
        let misc = Misc::new(b"mpe/env/v1", vec![0; 256]).unwrap();
        l.submit(MockTx {
            contract: [1; 32],
            intents: vec![Intent {
                id: 1,
                guaranteed: false,
                succeeds: false,
                events: vec![misc],
            }],
            action: Action::Events,
            ttl: 1000,
            fee: 1,
        })
        .unwrap();
        l.advance_to(24).unwrap();
        assert!(l.finalized_events(&[1; 32], 0, 100).unwrap().is_empty());
    }
    #[test]
    fn oversized_tx_refused() {
        let l = ledger();
        let misc = Misc::new(b"mpe/env/v1", vec![0; 256]).unwrap();
        assert_eq!(
            l.submit(MockTx {
                contract: [1; 32],
                intents: vec![Intent {
                    id: 0,
                    guaranteed: true,
                    succeeds: true,
                    events: vec![misc; 4000]
                }],
                action: Action::Events,
                ttl: 1000,
                fee: 1
            }),
            Err(LedgerError::Limit)
        );
    }
}
