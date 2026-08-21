from decimal import Decimal
from uuid import uuid4

from app.domain.entities.recovery_case import RecoveryCase
from app.domain.enums.recovery_action import RecoveryAction
from app.domain.value_objects.money import Money
from app.infrastructure.analyzers.rule_based_recovery_analyzer import (RuleBasedRecoveryAnalyzer)
from app.infrastructure.analyzers.rule_based_recovery_analyzer_config import (RuleBasedRecoveryAnalyzerConfig)


def create_analyzer() -> RuleBasedRecoveryAnalyzer:
    return RuleBasedRecoveryAnalyzer(
        config=RuleBasedRecoveryAnalyzerConfig(
            high_value_payment_threshold=Decimal("10000"),
        )
    )


def create_recovery_case(
    *,
    amount: Decimal = Decimal("1000"),
) -> RecoveryCase:
    return RecoveryCase(
        recovery_case_id=uuid4(),
        merchant_id=uuid4(),
        payment_id=uuid4(),
        amount=Money(
            amount=amount,
            currency="INR",
        ),
    )


def test_creates_standard_retry_proposal() -> None:
    analyzer = create_analyzer()

    proposal = analyzer.analyze(recovery_case=create_recovery_case())

    assert proposal.proposed_action == RecoveryAction.RETRY_PAYMENT
    assert proposal.recovery_probability.value == Decimal("0.85")
    assert proposal.risk_score.value == Decimal("0.15")


def test_creates_conservative_proposal_for_high_value_payment() -> None:
    analyzer = create_analyzer()

    proposal = analyzer.analyze(recovery_case=create_recovery_case(amount=Decimal("10000")))

    assert proposal.proposed_action == RecoveryAction.RETRY_PAYMENT
    assert proposal.recovery_probability.value == Decimal("0.65")
    assert proposal.risk_score.value == Decimal("0.45")