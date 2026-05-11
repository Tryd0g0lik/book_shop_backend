"""
persons/views/views_register.py:1
"""

import datetime
import logging
import re

from allauth.account.adapter import get_adapter
from allauth.account.views import SignupView as AllauthSignupView
from django.contrib import messages
from django.db.models.expressions import result
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.http import require_GET, require_POST

from persons.forms import UsersRegistrationForm
from project.settings import LOGIN_URL
from project.settings_conf.settings_env import APP_DEFAULT_FROM_EMAIL, CATEGORY_STATUS
from project.settings_conf.settings_security import ACCOUNT_ADAPTER

log = logging.getLogger(__name__)


class UsersRegistrationView(AllauthSignupView):
    """
    TODO: Тут имеем авторизованого пользоватяля. Без прав админа он рендерится на главную
            Разрулить урлы, чтою присволить роли
            Отправить код аутендификации и авторизации.
    """

    template_name = "auth/register.html"
    form_class = UsersRegistrationForm
    success_url = "admin/login"

    def __init__(
        self,
        **kwargs,
    ):
        """
        THis is the view class of the user registration.
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.log_t = ("[%s]:" % UsersRegistrationView.__class__.__name__,)

    @method_decorator(require_GET)
    def get(
        self,
        request,
        *args,
        **kwargs,
    ):

        user = request.user
        is_open: bool = self.is_open()
        if not user.is_anonymous or user.id is not None or not is_open:
            log_t = _("User on that email already exists.")
            log.warning(log_t)
            raise ValueError(log_t)

        try:
            form = self.get_form()
            context = {
                "form": form,
                "category_choices": CATEGORY_STATUS,
            }

            super().get(request, *args, **kwargs)

            # response.rendered_content = render_to_string(
            #     "auth/register.html",
            #     context,
            #     request=request
            # )
            # response.template_name = "auth/register.html"
            # response.META = request.META
            # response.user = request.user
            # response.headers = request.headers
            # response.COOKIES = request.COOKIES
            # response.template_name = self.template_name

            return render(request, "auth/register.html", context, status=200)
            # return response
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
            return HttpResponseRedirect("login", {"detail": ERROR_TEXT})
        finally:
            pass

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):

        # form = self.form_class(request.POST)
        pathname = request.path
        user = request.user
        url_parent = request.headers.get("Referer")

        if request.user.is_authenticated or (
            user.is_active and not user.is_anonymous and not user.is_superuser
        ):
            log_t = _("User on that email already exists.")
            log.warning(log_t + "Authenticated user tried to register")
            return redirect("/")
        # ---- END TEST BLOCK
        messages.success(request, _("Registration successful! Chek your email."))

        try:
            """
            TODO: В зависимости от того какой pathname в result_list - присваеваем роль.
            """
            result_list = [
                item
                for item in ["register/admin", "register/moderator", "register/manager"]
                if item in url_parent or re.search(r"/register/$", url_parent)
            ]

            if result_list[0] is not None:
                super().post(request, *args, **kwargs)
                # response.META = request.META
                # response.user = request.user
                # response.headers = request.headers
                # response.COOKIES = request.COOKIES

                # return redirect("login")
                log.info("[UsersRegistrationView]: TEST DEBUG POST")
                # return render(response, "auth/login.html", status=201)
                return render(request, "auth/register.html", status=201)
                # return response
                # context = {
                #     "form": form,
                #     "category_choices": CATEGORY_STATUS,
                #     "message_for_user": USER_EMAIL_BASIS_MESSAGE,
                # }
                #
                # return render(request, "auth/register.html", context, status=401)
            return HttpResponseRedirect(
                reverse(
                    "register",
                    kwargs={
                        "detail": """Something what wrong with the var.'category.\n
    It is from a registration form by url %s"""
                        % (pathname,)
                    },
                ),
                status=400,
            )
        except Exception as e:
            ERROR_TEXT = " ".join(
                [
                    self.log_t[-1] + f"{self.get.__name__}:",
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    " Server error to the user registration. URL: %s TEXT_ERROR: %s"
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
        from django.core.mail import send_mail

        username = form.cleaned_data.get("username")
        to_email = form.cleaned_data.get("email")
        if (username is None) or (
            username is not None and isinstance(username, str) and len(username) < 2
        ):
            setattr(form, "username", to_email.split("@")[0])
        try:

            super().form_valid(form)
        except Exception as e:
            log_t = f"[UsersRegistrationView]: {e.args[0] if e.args else str(e)}"
            raise ValueError(log_t)

        message = "Регистрация почти завершена! Проверьте вашу почту."

        try:
            text_context = render_to_string(
                "account/email/email_confirmation_signup_message.txt"
            )
            subject = "Test Email message"
            send_mail(subject, text_context, APP_DEFAULT_FROM_EMAIL, [to_email])
        except Exception as e:
            log_t = _(
                f"[UsersRegistrationView] TEXT_ERROR: {e.args[0] if e.args else str(e)}"
            )
            message = "Hte function was completed with containing a mistakes. Look in a loog messages."
            messages.error(self.request, message)
            raise ValueError(log_t)
        messages.success(self.request, message)

        return
