from __future__ import annotations

from typing import Protocol
from uuid import UUID

from app.domain.entities.recovery_case import RecoveryCase


class RecoveryCaseRepository(Protocol):
    """Defines persistence operations for recovery cases."""

    def add(
        self,
        *,
        recovery_case: RecoveryCase,
    ) -> None:
        """Persist a new recovery case."""

    def get_by_id(
        self,
        *,
        recovery_case_id: UUID,
    ) -> RecoveryCase | None:
        """Return a recovery case by its identifier."""

    def get_by_payment_id(
        self,
        *,
        payment_id: UUID,
    ) -> RecoveryCase | None:
        """Return a recovery case associated with a payment."""

    def update(
        self,
        *,
        recovery_case: RecoveryCase,
    ) -> None:
        """Persist changes to an existing recovery case."""