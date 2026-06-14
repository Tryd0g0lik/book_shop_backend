"""
persons/views/views_login.py
"""

import asyncio
import base64
import datetime
import json
import logging

from allauth.account.views import LoginView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import status

from persons.exceptions.error_person import PersonLogingError
from persons.forms import UsersLoginForm
from persons.forms.verification_form import UsersCheckCodeVerificationForm
from persons.interfaces import UsersPydantic

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
        TODO: Сохранение в базу данных!
        :param request:
        :return:
        """
        from django.core import serializers

        from persons.apps import account_manager
        from persons.models import Users

        ERROR_TEXT = f"{self.log_t[:-1]}[{self.post.__name__}]: Error =>"
        database_service = account_manager.postman.database_service
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
                messages.warning(request, "User does not exists!")
                return JsonResponse(
                    data={
                        "details": ERROR_TEXT
                        + f" {PersonLogingError('User does not exists!')}"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            try:
                user = user_queryset.first()
                password_hashed = database_service.hashes_password(password)
                if user.password != password_hashed:
                    t = "User's password is invalid!"
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

                dtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user.is_active = True
                user.date_joined = dtime
                user.updated_at = dtime
                user.save(update_fields=["is_active", "date_joined", "updated_at"])
                # user_json: json = UsersPydantic.model_validate(user).to_public_dict()

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
                            "category": user.category,
                            "email": user.email,
                        }
                    )
                    request.session[user.verification_code] = session_data_json_str
                    return redirect(
                        "wagtailadmin:wagtailcore_login",
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
                        self.log_t[-2],
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


# DFMN-HTJB
