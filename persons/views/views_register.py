"""
persons/views/views_register.py:1
"""

import asyncio
import datetime
import json
import logging
import re
from typing import Optional

from allauth.account.views import SignupView as AllauthSignupView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.http import require_GET, require_POST
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from persons import EnumTemplatesKeysCache
from persons.apps import account_manager, cachemanager
from persons.forms import UsersRegistrationForm
from persons.forms.users_registration_form import UsersCheckCodeVerificationForm
from persons.tasks.tasks_celery.task_send_letter_to_user_email import task_postman
from project.settings_conf.settings_env import CATEGORY_STATUS

log = logging.getLogger(__name__)
path_names: list[str] = [
    "/register/admin/",
    "/register/moderator/",
    "/register/manager/",
]


class UsersRegistrationView(AllauthSignupView):
    """
    TODO: Тут имеем авторизованого пользоватяля. Без прав админа он рендерится на главную
            Разрулить урлы, чтою присволить роли
            Отправить код аутендификации и авторизации.
    """

    template_name = "auth/register.html"
    form_class = UsersRegistrationForm
    success_url = "register/admin/"

    def __init__(
        self,
        **kwargs,
    ):
        """
        THis is the view class of the user registration.
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.log_t = "[%s]:" % UsersRegistrationView.__class__.__name__

    @method_decorator(require_GET)
    def get(
        self,
        request,
        *args,
        **kwargs,
    ):
        """
        It for open the page of registrate .
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = request.user
        is_open: bool = self.is_open()

        if not user.is_anonymous or user.id is not None or not is_open:
            log_t = _("User on that email already exists.")
            log.warning(log_t)
            raise ValueError(log_t)

        try:
            context = {}
            if request.path in path_names:
                form = self.get_form()
                context.update(
                    {
                        "form": form,
                        "category_choices": CATEGORY_STATUS,
                        "validation_sent": False,  # Code validation hase not been to send.
                    }
                )
                super().get(request, *args, **kwargs)
                return render(request, "auth/register.html", context, status=200)
            elif request.path not in path_names and "register" in request.path:
                form = UsersCheckCodeVerificationForm()
                context.update({"validation_sent": True, "form": form})

            return render(request, "auth/register.html", context, status=200)

        except Exception as e:

            ERROR_TEXT = " ".join(
                [
                    self.log_t[-1] + f"{self.get.__name__}:",
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    (
                        " Server error to the user registration GET. ERROR_TEXT: %s"
                        % e.args[0]
                        if e.args
                        else str(e)
                    ),
                ]
            )
            log.error(ERROR_TEXT)
            return HttpResponseRedirect("/login", {"detail": ERROR_TEXT})
        finally:
            pass

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        """
        TODO: В зависимости от того какой pathname в result_list - присваеваем роль.
        :param request:
            - request.HEADER Referer: Required. "http://127.0.0.1:8000/register/admin/"
            - required.< FORM DATA>
            -- email: Required. This is the email of user. Required of var. Unique. User can  not  change.
            -- first_name: This is the first name of user.
            -- username: It is a login or username of user.  If user did not provided his the first name, mean we
                will resieve  from him email address provided.
                Exemple: ''sergey_24@mail.ru'  -> 'sergey_24'.
            -- password1: Required, Password of user
            -- password2: Required. Password of user too. That is for the checks
            -- csrfmiddlewaretoken: Required, This is CSRF-token. He provided of automatic.
            -- check_user: Required. Data can been send only  if user tell us that 'YES, I agree' Example: 'on'
            -- category:  Required. This is the basis name from the all categories. Next we will
                be changing  when  user tell us-  that "YES, it is my the email address".
                He should be showing  us - code of latter.

        It for open the page of registrate and the registration's POST method.
        :return Status code
            302: Means - Registration successful! Chek your email,
            400: Means - Something what wrong
            500: Means - Server error under user registration
        """
        # form = self.form_class(request.POST)
        pathname = request.path
        user = request.user
        url_parent = request.headers.get("Referer")
        if request.user.is_authenticated or (
            user.is_active and not user.is_anonymous and not user.is_superuser
        ):
            log_t = (
                self.log_t[:-1]
                + f"[{self.post.__name__}]: "
                + _("User on that email already exists.")
            )
            log.warning(log_t + "Authenticated user tried to register")
            # return redirect("/")
            return HttpResponseRedirect(reverse("/"), status=400)
        # ---- END TEST BLOCK
        messages.success(request, _("Registration successful! Chek your email."))
        try:
            log.info(
                """\n
            # ============================================
            # POST'S DATA BEFORE REGISTRATION
            # ============================================
            """
            )
            result_list = [item for item in path_names if item in url_parent]

            if len(result_list) > 0:
                log_t = (
                    self.log_t[:-1]
                    + f"[{self.post.__name__}]: "
                    + "User data These are before records in database."
                )
                log.info(log_t)
                super().post(request, *args, **kwargs)
                # return render(request, "auth/register.html", status=201)
                return HttpResponseRedirect(reverse("register/"), status=302)
            elif len(result_list) == 0 and re.search(r"register/$", url_parent):
                log_t = (
                    self.log_t[:-1]
                    + f"[{self.post.__name__}]: "
                    + "User data before checks the code verification."
                )
                log.info(log_t)
                # Check of code verification
            return HttpResponseRedirect(
                reverse(
                    "management",
                    kwargs={
                        "details": """Something what wrong with the var.'category.\n
    It is form of registration by the url %s"""
                        % (pathname,)
                    },
                ),
                status=400,
            )
        except Exception as e:
            ERROR_TEXT = " ".join(
                [
                    self.log_t[-1] + f"{self.post.__name__}:",
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    " Server error under user registration. URL: %s TEXT_ERROR: %s"
                    % (pathname, e.args[0] if e.args else str(e)),
                ]
            )
            log.error(ERROR_TEXT)
            return render(
                request,
                "auth/register.html",
                status=500,
            )
        finally:
            pass

    def form_valid(self, form):
        from persons.tasks.tasks_celery.task_set_cache import (
            task_of_cache,
        )

        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")

        super().form_valid(form)

        if (username is None) or (
            username is not None and isinstance(username, str) and len(username) < 2
        ):
            setattr(form, "username", email.split("@")[0])
            username = form.cleaned_data.get("username")
        args = (EnumTemplatesKeysCache.USER_PENDING.value % re.sub(r"[@.]", "", email),)
        # args = (email,)
        # ------------------------------------
        kwargs = {"username": username, "email": email}
        try:
            # CELERY + REDIS
            task_of_cache.delay(*args, **kwargs)
            message = _("Registration is almost complete! Check your email.")
        except Exception as e:
            log_t = f"[UsersRegistrationView]: {e.args[0] if e.args else str(e)}"
            raise ValueError(log_t)
        finally:
            task_postman.delay(*args, **kwargs)
        messages.success(self.request, message)

        return


