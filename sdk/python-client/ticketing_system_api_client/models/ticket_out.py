from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ticket_status import TicketStatus

T = TypeVar("T", bound="TicketOut")


@_attrs_define
class TicketOut:
    """
    Attributes:
        ticket_id (int):
        event_id (int):
        user_id (int):
        seat_number (str):
        status (TicketStatus): Можливі статуси квитка протягом його життєвого циклу.
        purchase_time (datetime.datetime):
    """

    ticket_id: int
    event_id: int
    user_id: int
    seat_number: str
    status: TicketStatus
    purchase_time: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ticket_id = self.ticket_id

        event_id = self.event_id

        user_id = self.user_id

        seat_number = self.seat_number

        status = self.status.value

        purchase_time = self.purchase_time.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ticket_id": ticket_id,
                "event_id": event_id,
                "user_id": user_id,
                "seat_number": seat_number,
                "status": status,
                "purchase_time": purchase_time,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ticket_id = d.pop("ticket_id")

        event_id = d.pop("event_id")

        user_id = d.pop("user_id")

        seat_number = d.pop("seat_number")

        status = TicketStatus(d.pop("status"))

        purchase_time = datetime.datetime.fromisoformat(d.pop("purchase_time"))

        ticket_out = cls(
            ticket_id=ticket_id,
            event_id=event_id,
            user_id=user_id,
            seat_number=seat_number,
            status=status,
            purchase_time=purchase_time,
        )

        ticket_out.additional_properties = d
        return ticket_out

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
