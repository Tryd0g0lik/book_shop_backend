# profiles/models/models_admin.py:1
from django.db import models

from profiles.models.models_profiles import ProfilesModel

# from persons.models import Users


class AdminProfileModel(ProfilesModel):
    user = models.OneToOneField(
        "persons.Users",
        on_delete=models.CASCADE,
        related_name="profile_admin",
    )

    class Meta:
        db_table = "profiles_admin"
        verbose_name = "Admin profile"
        verbose_name_plural = "Admin Profiles"

    def __str__(self):
        return f"Admin: {self.user.username if len(self.user.username) > 0 else self.user.first_name}"
