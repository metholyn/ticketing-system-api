from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizerOut")


@_attrs_define
class OrganizerOut:
    """
    Attributes:
        full_name (str):
        email (str):
        person_id (int):
        organization_name (str | Unset):  Default: ''.
    """

    full_name: str
    email: str
    person_id: int
    organization_name: str | Unset = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        full_name = self.full_name

        email = self.email

        person_id = self.person_id

        organization_name = self.organization_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "full_name": full_name,
                "email": email,
                "person_id": person_id,
            }
        )
        if organization_name is not UNSET:
            field_dict["organization_name"] = organization_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        full_name = d.pop("full_name")

        email = d.pop("email")

        person_id = d.pop("person_id")

        organization_name = d.pop("organization_name", UNSET)

        organizer_out = cls(
            full_name=full_name,
            email=email,
            person_id=person_id,
            organization_name=organization_name,
        )

        organizer_out.additional_properties = d
        return organizer_out

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
