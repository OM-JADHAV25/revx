from decimal import Decimal

import pytest

from app.domain.exceptions import InvalidMoneyError
from app.domain.value_objects.money import Money


def test_creates_valid_money() -> None:
    money = Money(
        amount=Decimal("1499.99"),
        currency="inr",
    )

    assert money.amount == Decimal("1499.99")
    assert money.currency == "INR"


def test_rejects_negative_amount() -> None:
    with pytest.raises(InvalidMoneyError):
        Money(
            amount=Decimal("-1"),
            currency="INR",
        )


def test_rejects_empty_currency() -> None:
    with pytest.raises(InvalidMoneyError):
        Money(
            amount=Decimal("100"),
            currency="",
        )


def test_money_is_immutable() -> None:
    money = Money(
        amount=Decimal("100"),
        currency="INR",
    )

    with pytest.raises(AttributeError):
        money.currency = "USD"


