from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VenueOut")


@_attrs_define
class VenueOut:
    """
    Attributes:
        name (str):
        address (str):
        capacity (int):
        venue_id (int):
    """

    name: str
    address: str
    capacity: int
    venue_id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        address = self.address

        capacity = self.capacity

        venue_id = self.venue_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "address": address,
                "capacity": capacity,
                "venue_id": venue_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        address = d.pop("address")

        capacity = d.pop("capacity")

        venue_id = d.pop("venue_id")

        venue_out = cls(
            name=name,
            address=address,
            capacity=capacity,
            venue_id=venue_id,
        )

        venue_out.additional_properties = d
        return venue_out

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
