"""
persons/admin.py:2
"""

from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from persons.models import Users


class BasicAdmin(SnippetViewSet):
    list_per_page = 10


class PanelAdmin(BasicAdmin):
    model = Users
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name" "username",
    ]
    list_filter = ["username", "email", "first_name", "last_name"]
    ordering = (
        "username",
        "email",
    )


register_snippet(PanelAdmin)
