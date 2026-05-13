class YoungPersonNotFound(Exception):
    """Raised when a young person record does not exist."""
    pass


class UnauthorisedAccess(Exception):
    """Raised when a user tries to access a case not assigned to them."""
    pass


class InterventionLimitExceeded(Exception):
    """Raised when a young person already has too many active interventions."""
    pass


class InvalidRiskLevel(Exception):
    """Raised when an invalid risk level is assigned to a young person."""
    pass


class OffenceNotFound(Exception):
    """Raised when an offence record does not exist."""
    pass