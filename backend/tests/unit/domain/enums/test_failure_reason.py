from app.domain.enums.failure_reason import FailureReason


def test_failure_reason_values() -> None:
    assert (FailureReason.INSUFFICIENT_FUNDS.value == "insufficient_funds")

    assert (FailureReason.CARD_EXPIRED.value == "card_expired")

    assert (FailureReason.PAYMENT_METHOD_DECLINED.value == "payment_method_declined")

    assert (FailureReason.AUTHENTICATION_REQUIRED.value == "authentication_required")

    assert (FailureReason.PROCESSING_ERROR.value == "processing_error")

    assert FailureReason.NETWORK_ERROR.value == "network_error"
    assert FailureReason.UNKNOWN.value == "unknown"


def test_failure_reason_is_string_enum() -> None:
    assert isinstance(FailureReason.UNKNOWN, str)