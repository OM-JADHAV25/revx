from __future__ import annotations

from decimal import Decimal

from app.domain.entities.recovery_case import RecoveryCase
from app.domain.enums.failure_reason import FailureReason
from app.domain.enums.recovery_action import RecoveryAction
from app.domain.models.recovery_proposal import RecoveryProposal
from app.domain.value_objects.recovery_probability import (RecoveryProbability)
from app.domain.value_objects.risk_score import RiskScore
from app.infrastructure.analyzers.rule_based_recovery_analyzer_config import (RuleBasedRecoveryAnalyzerConfig)


class RuleBasedRecoveryAnalyzer:
    """Produces deterministic recovery proposals using predefined rules."""

    def __init__(
        self,
        *,
        config: RuleBasedRecoveryAnalyzerConfig,
    ) -> None:
        self._config = config

    def analyze(
        self,
        *,
        recovery_case: RecoveryCase,
    ) -> RecoveryProposal:
        if (recovery_case.amount.amount >= self._config.high_value_payment_threshold):
            return self._create_high_value_retry_proposal(recovery_case=recovery_case)

        return self._create_standard_retry_proposal(
            recovery_case=recovery_case,
        )

    @staticmethod
    def _create_high_value_retry_proposal(
        *,
        recovery_case: RecoveryCase,
    ) -> RecoveryProposal:
        return RecoveryProposal.create(
            recovery_case_id=recovery_case.recovery_case_id,
            failure_reason=FailureReason.UNKNOWN,
            proposed_action=RecoveryAction.RETRY_PAYMENT,
            recovery_probability=RecoveryProbability(value=Decimal("0.65")),
            risk_score=RiskScore(value=Decimal("0.45")),
            rationale=(
                "The payment is classified as high value, "
                "so recovery requires a more conservative retry assessment."
            ),
        )

    @staticmethod
    def _create_standard_retry_proposal(
        *,
        recovery_case: RecoveryCase,
    ) -> RecoveryProposal:
        return RecoveryProposal.create(
            recovery_case_id=recovery_case.recovery_case_id,
            failure_reason=FailureReason.UNKNOWN,
            proposed_action=RecoveryAction.RETRY_PAYMENT,
            recovery_probability=RecoveryProbability(
                value=Decimal("0.85"),
            ),
            risk_score=RiskScore(value=Decimal("0.15")),
            rationale=(
                "The payment is within the standard recovery range "
                "and is suitable for an automated retry."
            ),
        )