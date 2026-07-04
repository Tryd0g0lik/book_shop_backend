# profiles/models/model_moderator.py:1
from django.db import models
from django.utils.translation import gettext_lazy as _

from profiles.models.models_profiles import ProfilesModel


class ModeratorProfileModel(ProfilesModel):
    user = models.OneToOneField(
        "persons.Users",
        on_delete=models.CASCADE,
        related_name="profile_moderator",
    )

    class Meta:
        db_table = "profiles_moderator"
        verbose_name = _("Moderator profile")
        verbose_name_plural = _("Moderator's profiles")

    def __str__(self):
        return f"Moderator: {self.user.username if len(self.user.username) > 0 else self.user.first_name}"
