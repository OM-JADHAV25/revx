from decimal import Decimal
from uuid import uuid4

from app.domain.entities.recovery_case import RecoveryCase
from app.domain.enums.failure_reason import FailureReason
from app.domain.enums.policy_decision import PolicyDecision
from app.domain.enums.recovery_action import RecoveryAction
from app.domain.models.recovery_policy_config import RecoveryPolicyConfig
from app.domain.models.recovery_proposal import RecoveryProposal
from app.domain.services.recovery_policy import RecoveryPolicy
from app.domain.value_objects.money import Money
from app.domain.value_objects.recovery_probability import RecoveryProbability
from app.domain.value_objects.risk_score import RiskScore


def create_policy() -> RecoveryPolicy:
    return RecoveryPolicy(
        config=RecoveryPolicyConfig(
            minimum_recovery_probability=Decimal("0.40"),
            maximum_risk_score=Decimal("0.70"),
            maximum_retry_count=3,
        )
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


def create_proposal(
    *,
    recovery_case_id,
    probability: Decimal = Decimal("0.80"),
    risk: Decimal = Decimal("0.20"),
    action: RecoveryAction = RecoveryAction.RETRY_PAYMENT,
) -> RecoveryProposal:
    return RecoveryProposal.create(
        recovery_case_id=recovery_case_id,
        failure_reason=FailureReason.INSUFFICIENT_FUNDS,
        proposed_action=action,
        recovery_probability=RecoveryProbability(value=probability),
        risk_score=RiskScore(value=risk),
        rationale="Recovery action is supported by the analysis.",
    )


def test_approves_valid_recovery_proposal() -> None:
    policy = create_policy()
    recovery_case = create_recovery_case()

    proposal = create_proposal(recovery_case_id=recovery_case.recovery_case_id,)

    evaluation = policy.evaluate(recovery_case=recovery_case,proposal=proposal)

    assert evaluation.decision == PolicyDecision.APPROVED


def test_escalates_high_risk_proposal() -> None:
    policy = create_policy()
    recovery_case = create_recovery_case()

    proposal = create_proposal(recovery_case_id=recovery_case.recovery_case_id,risk=Decimal("0.71"),)

    evaluation = policy.evaluate(recovery_case=recovery_case,proposal=proposal)

    assert evaluation.decision == PolicyDecision.ESCALATED


def test_rejects_low_probability_proposal() -> None:
    policy = create_policy()
    recovery_case = create_recovery_case()

    proposal = create_proposal(recovery_case_id=recovery_case.recovery_case_id,probability=Decimal("0.39"),)

    evaluation = policy.evaluate(recovery_case=recovery_case,proposal=proposal)

    assert evaluation.decision == PolicyDecision.REJECTED

def test_approves_retry_when_below_maximum_retry_count() -> None:
    policy = create_policy()

    recovery_case = create_recovery_case(retry_count=2)

    proposal = create_proposal(recovery_case_id=recovery_case.recovery_case_id)

    evaluation = policy.evaluate(recovery_case=recovery_case,proposal=proposal)

    assert evaluation.decision == PolicyDecision.APPROVED


def test_rejects_retry_when_maximum_retry_count_reached() -> None:
    policy = create_policy()

    recovery_case = create_recovery_case(retry_count=3)

    proposal = create_proposal(recovery_case_id=recovery_case.recovery_case_id)

    evaluation = policy.evaluate(recovery_case=recovery_case,proposal=proposal)

    assert evaluation.decision == PolicyDecision.REJECTED


def test_rejects_proposal_for_different_recovery_case() -> None:
    policy = create_policy()
    recovery_case = create_recovery_case()

    proposal = create_proposal(recovery_case_id=uuid4())

    evaluation = policy.evaluate(recovery_case=recovery_case,proposal=proposal)

    assert evaluation.decision == PolicyDecision.REJECTED