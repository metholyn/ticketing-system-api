"""Venue class -- the place where events are held."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Venue:
    """A physical or virtual venue where events are held.

    The :class:`~app.event.Event` class has a dependency (composition)
    on this class: every event is held at a particular venue.

    Attributes:
        venue_id: Unique identifier of the venue.
        name: Name of the venue.
        address: Address of the venue.
        capacity: Maximum capacity (number of attendees).
    """

    venue_id: int
    name: str
    address: str
    capacity: int

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ValueError("capacity must be a positive number")
