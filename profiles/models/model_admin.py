# profiles/models/models_admin.py:1
from django.db import models

from persons.models import Users

# from profiles.models.models_profiles import ProfilesModels

#
# class AdminProfileModels(ProfilesModels):
#     dashboard_preference = models.JSONField(
#         default=dict,
#         blank=True,
#         description="User preferences for dashboards and layout"
#     )
#     user = models.OneToOneField(Users,
#                                 on_delete=models.CASCADE,
#                                 related_name="admin_profile",
#                                 )
#     class Meta:
#         db_table = "admin_profiles"
#         verbose_name = "Admin Profile"
#         verbose_name_plural = "Admin Profiles"
#
#     def __str__(self):
#         return f"Admin: {self.user.username if len(self.user.username) > 0 else self.user.first_name  }"
