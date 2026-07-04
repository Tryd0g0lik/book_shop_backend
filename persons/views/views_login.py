"""
persons/views/views_login.py
"""

import asyncio
import datetime
import json
import logging

from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.account.views import LoginView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import QuerySet
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from rest_framework import status

from persons.exceptions.error_person import PersonLogingError
from persons.forms import UsersLoginForm
from persons.forms.verification_form import UsersCheckCodeVerificationForm

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
         Функцию - восстановить пароль - проверить после настройки посты на внешний провайдер.
        :param request:
        :return:
        """
        from django.core import serializers

        from persons.apps import account_manager
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
                dtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

                # --- Allauth
                queryset = EmailAddress.objects.filter(user=user)
                if queryset.exists():
                    account_email = queryset.first()
                    email_conf = None
                    if account_email.email == user.email:
                        setattr(account_email, "verified", True)
                        account_email.save(update_fields=["verified"])
                        email_conf = EmailConfirmation.objects.filter(
                            email_address_id=account_email.id,
                        )
                    else:
                        log.warning(
                            self.log_t[-1]
                            + f"[{self.post.__name__}]:"
                            + "Allauth did not save new verified!"
                        )
                    email_obj = email_conf.first() if email_conf.exists() else None
                    if email_obj is not None:
                        email_obj.verified = True
                        email_obj.save()
                    else:
                        log.warning(
                            self.log_t[-1]
                            + f"[{self.post.__name__}]:"
                            + "Allauth did not save new email!"
                        )

                # ---
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

                    return redirect(
                        "wagtailadmin_home",
                    )
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
