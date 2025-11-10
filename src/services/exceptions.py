"""Domain-specific exception classes for the finance application.

All custom exceptions subclass ValueError so that existing tests expecting
ValueError keep passing until they are updated to target these explicit types.
"""


class DomainError(ValueError):
    """Base class for domain errors (subclasses ValueError for compatibility)."""


class CategoryNotFoundError(DomainError):
    pass


class CategoryOwnershipError(DomainError):
    pass


class AccountNotFoundError(DomainError):
    pass


class AccountOwnershipError(DomainError):
    pass


class InsufficientBalanceError(DomainError):
    pass


class BudgetExceededError(DomainError):
    pass


class TransactionNotFoundError(DomainError):
    pass


class NoDataToUpdateError(DomainError):
    pass


class CategoryInUseError(DomainError):
    pass


class AccountAccessError(DomainError):
    pass
