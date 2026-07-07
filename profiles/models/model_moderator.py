# profiles/models/model_moderator.py:1
from django.db import models
from django.utils.translation import gettext_lazy as _

from profiles.models.models_profiles import ProfilesModel


class ModeratorProfileModel(ProfilesModel):

    class Meta:
        db_table = "profiles_moderator"
        verbose_name = _("Moderator profile")
        verbose_name_plural = _("Moderator's profiles")

    def __str__(self):
        return f"Moderator profile: {self.id}"
