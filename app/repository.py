"""In-memory repositories for storing the model entities.

The :class:`TicketingRepository` class aggregates all the other model
classes (Person, Venue, Event, Ticket) and provides a single access
point for the application layer (CLI or REST API).
"""

from __future__ import annotations

from itertools import count
from typing import Optional

from app.event import Event
from app.person import Organizer, User
from app.ticket import Ticket
from app.venue import Venue


class TicketingRepository:
    """Aggregates and stores all entities of the ticketing system.

    This is the highest level of composition in the model: the
    repository owns the collections of organizers, users, venues,
    events and tickets, and is responsible for generating new ids.
    """

    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._organizers: dict[int, Organizer] = {}
        self._venues: dict[int, Venue] = {}
        self._events: dict[int, Event] = {}
        self._tickets: dict[int, Ticket] = {}
        self._id_counter = count(1)

    def _next_id(self) -> int:
        return next(self._id_counter)

    # -- Users ---------------------------------------------------------
    def add_user(self, full_name: str, email: str, phone: str = "") -> User:
        """Creates and stores a new user."""
        user = User(person_id=self._next_id(), full_name=full_name, email=email, phone=phone)
        self._users[user.person_id] = user
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        """Returns the user with the given id, or None."""
        return self._users.get(user_id)

    def list_users(self) -> list[User]:
        """Returns the list of all users."""
        return list(self._users.values())

    # -- Organizers ------------------------------------------------------
    def add_organizer(self, full_name: str, email: str, organization_name: str = "") -> Organizer:
        """Creates and stores a new organizer."""
        organizer = Organizer(
            person_id=self._next_id(),
            full_name=full_name,
            email=email,
            organization_name=organization_name,
        )
        self._organizers[organizer.person_id] = organizer
        return organizer

    def get_organizer(self, organizer_id: int) -> Optional[Organizer]:
        """Returns the organizer with the given id, or None."""
        return self._organizers.get(organizer_id)

    # -- Venues ----------------------------------------------------------
    def add_venue(self, name: str, address: str, capacity: int) -> Venue:
        """Creates and stores a new venue."""
        venue = Venue(venue_id=self._next_id(), name=name, address=address, capacity=capacity)
        self._venues[venue.venue_id] = venue
        return venue

    def get_venue(self, venue_id: int) -> Optional[Venue]:
        """Returns the venue with the given id, or None."""
        return self._venues.get(venue_id)

    # -- Events ------------------------------------------------------------
    def add_event(
        self,
        title: str,
        start_time,
        organizer_id: int,
        venue_id: int,
        ticket_price: float,
        total_tickets: int,
    ) -> Event:
        """Creates a new event linked to an existing organizer and venue.

        Raises:
            KeyError: if organizer_id or venue_id cannot be found.
        """
        organizer = self._organizers[organizer_id]
        venue = self._venues[venue_id]
        event = Event(
            event_id=self._next_id(),
            title=title,
            start_time=start_time,
            organizer=organizer,
            venue=venue,
            ticket_price=ticket_price,
            total_tickets=total_tickets,
        )
        self._events[event.event_id] = event
        return event

    def get_event(self, event_id: int) -> Optional[Event]:
        """Returns the event with the given id, or None."""
        return self._events.get(event_id)

    def list_events(self) -> list[Event]:
        """Returns the list of all events."""
        return list(self._events.values())

    def delete_event(self, event_id: int) -> None:
        """Deletes the event with the given id, if it exists."""
        self._events.pop(event_id, None)

    # -- Tickets -----------------------------------------------------------
    def add_ticket(self, event_id: int, user_id: int, seat_number: str) -> Ticket:
        """Buys (creates) a new ticket for a user to attend an event.

        Raises:
            KeyError: if event_id or user_id cannot be found.
            SoldOutError: if there are no more tickets available for
                the event.
        """
        event = self._events[event_id]
        user = self._users[user_id]
        ticket = Ticket(
            ticket_id=self._next_id(),
            event=event,
            owner=user,
            seat_number=seat_number,
        )
        self._tickets[ticket.ticket_id] = ticket
        return ticket

    def get_ticket(self, ticket_id: int) -> Optional[Ticket]:
        """Returns the ticket with the given id, or None."""
        return self._tickets.get(ticket_id)

    def list_tickets(self) -> list[Ticket]:
        """Returns the list of all tickets."""
        return list(self._tickets.values())

    def delete_ticket(self, ticket_id: int) -> None:
        """Cancels and deletes the ticket with the given id."""
        ticket = self._tickets.pop(ticket_id, None)
        if ticket is not None and ticket.status.value != "cancelled":
            ticket.cancel()
