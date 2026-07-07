# profiles/models/models_admin.py:1
from django.db import models
from django.utils.translation import gettext_lazy as _

from profiles.models.models_profiles import ProfilesModel


class ManagerProfileModel(ProfilesModel):

    class Meta:
        db_table = "profiles_manage"
        verbose_name = _("Manager profile")
        verbose_name_plural = _("Manager profiles")

    def __str__(self):
        return f"Manager profile: {self.id}"
