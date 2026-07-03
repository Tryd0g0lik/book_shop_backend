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
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.http import require_GET, require_POST

from persons import CATEGORY_STATUS, EnumTemplatesKeysCache
from persons.apps import account_manager, cachemanager
from persons.forms import UsersRegistrationForm
from persons.forms.verification_form import UsersCheckCodeVerificationForm
from persons.models import Users
from persons.tasks.tasks_celery.task_send_letter_to_user_email import task_postman

# from project.settings_conf.settings_first import LOGIN_URL

log = logging.getLogger(__name__)
path_names: list[str] = [
    "/person/register/account/",
    "/person/register/admin/",
    "/person/register/moderator/",
    "/person/register/manager/",
]


class UsersRegistrationView(AllauthSignupView):
    """
    TODO: Тут имеем авторизованого пользоватяля. Без прав админа он рендерится на главную
            Разрулить урлы, чтою присволить роли
            Отправить код аутендификации и авторизации.
    """

    template_name = "auth/register.html"
    form_class = UsersRegistrationForm
    success_url = "register/admin"

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

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        """
        TODO: В зависимости от того какой pathname в result_list - присваеваем роль.
            400 ответ в JsonResponse(context_, status=400) - Перехватить черезJavaScript и вывести сообщение об ошибке.
        :param request:
            - request.HEADER Referer: Required. "http://127.0.0.1:8000/register/admin"
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
            return HttpResponseRedirect(reverse("/"), status=400)
        messages.success(request, _("Registration successful! Chek your email."))
        try:
            log.info(
                """\n
            # ============================================
            # POST'S DATA BEFORE SAVING IN DATABASE
            # ============================================
            """
            )
            result_list = [item for item in path_names if item in url_parent]

            if len(result_list) > 0:
                response = super().post(request, *args, **kwargs)
                if response and response.status_code >= 400:
                    context_ = {
                        "details": str(response.context_data["form"].errors),
                        "validation_sent": False,
                    }
                    messages.error(request, context_["details"])
                    log.warning(
                        self.log_t[:-1]
                        + f"[{self.post.__name__}]: "
                        + context_["details"]
                    )
                    return JsonResponse(context_, status=400)

                return HttpResponseRedirect(
                    reverse("persons:register_token"), status=302
                )
            elif len(result_list) == 0 and re.search(r"register/$", url_parent):
                log_t = (
                    self.log_t[:-1]
                    + f"[{self.post.__name__}]: "
                    + "User data before checks the code verification."
                )
                log.info(log_t)
                # Check of code verification
                messages.warning(
                    request, "Something what wrong! Send screenshot to the support."
                )
            return HttpResponseRedirect(
                reverse(
                    "persons:management",
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
        path = request.path
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
                role_ = path.split("register/")[-1].split("/")[0]
                context.update(
                    {
                        "form": form,
                        "category_choices": CATEGORY_STATUS,
                        "validation_sent": False,  # Code validation hase not been to send.
                        "role": role_,
                    }
                )
                # super().get(request, *args, **kwargs)
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
            return HttpResponseRedirect("/", {"detail": ERROR_TEXT})

    def form_invalid(self, form):
        """
        TODO: https://learn.javascript.ru/xmlhttprequest
            Емайл - уникальныq емал. Когда получаем ошибку (при заполнени формы) - показываем сообщение!! Остановить перезагрузку
        :param form:
        :return:
        """
        resp = super().form_invalid(form)
        resp.status_code = 400
        return resp

    def form_valid(self, form):
        from persons.apps import account_manager
        from persons.tasks.tasks_celery.task_set_cache import (
            task_of_cache,
        )

        username: str = form.cleaned_data.get("username")
        email: str = form.cleaned_data.get("email")
        role: str = form.cleaned_data.get("category")
        try:
            super().form_valid(form)
            user = Users.objects.get(email=email)
            user.set_password(form.cleaned_data.get("password1"))
            user.save()
            # Note: Below the 'category' we will be caching.
            # User will get own role/category when pass a verification.
            group, created = Group.objects.get_or_create(
                name=list(CATEGORY_STATUS[0])[1]
            )
            user.groups.add(group)
            user.save()

            queryset = Users.objects.filter(is_superuser=False, is_staff=True)
            # We can have a (count):
            # - Superadmin before 1;
            # - Admin ... 1;
            # - Manager ... 0-3;
            # - Client more.
            if role.upper() in CATEGORY_STATUS[1]:
                queryset_superadmin = Users.objects.filter(is_superuser=True)

                if queryset_superadmin.count() == 0:
                    # Superuser
                    setattr(user, "is_superuser", True)
                    setattr(user, "is_staff", True)
                elif queryset.count() == 0:
                    # Admins
                    setattr(user, "is_superuser", False)
                    setattr(user, "is_staff", True)
            elif (
                role.upper() in CATEGORY_STATUS[2]
                and queryset.count() >= 0
                and queryset.count() <= 3
            ):
                # Managers
                setattr(user, "is_superuser", False)
                setattr(user, "is_staff", True)
            else:
                # Clients
                setattr(user, "is_superuser", False)
                setattr(user, "is_staff", False)

            setattr(user, "updated_at", datetime.datetime.now())
            user.save(
                update_fields=[
                    "password",
                    "updated_at",
                    "is_superuser",
                    "is_staff",
                ]
            )
        except Exception as e:
            raise e

        if (username is None) or (
            username is not None and isinstance(username, str) and len(username) < 2
        ):
            setattr(form, "username", email.split("@")[0])

        args = (
            EnumTemplatesKeysCache.USER_PENDING_ZERO.value % re.sub(r"[@.]", "", email),
        )
        # ------------------------------------
        kwargs = {"category": role, "email": email}
        try:
            # CELERY + REDIS
            task_of_cache.delay(*args, **kwargs)
        except Exception as e:
            log_t = f"[UsersRegistrationView]: {e.args[0] if e.args else str(e)}"
            raise ValueError(log_t)
        finally:
            task_postman.delay(*args, **kwargs)
        # messages.success(self.request, message)

        return


class UsersVerificationDuringRegistration(View):
    form_class = UsersCheckCodeVerificationForm
    success_url = "register/"
    template_name = "auth/register.html"
    # async def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    async def get(self, request, *args, **kwargs):
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
        is_authenticated = await asyncio.to_thread(lambda: user.is_authenticated)
        if request.method == "GET" and not is_authenticated:
            token_key = request.GET.get("key")
            keys = EnumTemplatesKeysCache.USER_PENDING_LETTER.value % "*"
            collection_ = []
            await cachemanager.aget(key_pattern=keys, collection=collection_)

            if len(collection_) > 0:
                for key in collection_.copy():
                    key: bytes = key[:]
                    collection_.clear()
                    await cachemanager.aget(key=key.decode(), collection=collection_)
            if len(collection_) > 0:
                for item in collection_:
                    try:
                        user_cache_json = json.loads(item.decode())
                        if user_cache_json["verification_code"] == token_key:
                            user_cache_json["is_verified"] = True
                            collection_.clear()
                            database_service = account_manager.postman.database_service
                            result: Optional[dict] = await asyncio.to_thread(
                                lambda: database_service.update_in_database(
                                    user_cache_json,
                                    user_email=user_cache_json["email"],
                                )
                            )

                            if result is not None:
                                log.info("Verification code updated successfully")
                                category: str = result["category"]
                                admin_ = list(CATEGORY_STATUS[1])[0]
                                manager_ = list(CATEGORY_STATUS[2])[0]
                                url = "persons:login"
                                if (
                                    category.lower() == admin_.lower()
                                    or category.lower() == manager_.lower()
                                ):
                                    # url = f"{admin_.lower()}/login/"
                                    url = "wagtailadmin_login"

                                return await asyncio.to_thread(
                                    lambda: HttpResponseRedirect(
                                        reverse(
                                            url,
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
