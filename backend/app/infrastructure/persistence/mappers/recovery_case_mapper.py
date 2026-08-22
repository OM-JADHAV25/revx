from __future__ import annotations

from app.domain.entities.recovery_case import RecoveryCase
from app.domain.value_objects.money import Money
from app.domain.value_objects.recovery_probability import RecoveryProbability
from app.domain.value_objects.risk_score import RiskScore
from app.infrastructure.persistence.models.recovery_case_model import (RecoveryCaseModel)


class RecoveryCaseMapper:
    """Maps between RecoveryCase domain entities and ORM models."""

    @staticmethod
    def to_model(
        recovery_case: RecoveryCase,
    ) -> RecoveryCaseModel:
        """Convert a domain entity into a persistence model."""

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
    def to_domain(
        recovery_case_model: RecoveryCaseModel,
    ) -> RecoveryCase:
        """Convert a persistence model into a domain entity."""

        return RecoveryCase(
            recovery_case_id=recovery_case_model.recovery_case_id,
            merchant_id=recovery_case_model.merchant_id,
            payment_id=recovery_case_model.payment_id,
            amount=Money(
                amount=recovery_case_model.amount,
                currency=recovery_case_model.currency,
            ),
            customer_id=recovery_case_model.customer_id,
            subscription_id=recovery_case_model.subscription_id,
            status=recovery_case_model.status,
            recovery_probability=(
                RecoveryProbability(
                    value=recovery_case_model.recovery_probability
                )
                if recovery_case_model.recovery_probability is not None
                else None
            ),
            risk_score=(
                RiskScore(
                    value=recovery_case_model.risk_score
                )
                if recovery_case_model.risk_score is not None
                else None
            ),
            retry_count=recovery_case_model.retry_count,
            version=recovery_case_model.version,
            created_at=recovery_case_model.created_at,
            updated_at=recovery_case_model.updated_at,
        )