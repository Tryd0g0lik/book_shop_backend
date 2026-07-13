"""
persons/views/views_login.py
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
from persons.tasks.tasks_celery.task_allauth import tasks_position_allauth
from persons.tasks.tasks_celery.tasks_wagtail import tasks_position_wagtail
from profiles.tasks.task_signals.task_create_profile import create_profile_signal
from utilities import CATEGORY_STATUS

log = logging.getLogger(__name__)


class UserLoginView(LoginView):
    form_class = UsersLoginForm
    template_name = "auth/login.html"
    log_t = "[UserLoginView]:"
    _lock = asyncio.Lock()

    def get(self, request, *args, **kwargs):
        """
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
        :param request:
        :return:
        """
        from persons.models import Users

        ERROR_TEXT = f"{self.log_t[:-1]}[{self.post.__name__}]: Error =>"
        user_request = request.user
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = None
        is_anonymous: bool = user_request.is_anonymous
        if is_anonymous:
            # Getting of user from database
            user_queryset: QuerySet[Users] = Users.objects.filter(email=email)
            if not user_queryset.exists():

                log.warning(ERROR_TEXT + " User does not exists!")
                messages.warning(request, _("User does not exists!"))
                return JsonResponse(
                    data={
                        "details": ERROR_TEXT
                        + f" {PersonLogingError('User does not exists!')}"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            try:
                user = user_queryset.first()
                password_hashed = user.check_password(password)
                if not password_hashed:
                    t = _("User's password is invalid!")
                    log.warning(ERROR_TEXT + f" {t}")
                    messages.warning(request, t)
                    return JsonResponse(
                        data={"details": ERROR_TEXT + f" {PersonLogingError(t)}"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            except Exception as e:
                return JsonResponse(
                    data={
                        "details": ERROR_TEXT
                        + f" {PersonLogingError(e.args if e.args else str(e))}"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            try:
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
                # --- Profile
                kwargs = {"user_id": user.id, "timeout_server": 3}
                args = []
                log.info(
                    f"Before 'tasks_position_allauth': DEBUG Profile args: {str(args)} & kwargs: {str(kwargs)}"
                )
                tasks_position_allauth.delay(*args, **kwargs)
                kwargs = {"user_id": user.id, "timeout_server": 3}
                log.info(
                    f"Before 'tasks_position_wagtail': DEBUG Profile args: {str(args)} & kwargs: {str(kwargs)}"
                )
                tasks_position_wagtail.delay(args, **kwargs)
                kwargs = {"user_id": user.id}
                log.info(
                    f"Before 'create_profile_signal': DEBUG Profile args: {str(args)} & kwargs: {str(kwargs)}"
                )
                create_profile_signal.send(sender=self.__class__, **kwargs)

                # --- USER LOGIN
                request.session.save()
                user_auth = authenticate(
                    request=request, email=email, password=password
                )
                if user_auth is not None:
                    login(request, user_auth)
                    request.user = user_queryset.first()
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
                    queryset_profile = user.groups.values_list("name", flat=True)
                    if queryset_profile.exists():
                        profile = queryset_profile.first()
                        if profile.upper() in [
                            CATEGORY_STATUS[1][0],
                            CATEGORY_STATUS[1][0],
                            CATEGORY_STATUS[2][0],
                            CATEGORY_STATUS[4][0],
                            CATEGORY_STATUS[5][0],
                        ]:
                            return redirect(
                                "wagtailadmin_home",
                            )
                        return redirect("catalog")
                messages.warning(request, "User login or password is invalid!")
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
