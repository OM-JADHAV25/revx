from __future__ import annotations

from app.application.dto.analyze_recovery_case_result import (
    AnalyzeRecoveryCaseResult,
)
from app.application.ports.recovery_analyzer import RecoveryAnalyzer
from app.domain.entities.recovery_case import RecoveryCase
from app.domain.enums.policy_decision import PolicyDecision
from app.domain.enums.recovery_status import RecoveryStatus
from app.domain.services.recovery_policy import RecoveryPolicy


class AnalyzeRecoveryCase:
    """Analyzes a recovery case and evaluates the proposed recovery action."""

    def __init__(
        self,
        *,
        recovery_analyzer: RecoveryAnalyzer,
        recovery_policy: RecoveryPolicy,
    ) -> None:
        self._recovery_analyzer = recovery_analyzer
        self._recovery_policy = recovery_policy

    def execute(
        self,
        *,
        recovery_case: RecoveryCase,
    ) -> AnalyzeRecoveryCaseResult:
        recovery_case.transition_to(RecoveryStatus.ANALYZING,)

        proposal = self._recovery_analyzer.analyze(recovery_case=recovery_case)

        recovery_case.transition_to(RecoveryStatus.ELIGIBLE)

        recovery_case.transition_to(RecoveryStatus.ACTION_PENDING)

        policy_evaluation = self._recovery_policy.evaluate(recovery_case=recovery_case,proposal=proposal)

        if policy_evaluation.decision == PolicyDecision.APPROVED:
            recovery_case.transition_to(RecoveryStatus.ACTION_APPROVED)

        elif policy_evaluation.decision == PolicyDecision.REJECTED:
            recovery_case.transition_to(RecoveryStatus.STOPPED)

        elif policy_evaluation.decision == PolicyDecision.ESCALATED:
            recovery_case.transition_to(RecoveryStatus.ESCALATED)

        return AnalyzeRecoveryCaseResult(
            recovery_case=recovery_case,
            proposal=proposal,
            policy_evaluation=policy_evaluation,
        )