# profiles/interfaces/interface_role_admine.py:1
from typing import Optional

from dulwich.protocol import Protocol


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


class UserProfile(Basis):
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
