"""Ticket class -- a ticket to an event and its possible statuses."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from app.event import Event
from app.exceptions import InvalidTicketStatusError
from app.person import User


class TicketStatus(str, Enum):
    """Possible statuses of a ticket throughout its lifecycle."""

    RESERVED = "reserved"
    PAID = "paid"
    CANCELLED = "cancelled"


#: Allowed transitions between ticket statuses.
_ALLOWED_TRANSITIONS: dict[TicketStatus, set[TicketStatus]] = {
    TicketStatus.RESERVED: {TicketStatus.PAID, TicketStatus.CANCELLED},
    TicketStatus.PAID: {TicketStatus.CANCELLED},
    TicketStatus.CANCELLED: set(),
}


@dataclass
class Ticket:
    """A ticket that links a specific user to a specific event.

    The class has two dependencies: on :class:`~app.event.Event`
    (which event the ticket was issued for) and on
    :class:`~app.person.User` (who the ticket belongs to). On
    creation, the ticket automatically reserves a seat at the event
    and registers itself with the owning user.

    Attributes:
        ticket_id: Unique identifier of the ticket.
        event: The event this ticket was issued for.
        owner: The owner of the ticket.
        seat_number: Seat number (if applicable).
        status: Current status of the ticket (:class:`TicketStatus`).
        purchase_time: Time the ticket was created/reserved.
    """

    ticket_id: int
    event: Event
    owner: User
    seat_number: str
    status: TicketStatus = TicketStatus.RESERVED
    purchase_time: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        self.event.reserve_ticket()
        self.owner.add_ticket(self.ticket_id)

    def pay(self) -> None:
        """Transitions the ticket to the PAID status.

        Raises:
            InvalidTicketStatusError: if the transition to PAID is not
                allowed from the current state.
        """
        self._transition(TicketStatus.PAID)

    def cancel(self) -> None:
        """Cancels the ticket and returns the seat to the pool of sale."""
        self._transition(TicketStatus.CANCELLED)
        self.event.release_ticket()

    def _transition(self, new_status: TicketStatus) -> None:
        """Validates and performs a transition between ticket statuses.

        Args:
            new_status: The desired new status.

        Raises:
            InvalidTicketStatusError: if the transition is not allowed.
        """
        if new_status not in _ALLOWED_TRANSITIONS[self.status]:
            raise InvalidTicketStatusError(
                f"Cannot transition from {self.status} to {new_status}"
            )
        self.status = new_status
