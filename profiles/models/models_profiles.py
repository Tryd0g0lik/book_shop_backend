# profiles/models/models_profiles.py:1
# Simply contain a common information of all roles/profiles

from django.db import models

from project.settings_conf.settings_first import (
    LANGUAGE_CODE,
    TIME_ZONE,
    WAGTAIL_CONTENT_LANGUAGES,
)


class ProfilesModel(models.Model):

    # Settings
    language = models.CharField(
        max_length=10, choices=WAGTAIL_CONTENT_LANGUAGES, default=LANGUAGE_CODE
    )
    time_zone = models.CharField(max_length=50, default=TIME_ZONE)
    dashboard_preference = models.JSONField(
        default=dict, blank=True, help_text="User preferences for dashboards and layout"
    )

    class Meta:
        abstract = True
