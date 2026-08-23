from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.enums.recovery_status import RecoveryStatus
from app.domain.exceptions import InvalidRecoveryCaseError
from app.domain.services.recovery_state_machine import RecoveryStateMachine
from app.domain.value_objects.money import Money
from app.domain.value_objects.recovery_probability import RecoveryProbability
from app.domain.value_objects.risk_score import RiskScore


@dataclass(slots=True)
class RecoveryCase:
    recovery_case_id: UUID
    merchant_id: UUID
    payment_id: UUID
    amount: Money

    customer_id: UUID | None = None
    subscription_id: UUID | None = None

    status: RecoveryStatus = RecoveryStatus.DETECTED

    recovery_probability: RecoveryProbability | None = None
    risk_score: RiskScore | None = None

    retry_count: int = 0
    version: int = 1

    _persisted_version: int | None = field(
        default=None,
        repr=False,
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def mark_persisted(self) -> None:
        """Mark the current aggregate version as persisted."""

        self._persisted_version = self.version

    @property
    def persisted_version(self) -> int:
        """Return the version currently persisted in storage."""

        if self._persisted_version is None:
            return self.version

        return self._persisted_version


    @classmethod
    def create(
        cls,
        *,
        merchant_id: UUID,
        payment_id: UUID,
        amount: Money,
        customer_id: UUID | None = None,
        subscription_id: UUID | None = None,
    ) -> "RecoveryCase":
        return cls(
            recovery_case_id=uuid4(),
            merchant_id=merchant_id,
            payment_id=payment_id,
            amount=amount,
            customer_id=customer_id,
            subscription_id=subscription_id,
        )

    def __post_init__(self) -> None:
        if self.retry_count < 0:
            raise InvalidRecoveryCaseError(
                "Retry count cannot be negative."
            )

        if self.version < 1:
            raise InvalidRecoveryCaseError(
                "Recovery case version must be at least 1."
            )

    def transition_to(
        self,
        target_status: RecoveryStatus,
    ) -> None:
        RecoveryStateMachine.validate_transition(
            current_status=self.status,
            target_status=target_status,
        )

        self.status = target_status
        self.version += 1
        self.updated_at = datetime.now(timezone.utc)

    @property
    def is_terminal(self) -> bool:
        return self.status in {
            RecoveryStatus.RECOVERED,
            RecoveryStatus.STOPPED,
        }