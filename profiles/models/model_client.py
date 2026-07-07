# profiles/models/model_client.py:1
from django.db import models
from django.utils.translation import gettext_lazy as _

from profiles.models.models_profiles import ProfilesModel


class ClientProfileModel(ProfilesModel):

    class Meta:
        db_table = "profiles_client"
        verbose_name = _("Client profile")
        verbose_name_plural = _("Client's profiles")

    def __str__(self):
        return f"Client profile: {self.id}"
