"""
persons/admin.py:2
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from persons.models import Users

# Register your models here.


class BasicAdmin(SnippetViewSet):
    list_per_page = 10


class PanelAdmin(BasicAdmin):
    model = Users
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name" "username",
        "category",
    ]
    list_filter = ["username", "email", "first_name", "last_name"]
    ordering = (
        "username",
        "email",
    )


register_snippet(PanelAdmin)
