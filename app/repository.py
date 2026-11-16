"""In-memory репозиторії для зберігання сутностей моделі.

Клас :class:`TicketingRepository` агрегує всі інші класи моделі
(Person, Venue, Event, Ticket) і надає єдину точку доступу для
прикладного рівня (CLI або REST API).
"""

from __future__ import annotations

from itertools import count
from typing import Optional

from app.event import Event
from app.person import Organizer, User
from app.ticket import Ticket
from app.venue import Venue


class TicketingRepository:
    """Агрегує та зберігає всі сутності системи продажу квитків.

    Це найвищий рівень композиції в моделі: репозиторій володіє
    колекціями організаторів, користувачів, майданчиків, подій та
    квитків і відповідає за генерацію нових ідентифікаторів.
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
        """Створює та зберігає нового користувача."""
        user = User(person_id=self._next_id(), full_name=full_name, email=email, phone=phone)
        self._users[user.person_id] = user
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        """Повертає користувача за ідентифікатором або None."""
        return self._users.get(user_id)

    def list_users(self) -> list[User]:
        """Повертає список усіх користувачів."""
        return list(self._users.values())

    # -- Organizers ------------------------------------------------------
    def add_organizer(self, full_name: str, email: str, organization_name: str = "") -> Organizer:
        """Створює та зберігає нового організатора."""
        organizer = Organizer(
            person_id=self._next_id(),
            full_name=full_name,
            email=email,
            organization_name=organization_name,
        )
        self._organizers[organizer.person_id] = organizer
        return organizer

    def get_organizer(self, organizer_id: int) -> Optional[Organizer]:
        """Повертає організатора за ідентифікатором або None."""
        return self._organizers.get(organizer_id)

    # -- Venues ----------------------------------------------------------
    def add_venue(self, name: str, address: str, capacity: int) -> Venue:
        """Створює та зберігає новий майданчик."""
        venue = Venue(venue_id=self._next_id(), name=name, address=address, capacity=capacity)
        self._venues[venue.venue_id] = venue
        return venue

    def get_venue(self, venue_id: int) -> Optional[Venue]:
        """Повертає майданчик за ідентифікатором або None."""
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
        """Створює нову подію, пов'язану з існуючим організатором і майданчиком.

        Raises:
            KeyError: якщо organizer_id або venue_id не знайдені.
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
        """Повертає подію за ідентифікатором або None."""
        return self._events.get(event_id)

    def list_events(self) -> list[Event]:
        """Повертає список усіх подій."""
        return list(self._events.values())

    def delete_event(self, event_id: int) -> None:
        """Видаляє подію за ідентифікатором, якщо вона існує."""
        self._events.pop(event_id, None)

    # -- Tickets -----------------------------------------------------------
    def add_ticket(self, event_id: int, user_id: int, seat_number: str) -> Ticket:
        """Купує (створює) новий квиток для користувача на подію.

        Raises:
            KeyError: якщо event_id або user_id не знайдені.
            SoldOutError: якщо на подію більше немає вільних квитків.
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
        """Повертає квиток за ідентифікатором або None."""
        return self._tickets.get(ticket_id)

    def list_tickets(self) -> list[Ticket]:
        """Повертає список усіх квитків."""
        return list(self._tickets.values())

    def delete_ticket(self, ticket_id: int) -> None:
        """Скасовує та видаляє квиток за ідентифікатором."""
        ticket = self._tickets.pop(ticket_id, None)
        if ticket is not None and ticket.status.value != "cancelled":
            ticket.cancel()
