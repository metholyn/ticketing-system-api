"""Клас Event -- подія, на яку продаються квитки."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.exceptions import SoldOutError
from app.person import Organizer
from app.venue import Venue


@dataclass
class Event:
    """Подія (концерт, вистава, матч тощо), на яку продаються квитки.

    Клас залежить від :class:`~app.person.Organizer` (хто проводить
    подію) та :class:`~app.venue.Venue` (де вона відбувається) --
    обидва передаються в конструктор як об'єкти, а не ідентифікатори,
    що демонструє композиційну залежність між класами моделі.

    Attributes:
        event_id: Унікальний ідентифікатор події.
        title: Назва події.
        start_time: Дата та час початку події.
        organizer: Організатор події (:class:`Organizer`).
        venue: Майданчик проведення (:class:`Venue`).
        ticket_price: Базова ціна квитка.
        total_tickets: Загальна кількість квитків у продажу.
        sold_tickets: Кількість уже проданих квитків.
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
                "total_tickets не може перевищувати capacity майданчика"
            )
        self.organizer.add_event(self.event_id)

    @property
    def available_tickets(self) -> int:
        """Кількість квитків, що залишились у продажу."""
        return self.total_tickets - self.sold_tickets

    def is_sold_out(self) -> bool:
        """Перевіряє, чи розпродані всі квитки на подію."""
        return self.available_tickets <= 0

    def reserve_ticket(self) -> None:
        """Резервує один квиток, збільшуючи лічильник проданих.

        Raises:
            SoldOutError: якщо вільних квитків більше немає.
        """
        if self.is_sold_out():
            raise SoldOutError(f"Подія {self.title!r} розпродана")
        self.sold_tickets += 1

    def release_ticket(self) -> None:
        """Повертає один квиток у продаж (скасування бронювання)."""
        if self.sold_tickets > 0:
            self.sold_tickets -= 1
