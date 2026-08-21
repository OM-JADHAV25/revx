from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_uses_default_settings() -> None:
    settings = Settings(_env_file=None)

    assert settings.app_name == "RevX"
    assert settings.app_version == "0.1.0"
    assert settings.minimum_recovery_probability == Decimal("0.40")
    assert settings.maximum_risk_score == Decimal("0.70")
    assert settings.maximum_retry_count == 3
    assert settings.high_value_payment_threshold == Decimal("10000")


def test_accepts_valid_custom_settings() -> None:
    settings = Settings(
        _env_file=None,
        minimum_recovery_probability=Decimal("0.50"),
        maximum_risk_score=Decimal("0.60"),
        maximum_retry_count=5,
        high_value_payment_threshold=Decimal("50000"),
    )

    assert settings.minimum_recovery_probability == Decimal("0.50")
    assert settings.maximum_risk_score == Decimal("0.60")
    assert settings.maximum_retry_count == 5
    assert settings.high_value_payment_threshold == Decimal("50000")


@pytest.mark.parametrize(
    "field_name, value",
    [
        ("minimum_recovery_probability", Decimal("-0.01")),
        ("minimum_recovery_probability", Decimal("1.01")),
        ("maximum_risk_score", Decimal("-0.01")),
        ("maximum_risk_score", Decimal("1.01")),
        ("maximum_retry_count", -1),
        ("high_value_payment_threshold", Decimal("0")),
        ("high_value_payment_threshold", Decimal("-1")),
    ],
)
def test_rejects_invalid_settings(
    field_name: str,
    value: Decimal | int,
) -> None:
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            **{field_name: value},
        )