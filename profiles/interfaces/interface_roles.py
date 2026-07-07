# profiles/interfaces/interface_role_admine.py:1
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
