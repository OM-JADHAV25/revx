from uuid import UUID

from pydantic import BaseModel

from app.domain.enums.policy_decision import PolicyDecision
from app.domain.enums.recovery_action import RecoveryAction
from app.domain.enums.recovery_status import RecoveryStatus


class AnalyzeRecoveryResponse(BaseModel):
    recovery_case_id: UUID
    proposal_id: UUID

    status: RecoveryStatus
    proposed_action: RecoveryAction
    policy_decision: PolicyDecision

    recovery_probability: str
    risk_score: str
    rationale: str
    policy_reason: str