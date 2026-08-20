from decimal import Decimal

import pytest

from app.domain.exceptions import InvalidRecoveryProbabilityError
from app.domain.value_objects.recovery_probability import RecoveryProbability


@pytest.mark.parametrize(
    "value",
    [
        Decimal("0"),
        Decimal("0.25"),
        Decimal("0.823471"),
        Decimal("1"),
    ],
)
def test_creates_valid_recovery_probability(value: Decimal) -> None:
    probability = RecoveryProbability(value=value)

    assert probability.value == value


@pytest.mark.parametrize(
    "value",
    [
        Decimal("-0.01"),
        Decimal("1.01"),
    ],
)
def test_rejects_probability_outside_valid_range(value: Decimal) -> None:
    with pytest.raises(InvalidRecoveryProbabilityError):
        RecoveryProbability(value=value)


def test_recovery_probability_is_immutable() -> None:
    probability = RecoveryProbability(value=Decimal("0.82"))

    with pytest.raises(AttributeError):
        probability.value = Decimal("0.90")