# profiles/models/model_client.py:1
from django.db import models
from django.utils.translation import gettext_lazy as _

from profiles.models.models_profiles import ProfilesModel


class ClientProfileModel(ProfilesModel):
    user = models.OneToOneField(
        "wagtailusers.UserProfile",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("User"),
        unique=True,
        db_comment="It is from the 'wagtail. users .models .UserProfile'",
    )

    class Meta:
        db_table = "profiles_client"
        verbose_name = _("Client profile")
        verbose_name_plural = _("Client's profiles")

    def __str__(self):
        return "Client profile: {}".format(
            self.user.user.username
            if len(self.user.user.username) > 0
            else self.user.user.first_name
        )
