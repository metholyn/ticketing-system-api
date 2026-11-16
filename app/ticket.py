"""Клас Ticket -- квиток на подію та його статуси."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from app.event import Event
from app.exceptions import InvalidTicketStatusError
from app.person import User


class TicketStatus(str, Enum):
    """Можливі статуси квитка протягом його життєвого циклу."""

    RESERVED = "reserved"
    PAID = "paid"
    CANCELLED = "cancelled"


#: Допустимі переходи між статусами квитка.
_ALLOWED_TRANSITIONS: dict[TicketStatus, set[TicketStatus]] = {
    TicketStatus.RESERVED: {TicketStatus.PAID, TicketStatus.CANCELLED},
    TicketStatus.PAID: {TicketStatus.CANCELLED},
    TicketStatus.CANCELLED: set(),
}


@dataclass
class Ticket:
    """Квиток, що зв'язує конкретного користувача з конкретною подією.

    Клас має дві залежності: від :class:`~app.event.Event` (на яку
    подію виданий квиток) та від :class:`~app.person.User`
    (кому належить квиток). При створенні квиток автоматично
    резервує місце на події та реєструється за користувачем.

    Attributes:
        ticket_id: Унікальний ідентифікатор квитка.
        event: Подія, на яку виданий квиток.
        owner: Власник квитка.
        seat_number: Номер місця (якщо застосовно).
        status: Поточний статус квитка (:class:`TicketStatus`).
        purchase_time: Час створення/бронювання квитка.
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
        """Переводить квиток у статус PAID.

        Raises:
            InvalidTicketStatusError: якщо перехід у статус PAID
                недопустимий з поточного стану.
        """
        self._transition(TicketStatus.PAID)

    def cancel(self) -> None:
        """Скасовує квиток і повертає місце в продаж на подію."""
        self._transition(TicketStatus.CANCELLED)
        self.event.release_ticket()

    def _transition(self, new_status: TicketStatus) -> None:
        """Перевіряє та виконує перехід між статусами квитка.

        Args:
            new_status: Новий бажаний статус.

        Raises:
            InvalidTicketStatusError: якщо перехід недопустимий.
        """
        if new_status not in _ALLOWED_TRANSITIONS[self.status]:
            raise InvalidTicketStatusError(
                f"Неможливо перейти з {self.status} у {new_status}"
            )
        self.status = new_status
