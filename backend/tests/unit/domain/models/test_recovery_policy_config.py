from decimal import Decimal

import pytest

from app.domain.exceptions import InvalidRecoveryPolicyConfigError
from app.domain.models.recovery_policy_config import RecoveryPolicyConfig


def test_creates_valid_recovery_policy_config() -> None:
    config = RecoveryPolicyConfig(
        minimum_recovery_probability=Decimal("0.40"),
        maximum_risk_score=Decimal("0.70"),
        maximum_retry_count=3,
    )

    assert config.minimum_recovery_probability == Decimal("0.40")
    assert config.maximum_risk_score == Decimal("0.70")
    assert config.maximum_retry_count == 3


@pytest.mark.parametrize(
    "minimum_recovery_probability",
    [Decimal("-0.01"),Decimal("1.01"),]
)
def test_rejects_invalid_minimum_recovery_probability(
    minimum_recovery_probability: Decimal,
) -> None:
    with pytest.raises(InvalidRecoveryPolicyConfigError):
        RecoveryPolicyConfig(
            minimum_recovery_probability=minimum_recovery_probability,
            maximum_risk_score=Decimal("0.70"),
            maximum_retry_count=3,
        )


@pytest.mark.parametrize(
    "maximum_risk_score",
    [Decimal("-0.01"), Decimal("1.01")]
)
def test_rejects_invalid_maximum_risk_score(
    maximum_risk_score: Decimal,
) -> None:
    with pytest.raises(InvalidRecoveryPolicyConfigError):
        RecoveryPolicyConfig(
            minimum_recovery_probability=Decimal("0.40"),
            maximum_risk_score=maximum_risk_score,
            maximum_retry_count=3,
        )


def test_rejects_negative_maximum_retry_count() -> None:
    with pytest.raises(InvalidRecoveryPolicyConfigError):
        RecoveryPolicyConfig(
            minimum_recovery_probability=Decimal("0.40"),
            maximum_risk_score=Decimal("0.70"),
            maximum_retry_count=-1,
        )