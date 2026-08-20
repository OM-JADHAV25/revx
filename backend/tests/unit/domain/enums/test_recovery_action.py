from app.domain.enums.recovery_action import RecoveryAction


def test_recovery_action_values() -> None:
    assert (RecoveryAction.RETRY_PAYMENT.value == "retry_payment")

    assert (RecoveryAction.REQUEST_PAYMENT_METHOD_UPDATE.value == "request_payment_method_update")

    assert (RecoveryAction.REQUEST_AUTHENTICATION.value == "request_authentication")

    assert (RecoveryAction.ESCALATE_TO_MERCHANT.value == "escalate_to_merchant")

    assert (RecoveryAction.STOP_RECOVERY.value == "stop_recovery")


def test_recovery_action_is_string_enum() -> None:
    assert isinstance(RecoveryAction.RETRY_PAYMENT, str)