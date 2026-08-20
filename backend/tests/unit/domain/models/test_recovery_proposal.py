from decimal import Decimal
from uuid import uuid4

import pytest

from app.domain.enums.failure_reason import FailureReason
from app.domain.enums.recovery_action import RecoveryAction
from app.domain.exceptions import InvalidRecoveryProposalError
from app.domain.models.recovery_proposal import RecoveryProposal
from app.domain.value_objects.recovery_probability import RecoveryProbability
from app.domain.value_objects.risk_score import RiskScore


def create_recovery_proposal(
    *,
    rationale: str = "Payment retry is likely to succeed.",
) -> RecoveryProposal:
    return RecoveryProposal.create(
        recovery_case_id=uuid4(),
        failure_reason=FailureReason.INSUFFICIENT_FUNDS,
        proposed_action=RecoveryAction.RETRY_PAYMENT,
        recovery_probability=RecoveryProbability(
            value=Decimal("0.87"),
        ),
        risk_score=RiskScore(
            value=Decimal("0.12"),
        ),
        rationale=rationale,
    )


def test_creates_valid_recovery_proposal() -> None:
    proposal = create_recovery_proposal()

    assert proposal.proposal_id is not None
    assert proposal.proposed_action == RecoveryAction.RETRY_PAYMENT
    assert proposal.rationale == "Payment retry is likely to succeed."


def test_recovery_proposal_is_immutable() -> None:
    proposal = create_recovery_proposal()

    with pytest.raises(AttributeError):
        proposal.rationale = "Changed rationale."


@pytest.mark.parametrize(
    "rationale",
    ["","   ","\n",]
)
def test_rejects_empty_rationale(
    rationale: str,
) -> None:
    with pytest.raises(InvalidRecoveryProposalError):
        create_recovery_proposal(
            rationale=rationale,
        )