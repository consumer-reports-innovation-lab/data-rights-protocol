from datetime import datetime
from typing import List, Optional, Set
from pydantic import HttpUrl, UUID4, validator, root_validator

from datarightsprotocol.models.base import BaseModel
from datarightsprotocol.models.invariants import RequestMD, Action, Regime, RequestStatus, RequestReason, is_valid_state_reason
from datarightsprotocol.models.identity import IdentityPayload

class DataRightsRequest(BaseModel):
    request_id: Optional[UUID4]
    meta: RequestMD = RequestMD()
    relationships: Optional[Set[str]]
    status_callback: Optional[HttpUrl]

    regime: Regime = Regime.ccpa
    exercise: Set[Action]

    identity: IdentityPayload

    def json(self):
        return super().json(
            models_as_dict=False,
            exclude_none=True,
        )


class DataRightsStatus(BaseModel):
    request_id: UUID4
    received_at: datetime
    results_url: Optional[str]

    expected_by: Optional[datetime]
    processing_details: Optional[str]

    status: RequestStatus
    reason: RequestReason

    @root_validator
    def no_results_for_unfulfilled(cls, values):
        if values.get('status') != RequestStatus.fulfilled:
            if values.get('results_url') != None:
                raise ValueError("cannot have results_url for unfulfilled request!")
        return values

    @root_validator
    def reason_valid_for_status(cls, values):
        status = values.get('status')
        reason = values.get('reason')
        if not is_valid_state_reason(status, reason):
            raise ValueError("reason not valid for state")
        return values
