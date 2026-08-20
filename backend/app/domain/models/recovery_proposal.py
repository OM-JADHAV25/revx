from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.enums.failure_reason import FailureReason
from app.domain.enums.recovery_action import RecoveryAction
from app.domain.exceptions import InvalidRecoveryProposalError
from app.domain.value_objects.recovery_probability import RecoveryProbability
from app.domain.value_objects.risk_score import RiskScore

@dataclass(frozen=True, slots=True)
class RecoveryProposal:
    proposal_id: UUID

    recovery_case_id: UUID

    failure_reason: FailureReason
    proposed_action: RecoveryAction

    recovery_probability: RecoveryProbability
    risk_score: RiskScore

    rationale: str

    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(
        cls,
        *,
        recovery_case_id: UUID,
        failure_reason: FailureReason,
        proposed_action: RecoveryAction,
        recovery_probability: RecoveryProbability,
        risk_score: RiskScore,
        rationale: str,
    ) -> "RecoveryProposal":
        return cls(
            proposal_id=uuid4(),
            recovery_case_id=recovery_case_id,
            failure_reason=failure_reason,
            proposed_action=proposed_action,
            recovery_probability=recovery_probability,
            risk_score=risk_score,
            rationale=rationale,
        )

    def __post_init__(self) -> None:
        if not self.rationale.strip():
            raise InvalidRecoveryProposalError("Recovery proposal rationale cannot be empty.")