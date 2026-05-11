"""
persons/views/views_login.py
"""

import datetime
import logging

from allauth.account.views import LoginView as AllauthLoginView
from allauth.account.views import LogoutView as AllauthLogoutView
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.db.models.expressions import result
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View

from persons.forms import UsersLoginForm
from persons.models import Users

# from wagtail.admin.telepath.widgets import ValidationErrorAdapter


log = logging.getLogger(__name__)


class UserLoginView(AllauthLoginView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log_t = "[%s]:" % UserLoginView.__class__.__name__

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :return:
        """

        try:

            user = request.user
            if user.is_authenticated and user.is_active:
                if user.is_staff or user.is_superuser:
                    return redirect("wagtailadmin_home")
                else:
                    messages.warning(
                        request, _("Your account doesn't have admin access.")
                    )
                    return redirect("/")

            result_debug = super().get(request, *args, **kwargs)
            form = UsersLoginForm()
            result_debug.context = {"form": form}
            result_debug.template_name = "auth/login.html"  # "persons/login.html"
            return result_debug
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
            log.error(ERROR_TEXT)
            return HttpResponseRedirect(reverse("login"), {"details": ERROR_TEXT})
        finally:
            pass

    def post(self, request, *args, **kwargs):
        """
        TODO: Сохранение в базу данных!
        :param request:
        :return:
        """
        super().post(request, *args, **kwargs)

        form = UsersLoginForm(request.POST)
        try:
            is_valid = form.is_valid()

            if is_valid:
                user = Users.objects.get(email=form.cleaned_data.get("email"))
                if not user.is_staff:
                    try:

                        user.is_staff = True
                        user.is_active = True
                        dtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        user.date_joined = dtime
                        user.updated_at = dtime
                        user.save()
                        auth_login(request, user)
                    except Exception as e:
                        ERROR_TEXT = " ".join(
                            [
                                self.log_t[-2],
                                ".%s]: %s Error => %s"
                                % (
                                    self.post.__name__,
                                    datetime.datetime.now().strftime(
                                        "%Y-%m-%d %H:%M:%S"
                                    ),
                                    e.args[0] if e.args else str(e),
                                ),
                            ]
                        )
                        log.error(ERROR_TEXT)
                        return render(
                            request,
                            "auth/login.html",
                            {"details": ERROR_TEXT},
                            status=500,
                        )
                    finally:
                        pass
                try:
                    # return HttpResponseRedirect(reverse("admin-panel"))

                    return redirect("wagtailadmin_home")
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
                    return HttpResponseRedirect(
                        reverse("login"), {"details": ERROR_TEXT}, status=500
                    )
                finally:
                    pass
            dtime = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),)

            error_details = {
                "form_errors": dict(form.errors),
                "non_filed_errors": form.non_field_errors(),
                "submit_data": {
                    k: v
                    for k, v in request.POST.items()
                    if k != "csrf_token" or k != "csrfmiddlewaretoken"
                },
            }
            WARN_TEXT = " ".join(
                [
                    self.log_t[-1],
                    ".%s]: %s Error => %s"
                    % (
                        self.post.__name__,
                        dtime,
                        "Data of form is no valid => " + str(error_details),
                    ),
                ]
            ).replace("] [", "][")
            log.warning(WARN_TEXT, {"details": WARN_TEXT})
            return redirect("login")
        except Exception as e:
            dtime = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),)
            ERROR_TEXT = " ".join(
                [
                    self.log_t[-2],
                    ".%s]: %s Error => %s"
                    % (self.post.__name__, dtime, e.args[0] if e.args else str(e)),
                ]
            )
            log.error(ERROR_TEXT)
            return render(
                request, "auth/login.html", {"details": ERROR_TEXT}, status=500
            )
