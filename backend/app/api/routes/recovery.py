from uuid import uuid4

from fastapi import APIRouter, Depends

from app.api.dependencies import get_analyze_recovery_case_use_case
from app.api.schemas.analyze_recovery_request import (AnalyzeRecoveryRequest)
from app.api.schemas.analyze_recovery_response import (AnalyzeRecoveryResponse)
from app.application.use_cases.analyze_recovery_case import (AnalyzeRecoveryCase)
from app.domain.entities.recovery_case import RecoveryCase
from app.domain.value_objects.money import Money


router = APIRouter(
    prefix="/recovery-cases",
    tags=["Recovery Cases"],
)


@router.post(
    "/analyze",
    response_model=AnalyzeRecoveryResponse,
)
def analyze_recovery_case(
    request: AnalyzeRecoveryRequest,
    use_case: AnalyzeRecoveryCase = Depends(
        get_analyze_recovery_case_use_case,
    ),
) -> AnalyzeRecoveryResponse:
    recovery_case = RecoveryCase(
        recovery_case_id=uuid4(),
        merchant_id=request.merchant_id,
        payment_id=request.payment_id,
        amount=Money(
            amount=request.amount,
            currency=request.currency,
        ),
        retry_count=request.retry_count,
    )

    result = use_case.execute(recovery_case=recovery_case)

    return AnalyzeRecoveryResponse(
        recovery_case_id=result.recovery_case.recovery_case_id,
        proposal_id=result.proposal.proposal_id,
        status=result.recovery_case.status,
        proposed_action=result.proposal.proposed_action,
        policy_decision=result.policy_evaluation.decision,
        recovery_probability=str(result.proposal.recovery_probability.value),
        risk_score=str(result.proposal.risk_score.value),
        rationale=result.proposal.rationale,
        policy_reason=result.policy_evaluation.reason,
    )