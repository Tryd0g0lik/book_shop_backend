# profiles/models/models_admin.py:1
from django.db import models
from django.utils.translation import gettext_lazy as _

from profiles.models.models_profiles import ProfilesModel


class EditorProfileModel(ProfilesModel):
    user = models.OneToOneField(
        "persons.Users",
        on_delete=models.CASCADE,
        related_name="profile_editor",
    )

    class Meta:
        db_table = "profiles_editor"
        verbose_name = _("Editor profile")
        verbose_name_plural = _("Editor profiles")

    def __str__(self):
        return f"Editor: {self.user.username if len(self.user.username) > 0 else self.user.first_name}"
