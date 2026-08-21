from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.enums.policy_decision import PolicyDecision
from app.domain.exceptions import InvalidPolicyEvaluationError


@dataclass(frozen=True, slots=True)
class PolicyEvaluation:
    evaluation_id: UUID
    recovery_case_id: UUID
    proposal_id: UUID

    decision: PolicyDecision
    reason: str

    created_at: datetime = field( default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(
        cls,
        *,
        recovery_case_id: UUID,
        proposal_id: UUID,
        decision: PolicyDecision,
        reason: str,
    ) -> "PolicyEvaluation":
        return cls(
            evaluation_id=uuid4(),
            recovery_case_id=recovery_case_id,
            proposal_id=proposal_id,
            decision=decision,
            reason=reason,
        )

    def __post_init__(self) -> None:
        if not self.reason.strip():
            raise InvalidPolicyEvaluationError("Policy evaluation reason cannot be empty.")