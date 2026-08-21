from decimal import Decimal
from uuid import uuid4

import pytest

from app.application.use_cases.analyze_recovery_case import (AnalyzeRecoveryCase)
from app.domain.entities.recovery_case import RecoveryCase
from app.domain.enums.failure_reason import FailureReason
from app.domain.enums.policy_decision import PolicyDecision
from app.domain.enums.recovery_action import RecoveryAction
from app.domain.enums.recovery_status import RecoveryStatus
from app.domain.models.recovery_policy_config import RecoveryPolicyConfig
from app.domain.models.recovery_proposal import RecoveryProposal
from app.domain.services.recovery_policy import RecoveryPolicy
from app.domain.value_objects.money import Money
from app.domain.value_objects.recovery_probability import (RecoveryProbability)
from app.domain.value_objects.risk_score import RiskScore


class FakeRecoveryAnalyzer:
    def __init__(
        self,
        *,
        probability: Decimal,
        risk: Decimal,
    ) -> None:
        self._probability = probability
        self._risk = risk

    def analyze(
        self,
        *,
        recovery_case: RecoveryCase,
    ) -> RecoveryProposal:
        return RecoveryProposal.create(
            recovery_case_id=recovery_case.recovery_case_id,
            failure_reason=FailureReason.INSUFFICIENT_FUNDS,
            proposed_action=RecoveryAction.RETRY_PAYMENT,
            recovery_probability=RecoveryProbability(value=self._probability),
            risk_score=RiskScore(value=self._risk),
            rationale="Test recovery proposal.",
        )


def create_recovery_case() -> RecoveryCase:
    return RecoveryCase(
        recovery_case_id=uuid4(),
        merchant_id=uuid4(),
        payment_id=uuid4(),
        amount=Money(amount=Decimal("1000"),currency="INR"),
    )


def create_recovery_policy() -> RecoveryPolicy:
    return RecoveryPolicy(
        config=RecoveryPolicyConfig(
            minimum_recovery_probability=Decimal("0.40"),
            maximum_risk_score=Decimal("0.70"),
            maximum_retry_count=3,
        )
    )


@pytest.mark.parametrize(
    ("probability", "risk", "expected_decision", "expected_status"),
    [
        (
            Decimal("0.80"),
            Decimal("0.20"),
            PolicyDecision.APPROVED,
            RecoveryStatus.ACTION_APPROVED,
        ),
        (
            Decimal("0.20"),
            Decimal("0.20"),
            PolicyDecision.REJECTED,
            RecoveryStatus.STOPPED,
        ),
        (
            Decimal("0.80"),
            Decimal("0.90"),
            PolicyDecision.ESCALATED,
            RecoveryStatus.ESCALATED,
        ),
    ],
)
def test_analyzes_recovery_case_and_applies_policy_decision(
    probability: Decimal,
    risk: Decimal,
    expected_decision: PolicyDecision,
    expected_status: RecoveryStatus,
) -> None:
    recovery_analyzer = FakeRecoveryAnalyzer(
        probability=probability,
        risk=risk,
    )

    use_case = AnalyzeRecoveryCase(
        recovery_analyzer=recovery_analyzer,
        recovery_policy=create_recovery_policy(),
    )

    recovery_case = create_recovery_case()

    result = use_case.execute(recovery_case=recovery_case,)

    assert (result.policy_evaluation.decision== expected_decision)

    assert result.recovery_case.status == expected_status