from __future__ import annotations

from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.domain.entities.recovery_case import RecoveryCase
from app.domain.enums.recovery_status import RecoveryStatus
from app.domain.value_objects.money import Money
from app.domain.value_objects.recovery_probability import (RecoveryProbability)
from app.domain.value_objects.risk_score import RiskScore
from app.infrastructure.persistence.base import Base
from app.infrastructure.persistence.models.recovery_case_model import (RecoveryCaseModel)
from app.infrastructure.persistence.repositories.sqlalchemy_recovery_case_repository import (SQLAlchemyRecoveryCaseRepository)


def create_test_session() -> Session:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    return Session(engine)


def create_recovery_case(
    *,
    payment_id: UUID | None = None,
    ) -> RecoveryCase:
        return RecoveryCase.create(
            merchant_id=uuid4(),
            payment_id=payment_id or uuid4(),
            amount=Money(
                amount=Decimal("1000.00"),
                currency="INR"
            )
        )


def test_add_and_get_by_id() -> None:
    session = create_test_session()

    repository = SQLAlchemyRecoveryCaseRepository(session=session)

    recovery_case = create_recovery_case()

    repository.add(recovery_case=recovery_case)

    retrieved_case = repository.get_by_id(recovery_case_id=recovery_case.recovery_case_id,)

    assert retrieved_case is not None

    assert (retrieved_case.recovery_case_id == recovery_case.recovery_case_id)

    assert (retrieved_case.merchant_id == recovery_case.merchant_id)

    assert (retrieved_case.payment_id == recovery_case.payment_id)

    assert retrieved_case.amount == recovery_case.amount

    assert retrieved_case.status == RecoveryStatus.DETECTED


def test_get_by_id_returns_none_when_case_does_not_exist() -> None:
    session = create_test_session()

    repository = SQLAlchemyRecoveryCaseRepository(session=session)

    recovery_case = repository.get_by_id(recovery_case_id=uuid4(),)

    assert recovery_case is None


def test_update_persists_recovery_case_changes() -> None:
    session = create_test_session()

    repository = SQLAlchemyRecoveryCaseRepository(session=session)

    recovery_case = create_recovery_case()

    repository.add(recovery_case=recovery_case)

    recovery_case.status = RecoveryStatus.ANALYZING

    recovery_case.recovery_probability = RecoveryProbability(value=Decimal("0.85"),)

    recovery_case.risk_score = RiskScore(value=Decimal("0.20"))

    recovery_case.retry_count = 1
    recovery_case.version = 2

    repository.update(recovery_case=recovery_case,)

    retrieved_case = repository.get_by_id(recovery_case_id=recovery_case.recovery_case_id)

    assert retrieved_case is not None

    assert retrieved_case.status == RecoveryStatus.ANALYZING

    assert retrieved_case.recovery_probability == (
        RecoveryProbability(value=Decimal("0.85"))
    )

    assert retrieved_case.risk_score == (
        RiskScore(value=Decimal("0.20"))
    )

    assert retrieved_case.retry_count == 1

    assert retrieved_case.version == 2


def test_get_by_payment_id_returns_matching_recovery_case() -> None:
    session = create_test_session()

    repository = SQLAlchemyRecoveryCaseRepository(session=session)

    recovery_case = create_recovery_case()

    repository.add(recovery_case=recovery_case)

    retrieved_case = repository.get_by_payment_id(payment_id=recovery_case.payment_id)

    assert retrieved_case is not None

    assert (retrieved_case.recovery_case_id == recovery_case.recovery_case_id)

    assert (retrieved_case.payment_id == recovery_case.payment_id)


def test_get_by_payment_id_returns_none_when_case_does_not_exist() -> None:
    session = create_test_session()

    repository = SQLAlchemyRecoveryCaseRepository(session=session)

    recovery_case = repository.get_by_payment_id(payment_id=uuid4())

    assert recovery_case is None


def test_rejects_duplicate_payment_id_at_database_level() -> None:
    session = create_test_session()

    repository = SQLAlchemyRecoveryCaseRepository(session=session)

    payment_id = uuid4()

    first_recovery_case = create_recovery_case(payment_id=payment_id)

    second_recovery_case = create_recovery_case(payment_id=payment_id)

    repository.add(recovery_case=first_recovery_case)

    with pytest.raises(IntegrityError):
        repository.add(recovery_case=second_recovery_case)


def test_database_rejects_duplicate_payment_id() -> None:
    """Database must enforce one recovery case per payment."""

    session = create_test_session()

    repository = SQLAlchemyRecoveryCaseRepository(session=session)

    payment_id = uuid4()

    first_recovery_case = create_recovery_case(payment_id=payment_id)

    second_recovery_case = create_recovery_case(payment_id=payment_id)

    repository.add(recovery_case=first_recovery_case,)

    with pytest.raises(IntegrityError):
        repository.add(recovery_case=second_recovery_case)

    session.rollback()

    stored_recovery_case = repository.get_by_payment_id(payment_id=payment_id)

    assert stored_recovery_case is not None

    assert (stored_recovery_case.recovery_case_id == first_recovery_case.recovery_case_id)

    assert stored_recovery_case.payment_id == payment_id