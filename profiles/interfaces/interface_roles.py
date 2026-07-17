# profiles/interfaces/interface_roles.py:1
from typing import Optional

from dulwich.protocol import Protocol
from pydantic import BaseModel


class Basis(Protocol):
    pass


class ClientProfileModel(Basis):
    # Settings
    language: str
    time_zone: str
    dashboard_preference: dict
    user: int

    def __str__(self) -> str: ...


class AdminProfileModel(ClientProfileModel):
    def __str__(self) -> str: ...


class ModeratorProfileModel(ClientProfileModel):
    def __str__(self) -> str: ...


class ManagerProfileModel(ClientProfileModel):
    def __str__(self) -> str: ...


class EditorProfileModel(ClientProfileModel):
    def __str__(self) -> str: ...


class UserProfileType(Basis):
    user: int
    submitted_notifications: bool
    approved_notifications: bool
    rejected_notifications: bool
    updated_comments_notifications: bool
    preferred_language: str
    current_time_zone: str
    avatar: str
    dismissibles: dict
    moderator: Optional[ModeratorProfileModel]
    manager: Optional[ManagerProfileModel]
    editor: Optional[EditorProfileModel]
    admin: Optional[AdminProfileModel]
    client: Optional[ClientProfileModel]

    def __str__(self) -> str: ...

    def clean_profile_name(self) -> None: ...


class UserProfilePydantic(BaseModel):
    id: Optional[int]
    moderator: Optional[int]
    manager: Optional[int]
    editor: Optional[int]
    admin: Optional[int]
    client: Optional[int]

    def to_dict_from_model(self) -> dict:
        """All data/field from a model"""
        data_dict: dict = self.model_dump()
        return data_dict
