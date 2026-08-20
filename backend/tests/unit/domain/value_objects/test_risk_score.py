from decimal import Decimal

import pytest

from app.domain.exceptions import InvalidRiskScoreError
from app.domain.value_objects.risk_score import RiskScore


@pytest.mark.parametrize(
    "value",
    [
        Decimal("0"),
        Decimal("0.25"),
        Decimal("0.75"),
        Decimal("1"),
    ],
)
def test_creates_valid_risk_score(value: Decimal) -> None:
    risk_score = RiskScore(value=value)

    assert risk_score.value == value


@pytest.mark.parametrize(
    "value",
    [
        Decimal("-0.01"),
        Decimal("1.01"),
    ],
)
def test_rejects_risk_score_outside_valid_range(value: Decimal) -> None:
    with pytest.raises(InvalidRiskScoreError):
        RiskScore(value=value)


def test_risk_score_is_immutable() -> None:
    risk_score = RiskScore(value=Decimal("0.75"))

    with pytest.raises(AttributeError):
        risk_score.value = Decimal("0.90")