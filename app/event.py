"""Event class -- an event that tickets are sold for."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.exceptions import SoldOutError
from app.person import Organizer
from app.venue import Venue


@dataclass
class Event:
    """An event (concert, show, match, etc.) that tickets are sold for.

    The class depends on :class:`~app.person.Organizer` (who runs the
    event) and :class:`~app.venue.Venue` (where it takes place) --
    both are passed into the constructor as objects rather than ids,
    which demonstrates a compositional dependency between the model
    classes.

    Attributes:
        event_id: Unique identifier of the event.
        title: Title of the event.
        start_time: Date and time the event starts.
        organizer: Organizer of the event (:class:`Organizer`).
        venue: Venue where the event is held (:class:`Venue`).
        ticket_price: Base price of a ticket.
        total_tickets: Total number of tickets on sale.
        sold_tickets: Number of tickets already sold.
    """

    event_id: int
    title: str
    start_time: datetime
    organizer: Organizer
    venue: Venue
    ticket_price: float
    total_tickets: int
    sold_tickets: int = 0

    def __post_init__(self) -> None:
        if self.total_tickets > self.venue.capacity:
            raise ValueError(
                "total_tickets cannot exceed the venue's capacity"
            )
        self.organizer.add_event(self.event_id)

    @property
    def available_tickets(self) -> int:
        """Number of tickets that are still available for sale."""
        return self.total_tickets - self.sold_tickets

    def is_sold_out(self) -> bool:
        """Checks whether all tickets for the event have been sold."""
        return self.available_tickets <= 0

    def reserve_ticket(self) -> None:
        """Reserves one ticket, incrementing the sold-ticket counter.

        Raises:
            SoldOutError: if there are no more tickets available.
        """
        if self.is_sold_out():
            raise SoldOutError(f"Event {self.title!r} is sold out")
        self.sold_tickets += 1

    def release_ticket(self) -> None:
        """Returns one ticket back to the pool (reservation cancelled)."""
        if self.sold_tickets > 0:
            self.sold_tickets -= 1
