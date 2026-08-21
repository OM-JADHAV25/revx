from __future__ import annotations

from dataclasses import dataclass

from app.domain.entities.recovery_case import RecoveryCase
from app.domain.models.policy_evaluation import PolicyEvaluation
from app.domain.models.recovery_proposal import RecoveryProposal


@dataclass(frozen=True, slots=True)
class AnalyzeRecoveryCaseResult:
    recovery_case: RecoveryCase
    proposal: RecoveryProposal
    policy_evaluation: PolicyEvaluation