"""Базові класи учасників системи: Person, User, Organizer.

Модуль демонструє відношення наслідування: User та Organizer
успадковують спільні атрибути та поведінку від абстрактного
класу Person.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class InvalidEmailError(ValueError):
    """Помилка, що виникає при встановленні некоректної електронної пошти."""


@dataclass
class Person(ABC):
    """Абстрактний базовий клас для будь-якої фізичної особи в системі.

    Є батьківським класом для :class:`User` та :class:`Organizer` і
    інкапсулює спільні поля (ідентифікатор, ім'я, e-mail) та їх
    валідацію.

    Attributes:
        person_id: Унікальний ідентифікатор особи.
        full_name: Повне ім'я особи.
        email: Електронна пошта особи (валідується при створенні).
    """

    person_id: int
    full_name: str
    email: str

    def __post_init__(self) -> None:
        if not _EMAIL_RE.match(self.email):
            raise InvalidEmailError(f"Некоректний email: {self.email!r}")

    @abstractmethod
    def role(self) -> str:
        """Повертає роль особи в системі.

        Returns:
            Рядкове представлення ролі ("User" або "Organizer").
        """
        raise NotImplementedError

    def __str__(self) -> str:  # pragma: no cover - тривіально
        return f"{self.role()}#{self.person_id} ({self.full_name})"


@dataclass
class User(Person):
    """Користувач (глядач), який купує квитки на події.

    Успадковує :class:`Person`. Веде список ідентифікаторів квитків,
    які належать користувачу (асоціація "один до багатьох" з
    :class:`~app.ticket.Ticket`, що зберігається за ідентифікаторами,
    щоб уникнути циклічної залежності модулів).

    Attributes:
        phone: Контактний телефон користувача.
        ticket_ids: Список ідентифікаторів придбаних квитків.
    """

    phone: str = ""
    ticket_ids: list[int] = field(default_factory=list)

    def role(self) -> str:
        return "User"

    def add_ticket(self, ticket_id: int) -> None:
        """Додає ідентифікатор квитка до списку квитків користувача.

        Args:
            ticket_id: Ідентифікатор придбаного квитка.
        """
        self.ticket_ids.append(ticket_id)

    def ticket_count(self) -> int:
        """Повертає кількість квитків, якими володіє користувач."""
        return len(self.ticket_ids)


@dataclass
class Organizer(Person):
    """Організатор, який створює та проводить події.

    Успадковує :class:`Person`. Має залежність "один до багатьох" із
    класом :class:`~app.event.Event`: один організатор може проводити
    декілька подій.

    Attributes:
        organization_name: Назва організації-організатора.
        event_ids: Список ідентифікаторів подій, якими керує організатор.
    """

    organization_name: str = ""
    event_ids: list[int] = field(default_factory=list)

    def role(self) -> str:
        return "Organizer"

    def add_event(self, event_id: int) -> None:
        """Реєструє нову подію за цим організатором.

        Args:
            event_id: Ідентифікатор створеної події.
        """
        self.event_ids.append(event_id)
