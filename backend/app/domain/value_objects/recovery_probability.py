from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.exceptions import InvalidRecoveryProbabilityError

@dataclass(frozen=True, slots=True)
class RecoveryProbability:
    value: Decimal

    def __post_init__(self) -> None:
        if not Decimal("0") <= self.value <= Decimal("1"):
            raise InvalidRecoveryProbabilityError("Recovery probability must be between 0 and 1.")