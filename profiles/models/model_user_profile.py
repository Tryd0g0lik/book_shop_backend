# profiles/models/model_user_profile.py:1
import logging

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from profiles.exceptions.error_profile import ProfileNotFound, ProfileValueError
from profiles.interfaces import UserProfilePydantic

log = logging.getLogger(__name__)


# Was renamed from UserProfileModel to
class UserProfileManagerModel(models.Model):
    """

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

    # id = models.AutoField(primary_key=True)
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
    # product = models.ForeignKey(
    #     "catalog.ProductModel",
    #     on_delete=models.SET_NULL,
    #     verbose_name=_("Product"),
    #     blank=True,
    #     null=True,
    #     related_name="product",
    # )

    class Meta:
        db_table = "profiles_users"
        verbose_name_plural = _("User profiles")
        verbose_name = _("User profiles")
        constraints = [
            models.UniqueConstraint(
                fields=["moderator", "manager", "editor", "admin", "client"],
                name="unique_of_profile_manager",
                violation_error_code="unique_review",
                violation_error_message="Combination of users profiles already exists.",
            )
        ]

    def __str__(self):
        list_profiles = [
            self.client,
            self.admin,
            self.editor,
            self.manager,
            self.moderator,
        ]
        list_profiles = [item for item in list_profiles if item is not None]
        return f"Id: {self.id} Profile {list_profiles[0] if len(list_profiles) == 1 else ''}"

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

    def get_profile_by_user_id(self, user_id, fields_exclude=["id"]) -> Q | None:
        """
        Here we create Q - script for request to the all db. It is from single request receive of user by 'user_id'
        next We get a UserProfileManagerModel's line and from that line we get of user.
        Example:```text
        profile_manager = UserProfileManagerModel()
        fields_exclude = ["id", "client"]
        q_objects = profile_manager.get_profile_by_user_id(
                    user_id, fields_exclude
                )
        if q_objects is not None:
            # --- All fields/column
            manager: Users | None = (
                await profile_manager.__class__.objects.filter(
                    q_objects
                ).afirst()
            )
            if manager is not None:
                fields_names_list = [
                    item.name for item in manager.__class__._meta.fields
                ]
                q_objects = Q()
                # --- One field/column
                for item in fields_names_list:
                    if item in fields_exclude:
                        continue
                    q_objects |= Q(
                        **{f"{item}__isnull": False},
                        **{f"{item}__user__user_id": user_id},
                    )

                product.created_by = await manager.__class__.objects.aget(
                    q_objects
                )
        ```
        :param int user_id: User id it that us need to find/
        :return: Q | None
        """

        log_t = "[{}][{}]".format(
            UserProfileManagerModel.__class__.__name__,
            self.get_profile_by_user_id.__name__,
        )
        from persons.tasks.tasks_celery.task_create_position.functions import (
            get_fields_of_model,
        )

        fields_names = get_fields_of_model(self.__class__)
        q_objects = Q()
        try:
            for item in fields_names:
                if item in fields_exclude:
                    continue
                q_objects |= Q(
                    **{f"{item}__isnull": False}, **{f"{item}__user__user_id": user_id}
                )
            return q_objects
        except Exception as e:
            log.warning(
                "{} Error => {}".format(
                    log_t, list(e.args)[0] if len(e.args) > 0 else str(e)
                )
            )
            return None
