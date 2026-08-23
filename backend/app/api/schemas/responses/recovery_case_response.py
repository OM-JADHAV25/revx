from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, field_serializer

from app.domain.enums.recovery_status import RecoveryStatus


class RecoveryCaseResponse(BaseModel):
    """Response schema for a recovery case."""

    recovery_case_id: UUID

    merchant_id: UUID
    payment_id: UUID

    customer_id: UUID | None
    subscription_id: UUID | None

    amount: Decimal
    currency: str

    status: RecoveryStatus

    recovery_probability: Decimal | None
    risk_score: Decimal | None

    retry_count: int
    version: int

    created_at: datetime
    updated_at: datetime

    @field_serializer("amount")
    def serialize_amount(self, amount: Decimal) -> str:
        return format(amount.normalize(), "f")