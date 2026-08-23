from __future__ import annotations

from app.api.schemas.responses.recovery_case_response import (RecoveryCaseResponse)
from app.domain.entities.recovery_case import RecoveryCase


def to_recovery_case_response(
    recovery_case: RecoveryCase,
) -> RecoveryCaseResponse:
    """Map a RecoveryCase domain entity to an API response."""

    return RecoveryCaseResponse(
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