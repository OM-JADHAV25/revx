from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.exceptions import InvalidRuleBasedAnalyzerConfigError


@dataclass(frozen=True, slots=True)
class RuleBasedRecoveryAnalyzerConfig:
    high_value_payment_threshold: Decimal = Decimal("10000")

    def __post_init__(self) -> None:
        if self.high_value_payment_threshold <= Decimal("0"):
            raise InvalidRuleBasedAnalyzerConfigError("High-value payment threshold must be greater than zero.")