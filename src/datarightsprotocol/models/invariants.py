from typing import TypedDict, List
from enum import Enum
from datarightsprotocol.models.base import BaseModel

class RequestStatus(str, Enum):
    in_progress = "in_progress"
    open = "open"
    fulfilled = "fulfilled"
    revoked = "revoked"
    denied = "denied"
    expired = "expired"

class RequestReason(str, Enum):
    need_verification = "need_user_verification"
    suspected_fraud = "suspected_fraud"
    insufficient_verification = "insuf_verification"
    no_match = "no_match"
    claim_not_covered = "claim_not_covered"
    too_many_requests = "too_many_requests"
    outside_jurisdiction = "outside_jurisdiction"
    other = "other"
    none = ""
    
class StateReasons(TypedDict):
    status: RequestStatus
    reasons: List[RequestReason]

def valid_states() -> StateReasons:
    """
    StateReasons.valid_states is a map of state -> valid reasons.
    see StateReasons.is_valid_state() to validate a pair.
    """
    return {
        RequestStatus.open: [RequestReason.none],
        RequestStatus.in_progress: [ RequestReason.none, RequestReason.need_verification ],
        RequestStatus.fulfilled: [ RequestReason.none ],
        RequestStatus.revoked: [ RequestReason.none ],
        RequestStatus.denied: [
            RequestReason.suspected_fraud,
            RequestReason.insufficient_verification,
            RequestReason.no_match,
            RequestReason.claim_not_covered,
            RequestReason.outside_jurisdiction,
            RequestReason.other,
        ],
        RequestStatus.expired: [ RequestReason.none ],
    }

def is_valid_state_reason(state: RequestStatus, reason: RequestReason):
    valid_reasons = valid_states().get(state, [])
    return reason in valid_reasons

class Action(str, Enum):
    opt_out = "sale:opt-out"
    opt_in  = "sale:opt-in"
    deletion = "deletion"
    access = "access"
    access_cat = "access:categories"
    access_specific = "access:specific"

class Regime(str, Enum):
    ccpa = "ccpa"

class RequestMD(BaseModel):
    version: str = "0.4"
