"""Domain exceptions of the ticketing system."""


class SoldOutError(RuntimeError):
    """Raised when there are no more tickets available for an event."""


class InvalidTicketStatusError(RuntimeError):
    """Raised on an invalid ticket status transition."""
