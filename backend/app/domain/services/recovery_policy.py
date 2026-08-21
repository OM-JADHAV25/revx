from __future__ import annotations

from app.domain.entities.recovery_case import RecoveryCase
from app.domain.enums.policy_decision import PolicyDecision
from app.domain.enums.recovery_action import RecoveryAction
from app.domain.models.policy_evaluation import PolicyEvaluation
from app.domain.models.recovery_policy_config import RecoveryPolicyConfig
from app.domain.models.recovery_proposal import RecoveryProposal


class RecoveryPolicy:
    """Evaluates recovery proposals against deterministic policy rules."""

    def __init__(
        self,
        config: RecoveryPolicyConfig,
    ) -> None:
        self._config = config

    def evaluate(
        self,
        *,
        recovery_case: RecoveryCase,
        proposal: RecoveryProposal,
    ) -> PolicyEvaluation:

        if recovery_case.recovery_case_id != proposal.recovery_case_id:
            return PolicyEvaluation.create(
                recovery_case_id=recovery_case.recovery_case_id,
                proposal_id=proposal.proposal_id,
                decision=PolicyDecision.REJECTED,
                reason="Recovery proposal does not belong to the recovery case.",
            )

        if proposal.risk_score.value > self._config.maximum_risk_score:
            return PolicyEvaluation.create(
                recovery_case_id=recovery_case.recovery_case_id,
                proposal_id=proposal.proposal_id,
                decision=PolicyDecision.ESCALATED,
                reason="Recovery proposal exceeds the maximum allowed risk score.",
            )

        if (
            proposal.recovery_probability.value
            < self._config.minimum_recovery_probability
        ):
            return PolicyEvaluation.create(
                recovery_case_id=recovery_case.recovery_case_id,
                proposal_id=proposal.proposal_id,
                decision=PolicyDecision.REJECTED,
                reason="Recovery probability is below the minimum policy threshold.",
            )

        if (
            proposal.proposed_action == RecoveryAction.RETRY_PAYMENT
            and recovery_case.retry_count >= self._config.maximum_retry_count
        ):
            return PolicyEvaluation.create(
                recovery_case_id=recovery_case.recovery_case_id,
                proposal_id=proposal.proposal_id,
                decision=PolicyDecision.REJECTED,
                reason="Maximum retry count has been reached.",
            )

        return PolicyEvaluation.create(
            recovery_case_id=recovery_case.recovery_case_id,
            proposal_id=proposal.proposal_id,
            decision=PolicyDecision.APPROVED,
            reason="Recovery proposal satisfies all policy requirements.",
        )