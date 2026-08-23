from __future__ import annotations

from uuid import UUID

from app.application.ports.recovery_case_repository import (RecoveryCaseRepository)
from app.domain.entities.recovery_case import RecoveryCase


class GetRecoveryCase:
    """Retrieve a recovery case by its identifier."""

    def __init__(
        self,
        *,
        recovery_case_repository: RecoveryCaseRepository,
    ) -> None:
        self._recovery_case_repository = recovery_case_repository

    def execute(
        self,
        *,
        recovery_case_id: UUID,
    ) -> RecoveryCase | None:
        """Return the recovery case if it exists."""

        return self._recovery_case_repository.get_by_id(recovery_case_id=recovery_case_id)