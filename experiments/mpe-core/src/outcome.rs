use serde::{Deserialize, Serialize};
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize, thiserror::Error)]
pub enum ClientError {
    #[error("TooLarge")]
    TooLarge,
    #[error("NotReady")]
    NotReady,
    #[error("NotAccepted")]
    NotAccepted,
    #[error("Busy")]
    Busy,
    #[error("Refused")]
    Refused,
    #[error("ResourceExhausted")]
    ResourceExhausted,
    #[error("StorageExhausted")]
    StorageExhausted,
    #[error("KeyLimit")]
    KeyLimit,
    #[error("Degraded")]
    Degraded,
    #[error("SourceFailed")]
    SourceFailed,
    #[error("Unresolved")]
    Unresolved,
    #[error("RetentionGap")]
    RetentionGap,
    #[error("KeyGap")]
    KeyGap,
    #[error("CorruptRecord")]
    CorruptRecord,
    #[error("LedgerUnavailable")]
    LedgerUnavailable,
    #[error("LedgerPaused")]
    LedgerPaused,
    #[error("BusPaused")]
    BusPaused,
    #[error("InsufficientDust")]
    InsufficientDust,
    #[error("SessionUpdateRequired")]
    SessionUpdateRequired,
}
impl From<crate::wire::Error> for ClientError {
    fn from(e: crate::wire::Error) -> Self {
        use crate::wire::Error;
        match e {
            Error::TooLarge => Self::TooLarge,
            Error::RandomnessUnavailable => Self::NotReady,
            Error::OverQuota => Self::NotReady,
            Error::StorageExhausted => Self::StorageExhausted,
            Error::Refused => Self::Refused,
            _ => Self::CorruptRecord,
        }
    }
}
