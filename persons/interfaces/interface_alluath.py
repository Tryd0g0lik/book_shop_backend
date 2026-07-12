# persons/interfaces/interface_alluath.py:1
from datetime import datetime
from typing import Protocol

from allauth.account.managers import EmailAddressManager, EmailConfirmationManager
from allauth.account.models import (
    EmailConfirmation,
    EmailConfirmationHMAC,
    EmailConfirmationMixin,
)
from django.db import models
from django.http import HttpRequest

from persons.interfaces import Users


class EmailAddress(models.Model):
    user: Users
    email: str
    verified: bool
    primary: bool

    objects: EmailAddressManager

    def __str__(self) -> str: ...

    def clean(self) -> None: ...

    def can_set_verified(self) -> bool: ...

    def set_verified(self, commit: bool = True) -> bool: ...

    def set_as_primary(self, conditional: bool = False) -> bool: ...

    def send_confirmation(
        self, request: HttpRequest | None = None, signup: bool = False
    ) -> EmailConfirmation | EmailConfirmationHMAC: ...

    def remove(self) -> None: ...


class EmailConfirmation(EmailConfirmationMixin, models.Model, Protocol):
    email_address: EmailAddress
    created: datetime
    sent: datetime
    key: str

    objects: EmailConfirmationManager

    def __str__(self) -> str: ...

    @classmethod
    def create(cls, email_address: EmailAddress): ...

    @classmethod
    def from_key(cls, key: str): ...

    def key_expired(self) -> bool: ...

    key_expired.boolean = True  # type: ignore[attr-defined]

    def confirm(self, request: HttpRequest) -> EmailAddress | None: ...

    def send(
        self, request: HttpRequest | None = None, signup: bool = False
    ) -> None: ...
