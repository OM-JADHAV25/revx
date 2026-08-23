from __future__ import annotations

from uuid import UUID

from app.domain.entities.recovery_case import RecoveryCase


class InMemoryRecoveryCaseRepository:
    """In-memory implementation of the recovery case repository."""

    def __init__(self) -> None:
        self._recovery_cases: dict[UUID, RecoveryCase] = {}

    def add(
        self,
        *,
        recovery_case: RecoveryCase,
    ) -> None:
        if recovery_case.recovery_case_id in self._recovery_cases:
            raise ValueError("A recovery case with the given identifier already exists.")

        self._recovery_cases[recovery_case.recovery_case_id] = recovery_case

    def get_by_id(
        self,
        *,
        recovery_case_id: UUID,
    ) -> RecoveryCase | None:
        return self._recovery_cases.get(recovery_case_id)

    def get_by_payment_id(
        self,
        *,
        payment_id: UUID,
    ) -> RecoveryCase | None:
        """Return a recovery case associated with a payment."""

        for recovery_case in self._recovery_cases.values():
            if recovery_case.payment_id == payment_id:
                return recovery_case

        return None

    def update(
        self,
        *,
        recovery_case: RecoveryCase,
    ) -> None:
        if recovery_case.recovery_case_id not in self._recovery_cases:
            raise ValueError("Cannot update a recovery case that does not exist.")

        self._recovery_cases[recovery_case.recovery_case_id] = recovery_case