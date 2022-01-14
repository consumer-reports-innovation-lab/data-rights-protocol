from datetime import datetime
from typing import List, Optional, Set
from pydantic import HttpUrl, UUID4, validator, root_validator

from .base import BaseModel
from .invariants import RequestMD, Action, Regime, RequestStatus, RequestReason, is_valid_state_reason
from .identity import IdentityPayload

class DataRightsRequest(BaseModel):
    request_id: Optional[UUID4]
    meta: RequestMD = RequestMD()
    relationships: Set[str]
    status_callback: Optional[HttpUrl]

    regime: Regime = Regime.ccpa
    exercise: Set[Action]

    identity: IdentityPayload

    def as_json(self):
        return self.json(
            models_as_dict=False,
            exclude_none=True,
        )

class DataRightsStatus(BaseModel):
    request_id: UUID4
    received_at: datetime
    results_url: Optional[str]

    status: RequestStatus
    reason: RequestReason

    @root_validator
    def no_results_for_unfulfilled(cls, values):
        if values.get('status') != RequestStatus.fulfilled:
            if values.get('results_url') != None:
                raise ValueError("cannot have results_url for unfulfilled request!")

    @root_validator
    def reason_valid_for_status(cls, values):
        status = values.get('status')
        reason = values.get('reason')
        if not is_valid_state_reason(status, reason):
            raise ValueError("reason not valid for state")
