# catalog/admin/admin_pages/admin_test_pages.py:4
# from wagtail.snippets.models import register_snippet
# from wagtail.snippets.views.snippets import SnippetViewSet
from django.utils.translation import gettext_lazy as _
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from catalog.models import BrandModel


class BrandAdmin(ModelAdmin):
    model = BrandModel
    menu_label = _("Brand")
    menu_icon = "tag"
    menu_order = 300
    add_to_settings_menu = True
    exclude_from_explorer = True

    list_display = ["name", "description", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "description"]
    list_per_page = 25

    # Панели для редактирования
    panels = [
        "name",
        "description",
    ]


# ✅ Регистрируем ModelAdmin


#
# class SnippetBrendAdmin(SnippetViewSet):
#     model = BrandModel
#     menu_label = "Brands Snippet"
#     menu_icon = "tag"
#     # menu_order = 300
#     add_to_settings_menu = False
#     exclude_from_explorer = False
#
#     list_display = ["name", "description", "created_at"]
#     list_filter = ["created_at"]
#     search_fields = ["name", "description"]
#     list_per_page = 25
#
#     # Панели для редактирования
#     panels = [
#         "name",
#         "description",
#     ]


# ✅ Регистрируем ModelAdmin
# register_snippet(SnippetBrendAdmin)
