# catalog/admin/admin_pages/admin_test_pages.py:4
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail_modeladmin.options import ModelAdmin

from catalog.models import BrandModel


class BrandAdmin(ModelAdmin):
    model = BrandModel
    menu_icon = "tag"
    menu_label = _("Brand")
    add_to_settings_menu = True
    exclude_from_explorer = False
    base_url_path = "catalog/brand"
    menu_order = 300
    list_per_page = 25

    list_display = [
        "name",
        "description",
        "updated_at",
    ]
    list_filter = [
        "created_at",
        "updated_at",
    ]
    search_fields = ["name", "created_at", "updated_at", "description"]
    # Панели для редактирования
    panels = [
        MultiFieldPanel(
            [
                "name",
                "description",
                FieldRowPanel([FieldPanel("created_at", read_only=True), "updated_at"]),
            ]
        ),
    ]
