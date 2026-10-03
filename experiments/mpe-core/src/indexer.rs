use crate::ledger::{ContractAddress, ContractEvent, LedgerError, MockLedger};
use std::sync::{Arc, Mutex};
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Coverage {
    Unknown,
}
pub trait Indexer: Send + Sync {
    fn contract_events(
        &self,
        contract: &ContractAddress,
        from_id: u64,
        limit: u16,
    ) -> Result<Vec<ContractEvent>, LedgerError>;
    fn retention_coverage(&self) -> Coverage;
}
pub struct MockIndexer {
    pub ledger: Arc<MockLedger>,
    pub calls: Mutex<Vec<(ContractAddress, u64, u16)>>,
}
impl MockIndexer {
    pub fn new(ledger: Arc<MockLedger>) -> Self {
        Self {
            ledger,
            calls: Mutex::new(vec![]),
        }
    }
    pub fn subscription_drain(
        &self,
        contract: &ContractAddress,
        from: u64,
    ) -> Result<Vec<ContractEvent>, LedgerError> {
        self.contract_events(contract, from, 20)
    }
}
impl Indexer for MockIndexer {
    fn contract_events(
        &self,
        contract: &ContractAddress,
        from_id: u64,
        limit: u16,
    ) -> Result<Vec<ContractEvent>, LedgerError> {
        self.calls
            .lock()
            .map_err(|_| LedgerError::Unavailable)?
            .push((*contract, from_id, limit.clamp(1, 500)));
        self.ledger.finalized_events(contract, from_id, limit)
    }
    fn retention_coverage(&self) -> Coverage {
        Coverage::Unknown
    }
}
