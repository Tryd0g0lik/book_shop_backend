# profiles/models/models_admin.py:1
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.users.models import UserProfile

from profiles.models.models_profiles import ProfilesModel


class EditorProfileModel(ProfilesModel):
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("User"),
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "profiles_editor"
        verbose_name = _("Editor profile")
        verbose_name_plural = _("Editor profiles")

    def __str__(self):
        return f"Editor profile: {self.id}"
