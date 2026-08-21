from decimal import Decimal

from app.application.use_cases.analyze_recovery_case import (AnalyzeRecoveryCase)
from app.domain.models.recovery_policy_config import (RecoveryPolicyConfig)
from app.domain.services.recovery_policy import RecoveryPolicy
from app.infrastructure.analyzers.rule_based_recovery_analyzer import (RuleBasedRecoveryAnalyzer)
from app.infrastructure.analyzers.rule_based_recovery_analyzer_config import (RuleBasedRecoveryAnalyzerConfig)


def get_analyze_recovery_case_use_case() -> AnalyzeRecoveryCase:
    """Create and return the AnalyzeRecoveryCase use case."""

    recovery_analyzer = RuleBasedRecoveryAnalyzer(config=RuleBasedRecoveryAnalyzerConfig())

    recovery_policy = RecoveryPolicy(
        config=RecoveryPolicyConfig(
            minimum_recovery_probability=Decimal("0.40"),
            maximum_risk_score=Decimal("0.70"),
            maximum_retry_count=3,
        )
    )

    return AnalyzeRecoveryCase(
        recovery_analyzer=recovery_analyzer,
        recovery_policy=recovery_policy,
    )