class DomainError(Exception):
    """Base exception for all domain-level errors."""


class InvalidMoneyError(DomainError):
    """Raised when a Money value violates domain rules."""


class InvalidRecoveryProbabilityError(DomainError):
    """Raised when a recovery probability is outside the valid range."""


class InvalidRiskScoreError(DomainError):
    """Raised when a risk score is outside the valid range."""


class InvalidRecoveryStateTransitionError(DomainError):
    """Raised when a recovery case attempts an invalid state transition."""


class InvalidRecoveryCaseError(DomainError):
    """Raised when a recovery case violates a domain invariant."""


class InvalidRecoveryProposalError(DomainError):
    """Raised when a recovery proposal violates a domain invariant."""


class InvalidPolicyEvaluationError(DomainError):
    """Raised when a policy evaluation violates a domain invariant."""


class InvalidRecoveryPolicyConfigError(DomainError):
    """Raised when recovery policy configuration is invalid."""