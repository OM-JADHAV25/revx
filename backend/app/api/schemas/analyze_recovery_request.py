from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class AnalyzeRecoveryRequest(BaseModel):
    merchant_id: UUID
    payment_id: UUID

    amount: Decimal = Field(
        gt=0,
        max_digits=18,
        decimal_places=2,
    )

    currency: str = Field(
        min_length=3,
        max_length=3,
    )

    retry_count: int = Field(
        default=0,
        ge=0,
    )