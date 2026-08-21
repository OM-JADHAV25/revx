from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.exceptions import InvalidRecoveryPolicyConfigError


@dataclass(frozen=True, slots=True)
class RecoveryPolicyConfig:
    minimum_recovery_probability: Decimal
    maximum_risk_score: Decimal
    maximum_retry_count: int

    def __post_init__(self) -> None:
        if not Decimal("0") <= self.minimum_recovery_probability <= Decimal("1"):
            raise InvalidRecoveryPolicyConfigError("Minimum recovery probability must be between 0 and 1.")

        if not Decimal("0") <= self.maximum_risk_score <= Decimal("1"):
            raise InvalidRecoveryPolicyConfigError("Maximum risk score must be between 0 and 1.")

        if self.maximum_retry_count < 0:
            raise InvalidRecoveryPolicyConfigError("Maximum retry count cannot be negative.")