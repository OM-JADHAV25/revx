from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.exceptions import InvalidMoneyError


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        if self.amount < Decimal("0"):
            raise InvalidMoneyError("Money amount cannot be negative.")

        if not self.currency:
            raise InvalidMoneyError("Currency must be provided.")

        object.__setattr__(self,"currency",self.currency.upper())