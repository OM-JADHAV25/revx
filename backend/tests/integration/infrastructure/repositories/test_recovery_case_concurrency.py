from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from app.domain.entities.recovery_case import RecoveryCase
from app.domain.enums.recovery_status import RecoveryStatus
from app.domain.exceptions import RecoveryCaseConcurrencyError
from app.domain.value_objects.money import Money
from app.infrastructure.persistence.database import SessionLocal
from app.infrastructure.persistence.repositories.sqlalchemy_recovery_case_repository import (SQLAlchemyRecoveryCaseRepository)

def test_only_one_concurrent_update_succeeds() -> None:
    """Only one update should succeed when two sessions use the same version."""

    # Arrange
    setup_session = SessionLocal()

    recovery_case = RecoveryCase.create(
        merchant_id=uuid4(),
        payment_id=uuid4(),
        amount=Money(
            amount=1000,
            currency="INR",
        ),
    )

    setup_repository = SQLAlchemyRecoveryCaseRepository(session=setup_session)

    setup_repository.add(recovery_case=recovery_case,)

    setup_session.close()

    # Two completely independent database sessions.
    session_one: Session = SessionLocal()
    session_two: Session = SessionLocal()

    repository_one = SQLAlchemyRecoveryCaseRepository(session=session_one)

    repository_two = SQLAlchemyRecoveryCaseRepository(session=session_two)

    try:
        # Both sessions read the same version.
        recovery_case_one = repository_one.get_by_id(recovery_case_id=recovery_case.recovery_case_id)

        recovery_case_two = repository_two.get_by_id(recovery_case_id=recovery_case.recovery_case_id)

        assert recovery_case_one is not None
        assert recovery_case_two is not None

        assert recovery_case_one.version == 1
        assert recovery_case_two.version == 1

        # First session modifies and persists successfully.
        recovery_case_one.transition_to(
            target_status=RecoveryStatus.ANALYZING,
        )

        repository_one.update(recovery_case=recovery_case_one)

        assert recovery_case_one.version == 2

        # Second session still has stale version 1.
        recovery_case_two.transition_to(target_status=RecoveryStatus.ANALYZING)

        # Act + Assert
        with pytest.raises(RecoveryCaseConcurrencyError):
            repository_two.update(recovery_case=recovery_case_two)

    finally:
        session_one.close()
        session_two.close()