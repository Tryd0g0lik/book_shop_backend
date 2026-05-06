"""
persons/views.py:3
"""

import logging
import threading

from django.conf.global_settings import LOGOUT_REDIRECT_URL
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.urls import reverse
from django.views import View

from persons.forms.users_registration_form import UsersRegistrationForm
from persons.serfices import CostumizationSyncAsyncLoop
from project.settings import LOGIN_URL
from project.settings_conf.settings_env import CATEGORY_STATUS, USER_EMAIL_BASIS_MASSAGE

log = logging.getLogger(__name__)

# Create your views here.
#
# def register(request):
#     from persons.forms.users_registration_form import UsersRegistrationForm
#     from project.settings import LOGIN_URL
#     form = UsersRegistrationForm()
#     if request.method == 'POST':
#         form = UsersRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse(LOGIN_URL))
#     return render(request, 'admin/register.html', {'form': form, "title": "Register"}, status=200)


class UsersRegistrationView(View):
    def __init__(self, **kwargs):
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
                        pass
                        raise e
                    # ---- END TEST BLOCK
                    return redirect("admin_home")

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
            self.log_t += (
                " Server error to the user registration. URL: %s TEXT_ERROR: %s"
                % (url, e.args[0] if e.args else str(e))
            )
            log.error(self.log_t)
            return HttpResponseRedirect(
                reverse(LOGIN_URL, kwargs={"detail": self.log_t.split(": ")[-1]}),
                status=500,
            )
        finally:
            self.log_t = self.log_t.split(": ")[0] + ":"
