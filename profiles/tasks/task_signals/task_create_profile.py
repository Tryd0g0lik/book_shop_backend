# profiles/tasks/task_signals/task_create_profile.py:1
import logging

from django.dispatch import Signal, receiver

create_profile_signal = Signal()
log = logging.getLogger(__name__)


@receiver(create_profile_signal)
def task_create_profile_from_signal(*args, **kwargs) -> None:
    # from wagtail.users import apps as wagtail_users_apps
    from wagtail.users.models import UserProfile

    # UserProfile = wagtail_users_apps.AppConfig.get_model("wagtailusers.UserProfile")
    from profiles.models import (
        AdminProfileModel,
        ClientProfileModel,
        EditorProfileModel,
        ManagerProfileModel,
        ModeratorProfileModel,
        UserProfileManagerModel,
    )

    log_t = f"[{task_create_profile_from_signal.__name__}]:"
    profile_mapping = {
        "moderator": ModeratorProfileModel,
        "client": ClientProfileModel,
        "manager": ManagerProfileModel,
        "editor": EditorProfileModel,
        "user": UserProfileManagerModel,
        "admin": AdminProfileModel,
    }

    user_id = kwargs.get("user_id")

    if not user_id:
        log.error(
            log_t + " ERROR => "
            f"user_id not provided! args: {str(args)} & kwargs: {str(kwargs)}"
        )
        return None
    try:

        user = UserProfile.objects.get(user_id=user_id)
        group_names_queryset = user.user.wagtail_userprofile.user.groups.values_list(
            "name", flat=True
        )
        group_names = (
            [group_names_queryset.first()] if group_names_queryset.exists() else []
        )
        for group_name in group_names:
            profile_class = profile_mapping.get(group_name.lower())
            if not profile_class:
                log.error(
                    log_t + " ERROR => "
                    f"User's role have not found! args: {str(args)} & kwargs: {str(kwargs)}, \
                                  group_names: {group_names} \
                                  group_name: {str(group_name)} & profile_class: {str(profile_class)}"
                )
                return None
            profile_class.objects.get_or_create(user=user)
            log.info(log_t + f" Created {profile_class.__name__} for user {user_id}")
            break

        return None
    except UserProfile.DoesNotExist:
        log.error(log_t + " User's profile has not found at the Wagtail's profile!")
        return None
    except Exception as e:
        log.error(log_t + " ERROR => " + list(e.args)[0] if len(e.args) else str(e))
        return None


create_profile_signal.connect(task_create_profile_from_signal)
