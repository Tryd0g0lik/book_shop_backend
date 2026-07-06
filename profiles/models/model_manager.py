# profiles/models/models_admin.py:1
from django.db import models
from django.utils.translation import gettext_lazy as _

from profiles.models.models_profiles import ProfilesModel


class ManagerProfileModel(ProfilesModel):
    user = models.OneToOneField(
        "persons.Users",
        on_delete=models.CASCADE,
        related_name="profile_manager",
    )

    class Meta:
        db_table = "profiles_manage"
        verbose_name = _("Manager profile")
        verbose_name_plural = _("Manager profiles")

    def __str__(self):
        return f"Manager: {self.user.username if len(self.user.username) > 0 else self.user.first_name}"
