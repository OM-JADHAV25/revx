from __future__ import annotations

from uuid import UUID

from app.application.ports.recovery_case_repository import (RecoveryCaseRepository)
from app.domain.entities.recovery_case import RecoveryCase
from app.domain.enums.recovery_status import RecoveryStatus


class TransitionRecoveryCase:
    """Transition an existing recovery case to a new status."""

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
        target_status: RecoveryStatus,
    ) -> RecoveryCase | None:
        """Transition and persist a recovery case."""

        recovery_case = (self._recovery_case_repository.get_by_id(recovery_case_id=recovery_case_id))

        if recovery_case is None:
            return None

        recovery_case.transition_to(target_status=target_status)

        self._recovery_case_repository.update(recovery_case=recovery_case)

        return recovery_case