"""
persons/views/views_login.py
"""

import datetime
import logging
import threading

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View

from persons.forms import UsersLoginForm, UsersRegistrationForm
from persons.serfices import CostumizationSyncAsyncLoop
from project.settings import LOGIN_URL
from project.settings_conf.settings_env import CATEGORY_STATUS, USER_EMAIL_BASIS_MASSAGE

# from wagtail.admin.telepath.widgets import ValidationErrorAdapter


log = logging.getLogger(__name__)


class UsersRegistrationView(View):
    def __init__(self, **kwargs):
        """
        THis is the view class of the user registration.
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.log_t = "[%s]:" % UsersRegistrationView.__class__.__name__

    def get(
        self,
        request,
    ):
        try:
            form = UsersRegistrationForm()
            context = {
                "form": form,
                "category_choices": CATEGORY_STATUS,
            }

            return render(request, "admin/register.html", context)
        except Exception as e:
            self.log_t += (
                " Server error to the user registration GET. ERROR_TEXT: %s" % e.args[0]
                if e.args
                else str(e)
            )
            return HttpResponseRedirect("login", {"detail": self.log_t})
        finally:
            if "ERROR_TEXT:" not in self.log_t:
                log.info("%s Opened the form of the register page " % self.log_t)

            self.log_t = self.log_t.split("]: ")[0] + "]:"

    def post(self, request):
        form = UsersRegistrationForm(request.POST)
        url = request.headers.get("Referer")
        try:

            result_list = [
                item
                for item in ["register", "register/admin", "register/manager"]
                if item in url
            ]
            if result_list[0] is not None:
                if form.is_valid():
                    user = form.save()
                    log.info(request, user)
                    # ---- TEST BLOCK
                    try:

                        def test_funcrion():
                            return True

                        debug_result = CostumizationSyncAsyncLoop(user.username, {})
                        debug_result.get_new_function = test_funcrion
                        test_result = debug_result.get_new_loop()
                        thread = threading.Thread(target=test_result)
                        thread.start()
                        pass
                    except Exception as e:
                        ERROR_TEXT = " ".join(
                            [
                                self.log_t,
                                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                " Server error per open a new stream. URL: %s TEXT_ERROR: %s"
                                % (url, e.args[0] if e.args else str(e)),
                            ]
                        )
                        log.error(self.log_t)
                        return HttpResponseRedirect(
                            reverse(LOGIN_URL, kwargs={"details": ERROR_TEXT}),
                            status=500,
                        )
                    # ---- END TEST BLOCK
                    messages.success(
                        request, _("Registration successful! Please log in.")
                    )
                    return redirect("login")

                context = {
                    "form": form,
                    "category_choices": CATEGORY_STATUS,
                    "massage_for_user": USER_EMAIL_BASIS_MASSAGE,
                }

                return render(request, "admin/register.html", context, status=401)
            return HttpResponseRedirect(
                reverse(
                    "register",
                    kwargs={
                        "detail": """Something what wrong with the var.'category.\n
    It is from a registration form by url %s"""
                        % (url,)
                    },
                ),
                status=400,
            )
        except Exception as e:
            ERROR_TEXT = " ".join(
                [
                    self.log_t,
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    " Server error to the user registration. URL: %s TEXT_ERROR: %s"
                    % (url, e.args[0] if e.args else str(e)),
                ]
            )
            log.error(self.log_t)
            return HttpResponseRedirect(
                reverse(LOGIN_URL, kwargs={"details": ERROR_TEXT}),
                status=500,
            )
        finally:
            self.log_t = self.log_t.split(": ")[0] + ":"


class UserLoginView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log_t = "[%s]:" % UserLoginView.__class__.__name__

    def get(self, request):
        try:
            if request.user.is_authenticated:
                return redirect("wagtailadmin_home")
            form = UsersLoginForm()
            return render(request, "auth/login.html", {"form": form})
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

    def post(self, request):
        """
        TODO: Сохранение в базу данных!
        :param request:
        :return:
        """
        from persons.models import Users

        form = UsersLoginForm(request.POST)
        try:
            is_valid = form.is_valid()
            if is_valid:
                try:

                    user = Users.objects.get(email=form.cleaned_data.get("email"))
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
                                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                e.args[0] if e.args else str(e),
                            ),
                        ]
                    )
                    log.error(ERROR_TEXT)
                    return render(
                        request, "auth/login.html", {"details": ERROR_TEXT}, status=500
                    )
                finally:
                    pass
                try:
                    # return HttpResponseRedirect(reverse("admin-panel"))

                    return (redirect("wagtailadmin_home"),)
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
