from uuid import uuid4

import pytest

from app.domain.enums.policy_decision import PolicyDecision
from app.domain.exceptions import InvalidPolicyEvaluationError
from app.domain.models.policy_evaluation import PolicyEvaluation


def create_policy_evaluation(
    *,
    reason: str = "Recovery action satisfies policy requirements.",
) -> PolicyEvaluation:
    return PolicyEvaluation.create(
        recovery_case_id=uuid4(),
        proposal_id=uuid4(),
        decision=PolicyDecision.APPROVED,
        reason=reason,
    )


def test_creates_valid_policy_evaluation() -> None:
    evaluation = create_policy_evaluation()

    assert evaluation.evaluation_id is not None
    assert evaluation.decision == PolicyDecision.APPROVED
    assert (evaluation.reason == "Recovery action satisfies policy requirements.")


def test_policy_evaluation_is_immutable() -> None:
    evaluation = create_policy_evaluation()

    with pytest.raises(AttributeError):
        evaluation.reason = "Modified reason."


@pytest.mark.parametrize(
    "reason",
    ["","   ","\n",]
)
def test_rejects_empty_policy_evaluation_reason(
    reason: str,
) -> None:
    with pytest.raises(InvalidPolicyEvaluationError):
        create_policy_evaluation(reason=reason)