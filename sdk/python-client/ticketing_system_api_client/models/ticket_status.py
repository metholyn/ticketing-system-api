from enum import StrEnum


class TicketStatus(StrEnum):
    CANCELLED = "cancelled"
    PAID = "paid"
    RESERVED = "reserved"

    def __str__(self) -> str:
        return str(self.value)
