"""Base classes for the people involved in the system: Person, User, Organizer.

This module demonstrates an inheritance relationship: User and
Organizer both inherit shared attributes and behaviour from the
abstract class Person.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class InvalidEmailError(ValueError):
    """Raised when an invalid e-mail address is assigned to a person."""


@dataclass
class Person(ABC):
    """Abstract base class for any natural person in the system.

    Acts as the parent class of :class:`User` and :class:`Organizer`
    and encapsulates the shared fields (id, name, e-mail) together
    with their validation.

    Attributes:
        person_id: Unique identifier of the person.
        full_name: Full name of the person.
        email: E-mail address of the person (validated on creation).
    """

    person_id: int
    full_name: str
    email: str

    def __post_init__(self) -> None:
        if not _EMAIL_RE.match(self.email):
            raise InvalidEmailError(f"Invalid email: {self.email!r}")

    @abstractmethod
    def role(self) -> str:
        """Returns the role of the person in the system.

        Returns:
            A string representation of the role ("User" or "Organizer").
        """
        raise NotImplementedError

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.role()}#{self.person_id} ({self.full_name})"


@dataclass
class User(Person):
    """A user (attendee) who buys tickets to events.

    Inherits from :class:`Person`. Keeps a list of the ids of the
    tickets that belong to the user (a one-to-many association with
    :class:`~app.ticket.Ticket`, stored by id to avoid a circular
    module dependency).

    Attributes:
        phone: User's contact phone number.
        ticket_ids: List of ids of the tickets purchased by the user.
    """

    phone: str = ""
    ticket_ids: list[int] = field(default_factory=list)

    def role(self) -> str:
        return "User"

    def add_ticket(self, ticket_id: int) -> None:
        """Adds the id of a purchased ticket to the user's ticket list.

        Args:
            ticket_id: Id of the purchased ticket.
        """
        self.ticket_ids.append(ticket_id)

    def ticket_count(self) -> int:
        """Returns the number of tickets owned by the user."""
        return len(self.ticket_ids)


@dataclass
class Organizer(Person):
    """An organizer who creates and runs events.

    Inherits from :class:`Person`. Has a one-to-many dependency on
    :class:`~app.event.Event`: a single organizer can run several
    events.

    Attributes:
        organization_name: Name of the organizer's organization.
        event_ids: List of ids of the events run by this organizer.
    """

    organization_name: str = ""
    event_ids: list[int] = field(default_factory=list)

    def role(self) -> str:
        return "Organizer"

    def add_event(self, event_id: int) -> None:
        """Registers a newly created event under this organizer.

        Args:
            event_id: Id of the created event.
        """
        self.event_ids.append(event_id)
