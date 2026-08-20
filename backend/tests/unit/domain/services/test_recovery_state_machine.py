import pytest

from app.domain.enums.recovery_status import RecoveryStatus
from app.domain.exceptions import InvalidRecoveryStateTransitionError
from app.domain.services.recovery_state_machine import RecoveryStateMachine


@pytest.mark.parametrize(
    ("current_status", "target_status"),
    [
        (
            RecoveryStatus.DETECTED,
            RecoveryStatus.ANALYZING,
        ),
        (
            RecoveryStatus.ANALYZING,
            RecoveryStatus.ELIGIBLE,
        ),
        (
            RecoveryStatus.ELIGIBLE,
            RecoveryStatus.ACTION_PENDING,
        ),
        (
            RecoveryStatus.ACTION_PENDING,
            RecoveryStatus.ACTION_APPROVED,
        ),
        (
            RecoveryStatus.ACTION_APPROVED,
            RecoveryStatus.EXECUTING,
        ),
        (
            RecoveryStatus.EXECUTING,
            RecoveryStatus.RECOVERED,
        ),
        (
            RecoveryStatus.EXECUTING,
            RecoveryStatus.RETRY_SCHEDULED,
        ),
        (
            RecoveryStatus.RETRY_SCHEDULED,
            RecoveryStatus.ACTION_PENDING,
        ),
    ],
)
def test_allows_valid_recovery_state_transitions(
    current_status: RecoveryStatus,
    target_status: RecoveryStatus,
) -> None:
    assert (
        RecoveryStateMachine.can_transition(
            current_status=current_status,
            target_status=target_status,
        )
        is True
    )


@pytest.mark.parametrize(
    ("current_status", "target_status"),
    [
        (
            RecoveryStatus.DETECTED,
            RecoveryStatus.RECOVERED,
        ),
        (
            RecoveryStatus.RECOVERED,
            RecoveryStatus.ANALYZING,
        ),
        (
            RecoveryStatus.STOPPED,
            RecoveryStatus.EXECUTING,
        ),
        (
            RecoveryStatus.ELIGIBLE,
            RecoveryStatus.RECOVERED,
        ),
        (
            RecoveryStatus.ACTION_PENDING,
            RecoveryStatus.EXECUTING,
        ),
    ],
)
def test_rejects_invalid_recovery_state_transitions(
    current_status: RecoveryStatus,
    target_status: RecoveryStatus,
) -> None:
    assert (
        RecoveryStateMachine.can_transition(
            current_status=current_status,
            target_status=target_status,
        )
        is False
    )


def test_validate_transition_does_not_raise_for_valid_transition() -> None:
    RecoveryStateMachine.validate_transition(
        current_status=RecoveryStatus.DETECTED,
        target_status=RecoveryStatus.ANALYZING,
    )


def test_validate_transition_raises_for_invalid_transition() -> None:
    with pytest.raises(InvalidRecoveryStateTransitionError):
        RecoveryStateMachine.validate_transition(
            current_status=RecoveryStatus.RECOVERED,
            target_status=RecoveryStatus.ANALYZING,
        )