from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from app.application.use_cases.transition_recovery_case import (TransitionRecoveryCase)
from app.domain.entities.recovery_case import RecoveryCase
from app.domain.enums.recovery_status import RecoveryStatus
from app.domain.value_objects.money import Money
from app.infrastructure.repositories.in_memory_recovery_case_repository import (InMemoryRecoveryCaseRepository)


def create_recovery_case() -> RecoveryCase:
    """Create a recovery case for testing."""

    return RecoveryCase.create(
        merchant_id=uuid4(),
        payment_id=uuid4(),
        amount=Money(
            amount=Decimal("1000"),
            currency="INR",
        ),
    )


def test_transitions_existing_recovery_case() -> None:
    """An existing recovery case should transition and persist."""

    repository = InMemoryRecoveryCaseRepository()

    recovery_case = create_recovery_case()

    repository.add(recovery_case=recovery_case,)

    use_case = TransitionRecoveryCase(recovery_case_repository=repository)

    result = use_case.execute(
        recovery_case_id=recovery_case.recovery_case_id,
        target_status=RecoveryStatus.ANALYZING,
    )

    assert result is not None
    assert result.status == RecoveryStatus.ANALYZING

    persisted_case = repository.get_by_id(recovery_case_id=recovery_case.recovery_case_id)

    assert persisted_case is not None
    assert persisted_case.status == RecoveryStatus.ANALYZING


def test_returns_none_when_recovery_case_does_not_exist() -> None:
    """A missing recovery case should return None."""

    repository = InMemoryRecoveryCaseRepository()

    use_case = TransitionRecoveryCase(recovery_case_repository=repository)

    result = use_case.execute(
        recovery_case_id=uuid4(),
        target_status=RecoveryStatus.ANALYZING,
    )

    assert result is None