from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EventUpdate")


@_attrs_define
class EventUpdate:
    """
    Attributes:
        title (None | str | Unset):
        start_time (datetime.datetime | None | Unset):
        ticket_price (float | None | Unset):
        total_tickets (int | None | Unset):
    """

    title: None | str | Unset = UNSET
    start_time: datetime.datetime | None | Unset = UNSET
    ticket_price: float | None | Unset = UNSET
    total_tickets: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        start_time: None | str | Unset
        if isinstance(self.start_time, Unset):
            start_time = UNSET
        elif isinstance(self.start_time, datetime.datetime):
            start_time = self.start_time.isoformat()
        else:
            start_time = self.start_time

        ticket_price: float | None | Unset
        if isinstance(self.ticket_price, Unset):
            ticket_price = UNSET
        else:
            ticket_price = self.ticket_price

        total_tickets: int | None | Unset
        if isinstance(self.total_tickets, Unset):
            total_tickets = UNSET
        else:
            total_tickets = self.total_tickets

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if ticket_price is not UNSET:
            field_dict["ticket_price"] = ticket_price
        if total_tickets is not UNSET:
            field_dict["total_tickets"] = total_tickets

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_start_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_time_type_0 = datetime.datetime.fromisoformat(data)

                return start_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        start_time = _parse_start_time(d.pop("start_time", UNSET))

        def _parse_ticket_price(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        ticket_price = _parse_ticket_price(d.pop("ticket_price", UNSET))

        def _parse_total_tickets(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_tickets = _parse_total_tickets(d.pop("total_tickets", UNSET))

        event_update = cls(
            title=title,
            start_time=start_time,
            ticket_price=ticket_price,
            total_tickets=total_tickets,
        )

        event_update.additional_properties = d
        return event_update

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
