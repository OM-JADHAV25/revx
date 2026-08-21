from __future__ import annotations

from decimal import Decimal
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "RevX"
    app_version: str = "0.1.0"

    minimum_recovery_probability: Decimal = Field(
        default=Decimal("0.40"),
        ge=Decimal("0"),
        le=Decimal("1"),
    )

    maximum_risk_score: Decimal = Field(
        default=Decimal("0.70"),
        ge=Decimal("0"),
        le=Decimal("1"),
    )

    maximum_retry_count: int = Field(
        default=3,
        ge=0,
    )

    high_value_payment_threshold: Decimal = Field(
        default=Decimal("10000"),
        gt=Decimal("0"),
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings."""

    return Settings()