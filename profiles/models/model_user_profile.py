# profiles/models/model_user_profile.py:1
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.users.models import UserProfile as WagtailUserProfile

from profiles.exceptions.error_profile import ProfileNotFound, ProfileValueError


class UserProfile(WagtailUserProfile):
    """
    Params that inherited from the 'wagtail.users.models.UserProfile'
    :param int id.
    :param bool submitted_notifications
    :param bool approved_notifications
    :param bool rejected_notifications
    :param int user_id
    :param str preferred_language
    :param str current_time_zone
    :param str avatar
    :param bool updated_comments_notifications
    :param str dismissibles
    :param str theme
    :param str density
    :param str contrast
    :param bool keyboard_shortcuts
    And added additional cell is profiles
    """

    moderator = models.ForeignKey(
        "profiles.ModeratorProfileModel",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name="profile_moderator",
        related_query_name="profile_moderator",
        verbose_name=_("Moderator"),
    )
    manager = models.ForeignKey(
        "profiles.ManagerProfileModel",
        on_delete=models.CASCADE,
        related_name="profile_manager",
        related_query_name="profile",
        verbose_name=_("Manager"),
        null=True,
        blank=True,
        db_index=True,
    )
    editor = models.ForeignKey(
        "profiles.EditorProfileModel",
        on_delete=models.CASCADE,
        related_name="profiles_editor",
        related_query_name="profile",
        verbose_name=_("Editor"),
        null=True,
        blank=True,
        db_index=True,
    )
    admin = models.ForeignKey(
        "profiles.AdminProfileModel",
        on_delete=models.CASCADE,
        related_name="profiles_admin",
        related_query_name="profile",
        null=True,
        blank=True,
        verbose_name=_("Admin"),
        db_index=True,
    )
    client = models.ForeignKey(
        "profiles.ClientProfileModel",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Client"),
        related_query_name="profiles_client",
        related_name="profiles",
        db_index=True,
        db_comment="User profile",
    )

    class Meta:
        db_table = "profiles_users"
        verbose_name_plural = _("User profiles")
        verbose_name = _("User profiles")

    def __str__(self):
        list_profiles = [
            self.client,
            self.admin,
            self.editor,
            self.manager,
            self.moderator,
        ]
        list_profiles = [item for item in list_profiles if item is not None]
        return f"{self.user.username} Profile {list_profiles[0] if len(list_profiles) == 1 else ''}"

    def clean_profile_name(self):
        list_profiles = [
            self.client,
            self.admin,
            self.editor,
            self.manager,
            self.moderator,
        ]
        list_profiles = [item for item in list_profiles if item is not None]
        if len(list_profiles) != 1:
            raise ProfileValueError()

        if len(list_profiles) == 0:
            raise ProfileNotFound()
