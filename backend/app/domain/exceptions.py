class DomainError(Exception):
    """Base exception for all domain-level errors."""


class InvalidMoneyError(DomainError):
    """Raised when a Money value violates domain rules."""


class InvalidRecoveryProbabilityError(DomainError):
    """Raised when a recovery probability is outside the valid range."""


class InvalidRiskScoreError(DomainError):
    """Raised when a risk score is outside the valid range."""