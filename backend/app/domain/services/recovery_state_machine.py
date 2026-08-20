from __future__ import annotations

from collections.abc import Mapping

from app.domain.enums.recovery_status import RecoveryStatus
from app.domain.exceptions import InvalidRecoveryStateTransitionError


class RecoveryStateMachine:
    """Validates state transitions for a recovery case."""

    _ALLOWED_TRANSITIONS: Mapping[
        RecoveryStatus,
        frozenset[RecoveryStatus],
    ] = {
        RecoveryStatus.DETECTED: frozenset(
            {
                RecoveryStatus.ANALYZING,
                RecoveryStatus.STOPPED,
            }
        ),
        RecoveryStatus.ANALYZING: frozenset(
            {
                RecoveryStatus.ELIGIBLE,
                RecoveryStatus.ESCALATED,
                RecoveryStatus.STOPPED,
            }
        ),
        RecoveryStatus.ELIGIBLE: frozenset(
            {
                RecoveryStatus.ACTION_PENDING,
                RecoveryStatus.STOPPED,
            }
        ),
        RecoveryStatus.ACTION_PENDING: frozenset(
            {
                RecoveryStatus.ACTION_APPROVED,
                RecoveryStatus.ESCALATED,
                RecoveryStatus.STOPPED,
            }
        ),
        RecoveryStatus.ACTION_APPROVED: frozenset(
            {
                RecoveryStatus.EXECUTING,
                RecoveryStatus.STOPPED,
            }
        ),
        RecoveryStatus.EXECUTING: frozenset(
            {
                RecoveryStatus.RECOVERED,
                RecoveryStatus.RETRY_SCHEDULED,
                RecoveryStatus.ESCALATED,
                RecoveryStatus.STOPPED,
            }
        ),
        RecoveryStatus.RETRY_SCHEDULED: frozenset(
            {
                RecoveryStatus.ACTION_PENDING,
                RecoveryStatus.RECOVERED,
                RecoveryStatus.ESCALATED,
                RecoveryStatus.STOPPED,
            }
        ),
        RecoveryStatus.RECOVERED: frozenset(),
        RecoveryStatus.ESCALATED: frozenset(),
        RecoveryStatus.STOPPED: frozenset(),
    }

    @classmethod
    def can_transition(
        cls,
        current_status: RecoveryStatus,
        target_status: RecoveryStatus,
    ) -> bool:
        """Return whether a transition between two states is allowed."""
        return target_status in cls._ALLOWED_TRANSITIONS[current_status]

    @classmethod
    def validate_transition(
        cls,
        current_status: RecoveryStatus,
        target_status: RecoveryStatus,
    ) -> None:
        """Validate a transition or raise a domain-specific exception."""
        if not cls.can_transition(
            current_status=current_status,
            target_status=target_status,
        ):
            raise InvalidRecoveryStateTransitionError(
                "Invalid recovery state transition: "
                f"{current_status.value} -> {target_status.value}."
            )