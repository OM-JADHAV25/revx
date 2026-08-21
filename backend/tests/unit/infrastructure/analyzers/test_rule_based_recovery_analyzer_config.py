from decimal import Decimal

import pytest

from app.domain.exceptions import InvalidRuleBasedAnalyzerConfigError
from app.infrastructure.analyzers.rule_based_recovery_analyzer_config import (RuleBasedRecoveryAnalyzerConfig)


def test_creates_valid_rule_based_analyzer_config() -> None:
    config = RuleBasedRecoveryAnalyzerConfig(high_value_payment_threshold=Decimal("10000"))

    assert (config.high_value_payment_threshold == Decimal("10000"))


@pytest.mark.parametrize(
    "threshold",
    [Decimal("0"),Decimal("-1"),]
)
def test_rejects_non_positive_high_value_payment_threshold(
    threshold: Decimal,
) -> None:
    with pytest.raises(InvalidRuleBasedAnalyzerConfigError):
        RuleBasedRecoveryAnalyzerConfig(high_value_payment_threshold=threshold)