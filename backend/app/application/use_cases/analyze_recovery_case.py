from __future__ import annotations

from app.application.dto.analyze_recovery_case_result import (
    AnalyzeRecoveryCaseResult,
)
from app.application.ports.recovery_analyzer import RecoveryAnalyzer
from app.application.ports.recovery_case_repository import RecoveryCaseRepository
from app.domain.entities.recovery_case import RecoveryCase
from app.domain.enums.policy_decision import PolicyDecision
from app.domain.enums.recovery_status import RecoveryStatus
from app.domain.services.recovery_policy import RecoveryPolicy


class AnalyzeRecoveryCase:
    """Coordinates recovery analysis, policy evaluation, and persistence."""

    def __init__(
        self,
        *,
        recovery_analyzer: RecoveryAnalyzer,
        recovery_policy: RecoveryPolicy,
        recovery_case_repository: RecoveryCaseRepository,
    ) -> None:
        self._recovery_analyzer = recovery_analyzer
        self._recovery_policy = recovery_policy
        self._recovery_case_repository = recovery_case_repository

    def execute(
        self,
        *,
        recovery_case: RecoveryCase,
    ) -> AnalyzeRecoveryCaseResult:

        existing_recovery_case = (
            self._recovery_case_repository.get_by_payment_id(
                payment_id=recovery_case.payment_id,
            )
        )

        if existing_recovery_case is not None:
            proposal = self._recovery_analyzer.analyze(
                recovery_case=existing_recovery_case
            )

            policy_evaluation = self._recovery_policy.evaluate(
                recovery_case=existing_recovery_case,
                proposal=proposal,
            )

            return AnalyzeRecoveryCaseResult(
                recovery_case=existing_recovery_case,
                proposal=proposal,
                policy_evaluation=policy_evaluation,
            )

        self._recovery_case_repository.add(
            recovery_case=recovery_case,
        )

        # DETECTED -> ANALYZING
        recovery_case.transition_to(
            target_status=RecoveryStatus.ANALYZING,
        )

        proposal = self._recovery_analyzer.analyze(
            recovery_case=recovery_case,
        )

        policy_evaluation = self._recovery_policy.evaluate(
            recovery_case=recovery_case,
            proposal=proposal,
        )

        if policy_evaluation.decision == PolicyDecision.APPROVED:

            # ANALYZING -> ELIGIBLE
            recovery_case.transition_to(
                target_status=RecoveryStatus.ELIGIBLE,
            )

            # ELIGIBLE -> ACTION_PENDING
            recovery_case.transition_to(
                target_status=RecoveryStatus.ACTION_PENDING,
            )

            # ACTION_PENDING -> ACTION_APPROVED
            recovery_case.transition_to(
                target_status=RecoveryStatus.ACTION_APPROVED,
            )

        else:

            # ANALYZING -> STOPPED
            recovery_case.transition_to(
                target_status=RecoveryStatus.STOPPED,
            )

        self._recovery_case_repository.update(
            recovery_case=recovery_case,
        )

        return AnalyzeRecoveryCaseResult(
            recovery_case=recovery_case,
            proposal=proposal,
            policy_evaluation=policy_evaluation,
        )