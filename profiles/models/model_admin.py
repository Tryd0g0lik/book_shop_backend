# profiles/models/models_admin.py:1
from django.db import models
from django.utils.translation import gettext_lazy as _

from profiles.models.models_profiles import ProfilesModel


class AdminProfileModel(ProfilesModel):
    user = models.OneToOneField(
        "persons.Users",
        on_delete=models.CASCADE,
        related_name="profile_admin",
    )

    class Meta:
        db_table = "profiles_admin"
        verbose_name = _("Admin profile")
        verbose_name_plural = _("Admin profiles")

    def __str__(self):
        return f"Admin: {self.user.username if len(self.user.username) > 0 else self.user.first_name}"
