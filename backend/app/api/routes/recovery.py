from uuid import uuid4
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import (
    get_analyze_recovery_case_use_case,
    get_recovery_case_use_case,
    get_transition_recovery_case_use_case,
)
from app.api.schemas.requests.analyze_recovery_request import (AnalyzeRecoveryRequest)
from app.api.schemas.requests.transition_recovery_case_request import (TransitionRecoveryCaseRequest)
from app.api.schemas.responses.analyze_recovery_response import (AnalyzeRecoveryResponse)
from app.api.schemas.responses.recovery_case_response import (RecoveryCaseResponse)
from app.application.use_cases.analyze_recovery_case import (AnalyzeRecoveryCase)
from app.application.use_cases.get_recovery_case import (GetRecoveryCase)
from app.application.use_cases.transition_recovery_case import (TransitionRecoveryCase)
from app.api.mappers.recovery_case_response_mapper import (to_recovery_case_response)
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


@router.patch(
    "/{recovery_case_id}/status",
    response_model=RecoveryCaseResponse,
)
def transition_recovery_case(
    recovery_case_id: UUID,
    request: TransitionRecoveryCaseRequest,
    use_case: TransitionRecoveryCase = Depends(
        get_transition_recovery_case_use_case,
    ),
) -> RecoveryCaseResponse:
    """Transition a recovery case to a new status."""

    recovery_case = use_case.execute(
        recovery_case_id=recovery_case_id,
        target_status=request.target_status,
    )

    if recovery_case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recovery case not found.",
        )

    return RecoveryCaseResponse(
        recovery_case_id=recovery_case.recovery_case_id,
        merchant_id=recovery_case.merchant_id,
        payment_id=recovery_case.payment_id,
        customer_id=recovery_case.customer_id,
        subscription_id=recovery_case.subscription_id,
        amount=recovery_case.amount.amount,
        currency=recovery_case.amount.currency,
        status=recovery_case.status,
        recovery_probability=(
            recovery_case.recovery_probability.value
            if recovery_case.recovery_probability is not None
            else None
        ),
        risk_score=(
            recovery_case.risk_score.value
            if recovery_case.risk_score is not None
            else None
        ),
        retry_count=recovery_case.retry_count,
        version=recovery_case.version,
        created_at=recovery_case.created_at,
        updated_at=recovery_case.updated_at,
    )