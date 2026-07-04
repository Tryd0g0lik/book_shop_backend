# profiles/models/model_client.py:1
from django.db import models
from django.utils.translation import gettext_lazy as _

from profiles.models.models_profiles import ProfilesModel


class ClientProfileModel(ProfilesModel):
    user = models.OneToOneField(
        "persons.Users",
        on_delete=models.CASCADE,
        related_name="profile_client",
    )

    class Meta:
        db_table = "profiles_Client"
        verbose_name = _("Client profile")
        verbose_name_plural = _("Client's profiles")

    def __str__(self):
        return f"Client: {self.user.username if len(self.user.username) > 0 else self.user.first_name}"
