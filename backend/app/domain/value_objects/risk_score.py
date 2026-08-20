from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.exceptions import InvalidRiskScoreError


@dataclass(frozen=True, slots=True)
class RiskScore:
    value: Decimal

    def __post_init__(self) -> None:
        if not Decimal("0") <= self.value <= Decimal("1"):
            raise InvalidRiskScoreError("Risk score must be between 0 and 1.")