from uuid import uuid4
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Depends

from app.api.dependencies import get_analyze_recovery_case_use_case
from app.api.schemas.requests.analyze_recovery_request import (AnalyzeRecoveryRequest)
from app.api.schemas.responses.analyze_recovery_response import (AnalyzeRecoveryResponse)
from app.application.use_cases.analyze_recovery_case import (AnalyzeRecoveryCase)
from app.domain.entities.recovery_case import RecoveryCase
from app.domain.value_objects.money import Money
from app.api.dependencies import get_recovery_case_use_case
from app.api.schemas.responses.recovery_case_response import (RecoveryCaseResponse)
from app.application.use_cases.get_recovery_case import (GetRecoveryCase)
from app.api.mappers.recovery_case_response_mapper import to_recovery_case_response


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


@router.get(
    "/{recovery_case_id}",
    response_model=RecoveryCaseResponse,
)
def get_recovery_case(
    recovery_case_id: UUID,
    use_case: GetRecoveryCase = Depends(
        get_recovery_case_use_case,
    ),
) -> RecoveryCaseResponse:
    """Retrieve a recovery case by its identifier."""

    recovery_case = use_case.execute(recovery_case_id=recovery_case_id)

    if recovery_case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recovery case not found.",
        )

    return to_recovery_case_response(
        recovery_case=recovery_case,
    )