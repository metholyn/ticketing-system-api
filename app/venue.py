"""Клас Venue -- майданчик, на якому проводяться події."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Venue:
    """Фізичний або віртуальний майданчик для проведення подій.

    Клас :class:`~app.event.Event` має залежність (композицію) від
    цього класу: кожна подія проводиться на певному майданчику.

    Attributes:
        venue_id: Унікальний ідентифікатор майданчика.
        name: Назва майданчика.
        address: Адреса майданчика.
        capacity: Максимальна місткість (кількість глядачів).
    """

    venue_id: int
    name: str
    address: str
    capacity: int

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ValueError("capacity має бути додатним числом")
