from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserOut")


@_attrs_define
class UserOut:
    """
    Attributes:
        full_name (str):
        email (str):
        person_id (int):
        phone (str | Unset):  Default: ''.
        ticket_count (int | Unset):  Default: 0.
    """

    full_name: str
    email: str
    person_id: int
    phone: str | Unset = ""
    ticket_count: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        full_name = self.full_name

        email = self.email

        person_id = self.person_id

        phone = self.phone

        ticket_count = self.ticket_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "full_name": full_name,
                "email": email,
                "person_id": person_id,
            }
        )
        if phone is not UNSET:
            field_dict["phone"] = phone
        if ticket_count is not UNSET:
            field_dict["ticket_count"] = ticket_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        full_name = d.pop("full_name")

        email = d.pop("email")

        person_id = d.pop("person_id")

        phone = d.pop("phone", UNSET)

        ticket_count = d.pop("ticket_count", UNSET)

        user_out = cls(
            full_name=full_name,
            email=email,
            person_id=person_id,
            phone=phone,
            ticket_count=ticket_count,
        )

        user_out.additional_properties = d
        return user_out

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
