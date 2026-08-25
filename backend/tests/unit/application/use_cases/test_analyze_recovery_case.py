from decimal import Decimal
from uuid import uuid4

from app.application.use_cases.analyze_recovery_case import (AnalyzeRecoveryCase)
from app.domain.entities.recovery_case import RecoveryCase
from app.domain.enums.failure_reason import FailureReason
from app.domain.enums.policy_decision import PolicyDecision
from app.domain.enums.recovery_action import RecoveryAction
from app.domain.models.recovery_policy_config import RecoveryPolicyConfig
from app.domain.models.recovery_proposal import RecoveryProposal
from app.domain.services.recovery_policy import RecoveryPolicy
from app.domain.value_objects.money import Money
from app.domain.value_objects.recovery_probability import (RecoveryProbability,)
from app.domain.value_objects.risk_score import RiskScore
from app.infrastructure.repositories.in_memory_recovery_case_repository import (InMemoryRecoveryCaseRepository)


class StubRecoveryAnalyzer:
    def analyze(
        self,
        *,
        recovery_case: RecoveryCase,
    ) -> RecoveryProposal:
        return RecoveryProposal.create(
            recovery_case_id=recovery_case.recovery_case_id,
            failure_reason=FailureReason.INSUFFICIENT_FUNDS,
            proposed_action=RecoveryAction.RETRY_PAYMENT,
            recovery_probability=RecoveryProbability(value=Decimal("0.85")),
            risk_score=RiskScore(value=Decimal("0.15")),
            rationale="The recovery proposal is valid."
        )


def create_recovery_case(
    *,
    retry_count: int = 0,
) -> RecoveryCase:
    return RecoveryCase(
        recovery_case_id=uuid4(),
        merchant_id=uuid4(),
        payment_id=uuid4(),
        amount=Money(
            amount=Decimal("1000"),
            currency="INR",
        ),
        retry_count=retry_count,
    )


def create_recovery_policy() -> RecoveryPolicy:
    return RecoveryPolicy(
        config=RecoveryPolicyConfig(
            minimum_recovery_probability=Decimal("0.40"),
            maximum_risk_score=Decimal("0.70"),
            maximum_retry_count=3,
        )
    )


def create_use_case(
    *,
    repository: InMemoryRecoveryCaseRepository,
) -> AnalyzeRecoveryCase:
    return AnalyzeRecoveryCase(
        recovery_analyzer=StubRecoveryAnalyzer(),
        recovery_policy=create_recovery_policy(),
        recovery_case_repository=repository,
    )


def test_analyzes_and_persists_approved_recovery_case() -> None:
    repository = InMemoryRecoveryCaseRepository()

    use_case = create_use_case(
        repository=repository,
    )

    recovery_case = create_recovery_case()

    result = use_case.execute(recovery_case=recovery_case)

    stored_recovery_case = repository.get_by_id(recovery_case_id=recovery_case.recovery_case_id)

    assert (result.policy_evaluation.decision == PolicyDecision.APPROVED)

    assert stored_recovery_case is not None

    assert (stored_recovery_case.recovery_case_id == recovery_case.recovery_case_id)

    assert (stored_recovery_case.status == result.recovery_case.status)


def test_analyzes_and_persists_rejected_recovery_case() -> None:
    repository = InMemoryRecoveryCaseRepository()

    use_case = create_use_case(repository=repository)

    recovery_case = create_recovery_case(retry_count=3)

    result = use_case.execute(recovery_case=recovery_case)

    stored_recovery_case = repository.get_by_id(recovery_case_id=recovery_case.recovery_case_id)

    assert (result.policy_evaluation.decision == PolicyDecision.REJECTED)

    assert stored_recovery_case is not None

    assert (stored_recovery_case.status == result.recovery_case.status)


def test_returns_existing_recovery_case_for_duplicate_payment() -> None:
    repository = InMemoryRecoveryCaseRepository()

    use_case = create_use_case(repository=repository)

    original_recovery_case = create_recovery_case()

    original_result = use_case.execute(recovery_case=original_recovery_case)

    duplicate_recovery_case = RecoveryCase(
        recovery_case_id=uuid4(),
        merchant_id=original_recovery_case.merchant_id,
        payment_id=original_recovery_case.payment_id,
        amount=original_recovery_case.amount,
    )

    duplicate_result = use_case.execute(recovery_case=duplicate_recovery_case)

    assert (duplicate_result.recovery_case.recovery_case_id == original_result.recovery_case.recovery_case_id)

    assert (duplicate_result.recovery_case.payment_id == original_result.recovery_case.payment_id)

    assert (
        repository.get_by_id(recovery_case_id=duplicate_recovery_case.recovery_case_id)
        is None
    )