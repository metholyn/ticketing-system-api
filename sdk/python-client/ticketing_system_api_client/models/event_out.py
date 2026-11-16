from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EventOut")


@_attrs_define
class EventOut:
    """
    Attributes:
        event_id (int):
        title (str):
        start_time (datetime.datetime):
        organizer_id (int):
        venue_id (int):
        ticket_price (float):
        total_tickets (int):
        sold_tickets (int):
        available_tickets (int):
    """

    event_id: int
    title: str
    start_time: datetime.datetime
    organizer_id: int
    venue_id: int
    ticket_price: float
    total_tickets: int
    sold_tickets: int
    available_tickets: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        event_id = self.event_id

        title = self.title

        start_time = self.start_time.isoformat()

        organizer_id = self.organizer_id

        venue_id = self.venue_id

        ticket_price = self.ticket_price

        total_tickets = self.total_tickets

        sold_tickets = self.sold_tickets

        available_tickets = self.available_tickets

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event_id": event_id,
                "title": title,
                "start_time": start_time,
                "organizer_id": organizer_id,
                "venue_id": venue_id,
                "ticket_price": ticket_price,
                "total_tickets": total_tickets,
                "sold_tickets": sold_tickets,
                "available_tickets": available_tickets,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        event_id = d.pop("event_id")

        title = d.pop("title")

        start_time = datetime.datetime.fromisoformat(d.pop("start_time"))

        organizer_id = d.pop("organizer_id")

        venue_id = d.pop("venue_id")

        ticket_price = d.pop("ticket_price")

        total_tickets = d.pop("total_tickets")

        sold_tickets = d.pop("sold_tickets")

        available_tickets = d.pop("available_tickets")

        event_out = cls(
            event_id=event_id,
            title=title,
            start_time=start_time,
            organizer_id=organizer_id,
            venue_id=venue_id,
            ticket_price=ticket_price,
            total_tickets=total_tickets,
            sold_tickets=sold_tickets,
            available_tickets=available_tickets,
        )

        event_out.additional_properties = d
        return event_out

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
