from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.recovery_case import RecoveryCase
from app.domain.value_objects.money import Money
from app.domain.value_objects.recovery_probability import (RecoveryProbability)
from app.domain.value_objects.risk_score import RiskScore
from app.infrastructure.persistence.models.recovery_case_model import (RecoveryCaseModel)


class SQLAlchemyRecoveryCaseRepository:
    """SQLAlchemy implementation of the recovery case repository."""

    def __init__(
        self,
        *,
        session: Session,
    ) -> None:
        self._session = session

    def add(
        self,
        *,
        recovery_case: RecoveryCase,
    ) -> None:
        model = self._to_model(recovery_case=recovery_case)

        self._session.add(model)
        self._session.commit()

    def get_by_id(
        self,
        *,
        recovery_case_id: UUID,
    ) -> RecoveryCase | None:
        statement = select(RecoveryCaseModel).where(
            RecoveryCaseModel.recovery_case_id
            == recovery_case_id
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_domain(model=model)

    def update(
        self,
        *,
        recovery_case: RecoveryCase,
    ) -> None:
        model = self._session.get(
            RecoveryCaseModel,
            recovery_case.recovery_case_id,
        )

        if model is None:
            raise ValueError(
                "Recovery case does not exist."
            )

        self._update_model(
            model=model,
            recovery_case=recovery_case,
        )

        self._session.commit()

    @staticmethod
    def _to_model(
        *,
        recovery_case: RecoveryCase,
    ) -> RecoveryCaseModel:
        return RecoveryCaseModel(
            recovery_case_id=recovery_case.recovery_case_id,
            merchant_id=recovery_case.merchant_id,
            payment_id=recovery_case.payment_id,
            customer_id=recovery_case.customer_id,
            subscription_id=recovery_case.subscription_id,
            amount=recovery_case.amount.amount,
            currency=recovery_case.amount.currency,
            status=recovery_case.status,
            recovery_probability=(
                recovery_case.recovery_probability.value
                if recovery_case.recovery_probability is not None
                else None
            ),
            risk_score=(
                recovery_case.risk_score.value
                if recovery_case.risk_score is not None
                else None
            ),
            retry_count=recovery_case.retry_count,
            version=recovery_case.version,
            created_at=recovery_case.created_at,
            updated_at=recovery_case.updated_at,
        )

    @staticmethod
    def _to_domain(
        *,
        model: RecoveryCaseModel,
    ) -> RecoveryCase:
        return RecoveryCase(
            recovery_case_id=model.recovery_case_id,
            merchant_id=model.merchant_id,
            payment_id=model.payment_id,
            amount=Money(
                amount=model.amount,
                currency=model.currency,
            ),
            customer_id=model.customer_id,
            subscription_id=model.subscription_id,
            status=model.status,
            recovery_probability=(
                RecoveryProbability(
                    value=model.recovery_probability
                )
                if model.recovery_probability is not None
                else None
            ),
            risk_score=(
                RiskScore(
                    value=model.risk_score
                )
                if model.risk_score is not None
                else None
            ),
            retry_count=model.retry_count,
            version=model.version,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _update_model(
        *,
        model: RecoveryCaseModel,
        recovery_case: RecoveryCase,
    ) -> None:
        model.merchant_id = recovery_case.merchant_id
        model.payment_id = recovery_case.payment_id
        model.customer_id = recovery_case.customer_id
        model.subscription_id = recovery_case.subscription_id

        model.amount = recovery_case.amount.amount
        model.currency = recovery_case.amount.currency

        model.status = recovery_case.status

        model.recovery_probability = (
            recovery_case.recovery_probability.value
            if recovery_case.recovery_probability is not None
            else None
        )

        model.risk_score = (
            recovery_case.risk_score.value
            if recovery_case.risk_score is not None
            else None
        )

        model.retry_count = recovery_case.retry_count
        model.version = recovery_case.version
        model.updated_at = recovery_case.updated_at