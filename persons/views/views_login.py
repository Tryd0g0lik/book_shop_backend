"""
persons/views/views_login.py
Login
"""

import asyncio
import datetime
import json
import logging

from allauth.account.views import LoginView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import QuerySet
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status

from persons.exceptions.error_person import PersonLogingError
from persons.forms import UsersLoginForm
from persons.forms.verification_form import UsersCheckCodeVerificationForm
from persons.interfaces import Users as UsersInterface
from persons.models import Users
from persons.tasks.tasks_celery.task_allauth import tasks_position_allauth
from persons.tasks.tasks_celery.tasks_wagtail import tasks_position_wagtail
from profiles.tasks.task_signals.task_create_profile import create_profile_signal
from utilities import CATEGORY_STATUS
from utilities.middleware.functions_jwt_tokens import get_tokens_for_user

log = logging.getLogger(__name__)


class UserLoginView(LoginView):
    form_class = UsersLoginForm
    template_name = "auth/login.html"
    log_t = "[UserLoginView]:"
    _lock = asyncio.Lock()

    def get(self, request, *args, **kwargs):
        """
        THis is method is  opening the form's page for a login-ing
        :param request:
        :return:
        """
        try:
            user = request.user
            form = self.form_class
            context = {"form": form}
            if user.is_anonymous:
                return render(
                    request, "auth/login.html", context, status=status.HTTP_200_OK
                )
            return JsonResponse(
                data={"details": PersonLogingError("User already exists!")}
            )
        except Exception as e:
            ERROR_TEXT = " ".join(
                [
                    self.log_t[-2],
                    "%s]: %s Error => %s"
                    % (
                        self.get.__name__,
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        e.args[0] if e.args else str(e),
                    ),
                ]
            )
            log.error(PersonLogingError(ERROR_TEXT))
            form = UsersCheckCodeVerificationForm()
            context = {"validation_sent": True, "form": form}
            return render(
                request,
                "auth/register.html",
                context,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            pass

    def post(self, request, *args, **kwargs):
        """
        TODO: После авторизации:
          - удалить запись из кеша!!!!!!
          - Создать (редирект для клиента) маршрут в аккаунт или в каталог для клиента
          - Прописать JWT токен тут или при редиректе (после удачной авторизации)
          - роли client, manager, editor не имеют страницы для редиректа в случае удачного логина.
          - 'redirect("catalog")' изменить ссылку для редиректа
         Функцию - восстановить пароль - проверить после настройки посты на внешний провайдер.
        :param str email: Required. Form data. Email of user for a logining.
        :param str password: Required. Form data. Password for user for a logining.
        :return: If all successful mean we returning a redirect to the admin (if it is user with right) or
            catalog (if it is a client).
        """
        LOG_TEXT = f"{self.log_t[:-1]}[{self.post.__name__}]: Error =>"
        user_request = request.user
        email = request.POST.get("email")
        password = request.POST.get("password")

        is_anonymous: bool = user_request.is_anonymous
        if is_anonymous:
            # ============================================
            # GETTING OF USER FROM DATABASE & UPDATING DATS
            # ============================================
            user_queryset: QuerySet[Users, Users] = Users.objects.filter(email=email)
            response: JsonResponse | None = self.sub_user_updating_db(
                request, user_queryset, email, password, LOG_TEXT
            )
            if response is None:
                return response
            try:
                user = user_queryset.first()
                # ============================================
                # THE TASKS AT THE ANOTHER THREAD
                # --- Profile
                # ============================================
                self.run_tasks(user.id, self.__class__)
                # ============================================
                # USER LOGIN & AUTHENTICATE
                # ============================================
                request.session.save()
                user_auth = authenticate(
                    request=request, email=email, password=password
                )
                if user_auth is not None:
                    login(request, user_auth)
                    request.user = user
                    session_data_json_str = json.dumps(
                        {
                            "username": user.username,
                            "category": ", ".join(
                                user.groups.values_list("name", flat=True)
                            ),
                            "email": user.email,
                        }
                    )
                    request.session[user.verification_code] = session_data_json_str
                    # ============================================
                    # JWT OF USER
                    # ============================================
                    tokens = get_tokens_for_user(request.user)
                    setattr(
                        request.headers, "Authorization", "Bearer {}".format(tokens)
                    )

                    queryset_profile = user.groups.values_list("name", flat=True)
                    # ---
                    if queryset_profile.exists():
                        profile = queryset_profile.first()
                        if profile.upper() in [item[0] for item in CATEGORY_STATUS[1:]]:
                            return redirect(
                                "wagtailadmin_home",
                            )
                        return redirect("catalog")
                messages.warning(request, _("User login or password is invalid!"))
                return render(
                    request,
                    "auth/login.html",
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            except Exception as e:
                ERROR_TEXT = " ".join(
                    [
                        self.log_t[-1] + f"[{self.post.__name__}]:",
                        ".%s]: %s Error => %s"
                        % (
                            self.post.__name__,
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            e.args[0] if e.args else str(e),
                        ),
                    ]
                )
                log.error(ERROR_TEXT)
                return render(
                    request,
                    "auth/login.html",
                    {"details": ERROR_TEXT},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return render(
            request,
            "index.html",
            {"details": _("User hase already logged")},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @staticmethod
    def run_tasks(
        user_id,
        sender_,
        timeout=3,
    ):
        kwargs = {"user_id": user_id, "timeout_server": timeout}
        args = []
        tasks_position_allauth.delay(*args, **kwargs)
        kwargs = {"user_id": user_id, "timeout_server": timeout}
        tasks_position_wagtail.delay(args, **kwargs)
        kwargs = {"user_id": user_id}
        create_profile_signal.send(sender=sender_, **kwargs)

    @staticmethod
    def sub_user_updating_db(
        request,
        user_queryset: QuerySet[Users, Users],
        email_: str,
        password_: str,
        prefix_log="",
    ):
        """

        :param request:
        :param person.models.Users user: On the external code we continue a work
        :param email_: Required. User email
        :param password_: Required. User password. The password variable will be changing/rename after a hashing.

        :param prefix_log: Start text to logging
        :return: JsonResponse if something is wrong
        """

        ERROR_TEXT = (
            "[{}]:".format(UserLoginView.sub_user_updating_db.__name__)
            if len(prefix_log) == 0
            else "{}[{}]:".format(
                prefix_log, UserLoginView.sub_user_updating_db.__name__
            )
        )
        if not user_queryset.exists():

            log.warning("{} User does not exists!".format(ERROR_TEXT))
            messages.warning(request, _("User does not exists!"))
            return JsonResponse(
                data={
                    "details": "{} {}".format(
                        ERROR_TEXT, PersonLogingError("User does not exists!")
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            user = user_queryset.first()
            # --- Person
            dtime = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            user.is_active = True
            user.is_verified = True
            user.date_joined = dtime
            user.updated_at = dtime
            user.save(
                update_fields=[
                    "is_active",
                    "date_joined",
                    "updated_at",
                    "is_verified",
                ]
            )
            password_hashed = user.check_password(password_)
            if not password_hashed:
                t = _("User's password is invalid!")
                log.warning("{} {}".format(ERROR_TEXT, t))
                messages.warning(request, t)
                return JsonResponse(
                    data={"details": "{} {}".format(ERROR_TEXT, PersonLogingError(t))},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except Exception as e:
            return JsonResponse(
                data={
                    "details": "{} {}".format(
                        ERROR_TEXT, PersonLogingError(e.args if e.args else str(e))
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        return None
