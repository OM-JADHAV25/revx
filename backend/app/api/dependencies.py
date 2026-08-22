from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.use_cases.analyze_recovery_case import (AnalyzeRecoveryCase,)
from app.core.config import get_settings
from app.domain.models.recovery_policy_config import (RecoveryPolicyConfig,)
from app.domain.services.recovery_policy import RecoveryPolicy
from app.infrastructure.analyzers.rule_based_recovery_analyzer import (RuleBasedRecoveryAnalyzer,)
from app.infrastructure.analyzers.rule_based_recovery_analyzer_config import (RuleBasedRecoveryAnalyzerConfig,)
from app.infrastructure.persistence.database import get_db_session
from app.infrastructure.persistence.repositories.sqlalchemy_recovery_case_repository import (SQLAlchemyRecoveryCaseRepository)


def get_recovery_case_repository(
    session: Session = Depends(get_db_session),
) -> SQLAlchemyRecoveryCaseRepository:
    """Provide the PostgreSQL recovery case repository."""

    return SQLAlchemyRecoveryCaseRepository(session=session)


def get_analyze_recovery_case_use_case(
    recovery_case_repository: SQLAlchemyRecoveryCaseRepository = Depends(get_recovery_case_repository)
) -> AnalyzeRecoveryCase:
    """Create and return the AnalyzeRecoveryCase use case."""

    settings = get_settings()

    recovery_analyzer = RuleBasedRecoveryAnalyzer(
        config=RuleBasedRecoveryAnalyzerConfig(
            high_value_payment_threshold=(settings.high_value_payment_threshold)
        )
    )

    recovery_policy = RecoveryPolicy(
        config=RecoveryPolicyConfig(
            minimum_recovery_probability=(settings.minimum_recovery_probability),
            maximum_risk_score=settings.maximum_risk_score,
            maximum_retry_count=settings.maximum_retry_count,
        ),
    )

    return AnalyzeRecoveryCase(
        recovery_analyzer=recovery_analyzer,
        recovery_policy=recovery_policy,
        recovery_case_repository=recovery_case_repository,
    )