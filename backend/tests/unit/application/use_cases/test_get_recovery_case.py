from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from app.application.use_cases.get_recovery_case import (GetRecoveryCase)
from app.domain.entities.recovery_case import RecoveryCase
from app.domain.value_objects.money import Money
from app.infrastructure.repositories.in_memory_recovery_case_repository import (InMemoryRecoveryCaseRepository)


def test_returns_recovery_case_when_it_exists() -> None:
    repository = InMemoryRecoveryCaseRepository()

    recovery_case = RecoveryCase.create(
        merchant_id=uuid4(),
        payment_id=uuid4(),
        amount=Money(
            amount=Decimal("1000.00"),
            currency="INR",
        ),
    )

    repository.add(recovery_case=recovery_case)

    use_case = GetRecoveryCase(recovery_case_repository=repository)

    result = use_case.execute(recovery_case_id=recovery_case.recovery_case_id)

    assert result == recovery_case


def test_returns_none_when_recovery_case_does_not_exist() -> None:
    repository = InMemoryRecoveryCaseRepository()

    use_case = GetRecoveryCase(recovery_case_repository=repository)

    result = use_case.execute(recovery_case_id=uuid4())

    assert result is None