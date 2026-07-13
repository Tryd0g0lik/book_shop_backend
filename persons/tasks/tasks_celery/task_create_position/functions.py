# persons/tasks/tasks_celery/task_create_position/functions.py:1
# This brought the duplicate cado here from create_position_allauth.py
# Plus the function 'aget_object_of_log' is duplicate ather ways else.
import asyncio
import logging
from threading import Thread
from typing import NewType, Optional

from allauth.account.models import EmailAddress
from asgiref.sync import sync_to_async
from django.db import models
from django.db.models import Q, QuerySet
from django.http import Http404
from django.shortcuts import aget_object_or_404
from wagtail.users.models import UserProfile as WagtailUserProfile

from persons.interfaces import EmailConfirmation as AlluathEmailConfirmation
from persons.interfaces import Users
from profiles.exceptions.error_profile import ProfileValueError
from profiles.interfaces import (
    AdminProfileModel,
    ClientProfileModel,
    EditorProfileModel,
    ManagerProfileModel,
    ModeratorProfileModel,
)

log = logging.getLogger(__name__)

E = type(EmailAddress)
M = E | Users
WPM = type(WagtailUserProfile)
PM = NewType(
    "PM",
    type(
        AdminProfileModel
        | ModeratorProfileModel
        | ManagerProfileModel
        | EditorProfileModel
        | ClientProfileModel
    ),
)


async def aget_object_of_log(
    model: M, user_id: int, log_prefix: str = ""
) -> Optional[Users]:
    log_t = log_prefix + "[{}]:".format(aget_object_of_log.__name__)

    try:
        user = await aget_object_or_404(model, pk=user_id)
        return user
    except Http404:
        log.warning("{} 'user' not exists!".format(log_t))
        return None
    except Exception as e:
        log.warning(log_t + " ERROR => {}".format(e.args if e.args else str(e)))
        return None


async def aget_object_from_allauth_or_log(
    index: int, log_prefix: str = ""
) -> Optional[AlluathEmailConfirmation]:
    from allauth.account.models import EmailConfirmation

    log_t = log_prefix + "[{}]:".format(aget_object_from_allauth_or_log.__name__)
    try:
        user = await aget_object_or_404(EmailConfirmation, email_address_id=index)
        return user
    except Http404:
        log.warning("{} 'user' not exists!".format(log_t))
        return None
    except Exception as e:
        log.warning(log_t + " ERROR => {}".format(e.args if e.args else str(e)))
        return None


async def greate_of_profile(
    models: list, wagtail_profile_object: WPM, log_prefix: str = ""
) -> None:
    """
    Way directly to the person's 'Users': 'persons.models.Users => wagtail.users.models.UserProfileManagerModel =>
        profiles.models.model_<client | admin | editor | manager | client| moderator > =>
         Wagtail's UserProfile => persons.Users'
    :param models: Required. This is list of the models 'profiles.models.model_<client | admin | editor | manager | client| moderator >'
    :param wagtail_profile_object: from the 'wagtail.users.models.UserProfile' for
        the 'profiles.models.model_user_<client | admin | editor | manager | client| moderator >.UserProfileModel'
    :return: None or log massage
    """
    from django.db import IntegrityError

    from profiles.models import UserProfileManagerModel
    from utilities.services import CustomizationSyncAsyncLoop

    # fields_names = []
    log_t = "{}[{}]".format(log_prefix, greate_of_profile.__name__)
    # custom_loop = CustomizationSyncAsyncLoop(UserProfileManagerModel, fields_names, log_t)

    log.info("DEBUG 0")
    try:
        log.info("DEBUG 1")
        # fields_names: list[str] = await sync_to_async(get_fields_of_model)(UserProfileManagerModel)
        # fields_names: list[str] = await asyncio.to_thread(lambda : get_fields_of_model(UserProfileManagerModel, log_t))
        fields_names: list[str] = get_fields_of_model(UserProfileManagerModel, log_t)
        # custom_loop.get_new_function = get_fields_of_model
        # wrapper = custom_loop.get_new_loop()

        # Thread(target=wrapper).start()
        # fields_names: list[str] =  [item.name for item in UserProfileManagerModel._meta.fields]
        log.info("DEBUG 2")
        # ============================================
        # GETTING A PROFILE/ROLE OF USER
        # ============================================
        role_of_user_queryset: QuerySet[list] = await asyncio.to_thread(
            lambda: wagtail_profile_object.user.wagtail_userprofile.user.groups.values_list(
                "name", flat=True
            )
        )
        log.info("DEBUG 3")
        exists_boll = await role_of_user_queryset.aexists()
        role: str = await role_of_user_queryset.afirst() if exists_boll else ""
        log.info("DEBUG 4")
        # ============================================
        # LOCK UP THE MODEL OF USER's PROfILE
        # ============================================
        model_Of_profile_list = [
            item for item in models if role.lower() in item._meta.model_name
        ]
        log.info("DEBUG 5")
        if len(model_Of_profile_list) == 0:
            raise ProfileValueError(
                "{}: Model of a user's profile didn't find!".format(log_t)
            )
        log.info("DEBUG 6")
        model = model_Of_profile_list.pop()
        log.info("DEBUG 7")
        # ============================================
        # CHECKING ALREADY EXISTS OF RECORD TO THE WAGTAIL's MODELS OF PROFILE OR NOT
        # ============================================
        user_profile_queryset = model.objects.filter(
            Q(user__isnull=False) & Q(user=wagtail_profile_object)
        )
        log.info("DEBUG 8")
        aexists = await user_profile_queryset.aexists()
        log.info("DEBUG 9")
        # ============================================
        # GETTING A SINGLE FIELD FROM THE UserProfileManagerModel
        # This a field will be containing a working record of the models of the user's profile.
        # Every others fields (it line) will hase a 'null' value
        # ============================================
        one_filed = [
            item for item in fields_names if item.lower() in model._meta.model_name
        ]
        log.info("DEBUG 10")
        # ============================================
        # CREATING A RECORD DIRECTLY IN THE UserProfileManagerModel MODEL
        # ============================================
        if not aexists:
            log.info("DEBUG 11")

            user_profile = await model.objects.acreate(user=wagtail_profile_object)
            log.info("DEBUG 12")

            await UserProfileManagerModel.objects.acreate(
                **{one_filed[0]: user_profile}
            )
            log.info("DEBUG 13")
        else:
            log.info("DEBUG 14")
            user_profile_first = await user_profile_queryset.afirst()
            await UserProfileManagerModel.objects.acreate(
                **{one_filed[0]: user_profile_first}
            )
            log.info("DEBUG 15")
    except IntegrityError as e:
        if hasattr(e, "code") and e.code == "unique_review":
            log.warning(
                "{}[{}]: Warning => {}".format(
                    log_prefix,
                    greate_of_profile.__name__,
                    e.args[0] if e.args else str(e),
                )
            )
            return None

    except Exception as e:
        raise ProfileValueError(
            "{}[{}]: 'ERROR => {}".format(
                log_prefix, greate_of_profile.__name__, e.args[0] if e.args else str(e)
            )
        ) from e


def get_fields_of_model(
    model: PM,
    prefix_log: str = "",
) -> list[str]:
    try:
        fields_names = [item.name for item in model._meta.fields]
        return fields_names
    except Exception as e:
        log_t = "{}[{}]: ProfileValueError => {}".format(
            prefix_log, greate_of_profile.__name__, str(e.args[0]) if e.args else str(e)
        )
        raise ProfileValueError(log_t) from e
