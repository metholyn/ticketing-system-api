from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EventCreate")


@_attrs_define
class EventCreate:
    """
    Attributes:
        title (str):
        start_time (datetime.datetime):
        organizer_id (int):
        venue_id (int):
        ticket_price (float):
        total_tickets (int):
    """

    title: str
    start_time: datetime.datetime
    organizer_id: int
    venue_id: int
    ticket_price: float
    total_tickets: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        start_time = self.start_time.isoformat()

        organizer_id = self.organizer_id

        venue_id = self.venue_id

        ticket_price = self.ticket_price

        total_tickets = self.total_tickets

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "start_time": start_time,
                "organizer_id": organizer_id,
                "venue_id": venue_id,
                "ticket_price": ticket_price,
                "total_tickets": total_tickets,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        start_time = datetime.datetime.fromisoformat(d.pop("start_time"))

        organizer_id = d.pop("organizer_id")

        venue_id = d.pop("venue_id")

        ticket_price = d.pop("ticket_price")

        total_tickets = d.pop("total_tickets")

        event_create = cls(
            title=title,
            start_time=start_time,
            organizer_id=organizer_id,
            venue_id=venue_id,
            ticket_price=ticket_price,
            total_tickets=total_tickets,
        )

        event_create.additional_properties = d
        return event_create

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
