from decimal import Decimal
from uuid import uuid4

import pytest

from app.domain.entities.recovery_case import RecoveryCase
from app.domain.value_objects.money import Money
from app.infrastructure.repositories.in_memory_recovery_case_repository import (
    InMemoryRecoveryCaseRepository,
)


def create_recovery_case() -> RecoveryCase:
    return RecoveryCase(
        recovery_case_id=uuid4(),
        merchant_id=uuid4(),
        payment_id=uuid4(),
        amount=Money(
            amount=Decimal("1000"),
            currency="INR",
        ),
    )


def test_add_and_get_recovery_case() -> None:
    repository = InMemoryRecoveryCaseRepository()
    recovery_case = create_recovery_case()

    repository.add(recovery_case=recovery_case)

    stored_recovery_case = repository.get_by_id(recovery_case_id=recovery_case.recovery_case_id)

    assert stored_recovery_case == recovery_case


def test_returns_none_when_recovery_case_does_not_exist() -> None:
    repository = InMemoryRecoveryCaseRepository()

    recovery_case = repository.get_by_id(recovery_case_id=uuid4())

    assert recovery_case is None


def test_rejects_duplicate_recovery_case() -> None:
    repository = InMemoryRecoveryCaseRepository()
    recovery_case = create_recovery_case()

    repository.add(recovery_case=recovery_case)

    with pytest.raises(ValueError):
        repository.add(recovery_case=recovery_case)


def test_updates_existing_recovery_case() -> None:
    repository = InMemoryRecoveryCaseRepository()
    recovery_case = create_recovery_case()

    repository.add(recovery_case=recovery_case)

    repository.update(recovery_case=recovery_case)

    updated_recovery_case = repository.get_by_id(recovery_case_id=recovery_case.recovery_case_id)

    assert updated_recovery_case == recovery_case


def test_rejects_updating_nonexistent_recovery_case() -> None:
    repository = InMemoryRecoveryCaseRepository()

    recovery_case = create_recovery_case()

    with pytest.raises(ValueError):
        repository.update(recovery_case=recovery_case)