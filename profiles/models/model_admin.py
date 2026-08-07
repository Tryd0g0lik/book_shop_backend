# profiles/models/models_admin.py:1
from django.db import models
from django.utils.translation import gettext_lazy as _

from profiles.models.models_profiles import ProfilesModel

# from wagtail.users import apps as wagtail_apps
# from wagtail.users.models import UserProfile as WagtailUserProfile


# WagtailUserProfile = wagtail_apps.AppConfig.get_model("wagtailusers.UserProfile")


class AdminProfileModel(ProfilesModel):
    user = models.OneToOneField(
        "wagtailusers.UserProfile",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("User"),
        # blank=True,
        # null=True,
        unique=True,
        db_comment="It is from the 'wagtail sers .models. UserProfile'",
    )

    class Meta:
        db_table = "profiles_admin"
        verbose_name = _("Admin profile")
        verbose_name_plural = _("Admin profiles")

    def __str__(self):
        return f"Admin: {self.user.user.username if len(self.user.user.username) > 0 else self.user.user.first_name}"
