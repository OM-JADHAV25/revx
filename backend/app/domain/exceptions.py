class DomainError(Exception):
    """Base exception for all domain-level errors."""


class InvalidMoneyError(DomainError):
    """Raised when a Money value violates domain rules."""