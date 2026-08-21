from app.domain.enums.policy_decision import PolicyDecision


def test_policy_decision_values() -> None:
    assert PolicyDecision.APPROVED.value == "approved"
    assert PolicyDecision.REJECTED.value == "rejected"
    assert PolicyDecision.ESCALATED.value == "escalated"


def test_policy_decision_is_string_enum() -> None:
    assert isinstance(PolicyDecision.APPROVED, str)