from app.domain.enums.recovery_status import RecoveryStatus


def test_recovery_status_values() -> None:
    assert RecoveryStatus.DETECTED.value == "detected"
    assert RecoveryStatus.ANALYZING.value == "analyzing"
    assert RecoveryStatus.ELIGIBLE.value == "eligible"
    assert RecoveryStatus.ACTION_PENDING.value == "action_pending"
    assert RecoveryStatus.ACTION_APPROVED.value == "action_approved"
    assert RecoveryStatus.EXECUTING.value == "executing"
    assert RecoveryStatus.RETRY_SCHEDULED.value == "retry_scheduled"
    assert RecoveryStatus.RECOVERED.value == "recovered"
    assert RecoveryStatus.ESCALATED.value == "escalated"
    assert RecoveryStatus.STOPPED.value == "stopped"


def test_recovery_status_is_string_enum() -> None:
    assert isinstance(RecoveryStatus.DETECTED, str)