from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

import pytest

from app.domain.entities.recovery_case import RecoveryCase
from app.domain.enums.recovery_status import RecoveryStatus
from app.domain.exceptions import (
    InvalidRecoveryCaseError,
    InvalidRecoveryStateTransitionError,
)
from app.domain.value_objects.money import Money


def create_recovery_case() -> RecoveryCase:
    return RecoveryCase.create(
        merchant_id=uuid4(),
        payment_id=uuid4(),
        amount=Money(
            amount=Decimal("1499.00"),
            currency="INR",
        ),
    )


def test_creates_recovery_case() -> None:
    recovery_case = create_recovery_case()

    assert recovery_case.recovery_case_id is not None
    assert recovery_case.status == RecoveryStatus.DETECTED
    assert recovery_case.retry_count == 0
    assert recovery_case.version == 1


def test_recovery_case_has_utc_timestamps() -> None:
    recovery_case = create_recovery_case()

    assert recovery_case.created_at.tzinfo == timezone.utc
    assert recovery_case.updated_at.tzinfo == timezone.utc


def test_transitions_to_valid_state() -> None:
    recovery_case = create_recovery_case()

    recovery_case.transition_to(
        RecoveryStatus.ANALYZING
    )

    assert recovery_case.status == RecoveryStatus.ANALYZING
    assert recovery_case.version == 2


def test_invalid_transition_does_not_modify_case() -> None:
    recovery_case = create_recovery_case()

    original_status = recovery_case.status
    original_version = recovery_case.version
    original_updated_at = recovery_case.updated_at

    with pytest.raises(InvalidRecoveryStateTransitionError):
        recovery_case.transition_to(
            RecoveryStatus.RECOVERED
        )

    assert recovery_case.status == original_status
    assert recovery_case.version == original_version
    assert recovery_case.updated_at == original_updated_at


def test_rejects_negative_retry_count() -> None:
    with pytest.raises(InvalidRecoveryCaseError):
        RecoveryCase(
            recovery_case_id=uuid4(),
            merchant_id=uuid4(),
            payment_id=uuid4(),
            amount=Money(
                amount=Decimal("100"),
                currency="INR",
            ),
            retry_count=-1,
        )


def test_rejects_invalid_version() -> None:
    with pytest.raises(InvalidRecoveryCaseError):
        RecoveryCase(
            recovery_case_id=uuid4(),
            merchant_id=uuid4(),
            payment_id=uuid4(),
            amount=Money(
                amount=Decimal("100"),
                currency="INR",
            ),
            version=0,
        )