class UsersVerificationDuringRegistration(View):
    form_class = UsersCheckCodeVerificationForm
    success_url = "/register/"
    template_name = "auth/register.html"
    # async def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    async def post(self, request, *args, **kwargs):
        """
        TODO: Time-live of the verification code must be re-writen
        Receive the verification code/toke. This code/token tell obout email address of user/person. It is correctly.
        Here we have a connection with: cache server (get bytes data) and main server when we get a user data and update it.
        To the entrypoint we receive the 'key'. then look up in the cache data. If we find exactly the current token in cache
            it means - all OK or not all successfully!
        :param request: Transmits only one element. It is 'key', Example: DLKK-XTDH
        :param args:
        :param kwargs:
        :return: JSON data if all successfully and 201 status code or 302, 400, 500 status code
            "302": description="All Successfully verified. Revers to the login page.",
            "500": description="Server vahe error. Open page for registration."
            "400": description="Bad request. Please check your status. User should be not 'is_authenticated' "
        """
        form = UsersCheckCodeVerificationForm()
        context = {"validation_sent": True, "form": form}
        user = request.user
        if request.method == "POST" and not user.is_authenticated:
            token_key = request.POST.get("key")
            keys = EnumTemplatesKeysCache.USER_PENDING_LETTER.value % "*"
            collection_ = []
            await cachemanager.aget(key_pattern=keys, collection=collection_)

            if len(collection_) > 0:
                for key in collection_:
                    collection_.clear()
                    await cachemanager.aget(key=key.decode(), collection=collection_)
            if len(collection_) > 0:
                for item in collection_:
                    try:
                        user_cache_json = json.loads(item.decode())
                        if user_cache_json["verification_code"] == token_key:
                            collection_.clear()
                            database_service = account_manager.postman.database_service
                            result: Optional[dict] = await asyncio.to_thread(
                                lambda: database_service.update_in_database(
                                    {
                                        "category": "CLIENT",
                                        "password": "pbkdf2_sha256$hash_admin_1",
                                        "is_verified": True,
                                        "verification_code": token_key,
                                        "is_superuser": False,
                                        "updated_at": datetime.datetime.now(),
                                    },
                                    user_email=user_cache_json["email"],
                                )
                            )

                            if result is not None:
                                log.info("Verification code updated successfully")
                                return await asyncio.to_thread(
                                    lambda: HttpResponseRedirect(
                                        reverse(
                                            "account_login",
                                        ),
                                        status=302,
                                    )
                                )
                    except Exception as e:
                        log.error(e)
                        context["details"] = e.args[0] if e.args else str(e)
                        return await asyncio.to_thread(
                            lambda: render(
                                request, "auth/register.html", context, status=500
                            )
                        )

        return await asyncio.to_thread(
            lambda: render(request, "auth/register.html", context, status=400)
        )
