# catalog/admin/admin_product_group/admin_category.py:1
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail_modeladmin.options import ModelAdmin

from catalog.models import CategoryModel


class CategoryAdmin(ModelAdmin):
    model = CategoryModel
    icon = "tag"
    menu_icon = "tag"
    menu_label = _("Categories")
    add_to_admin_menu = False
    base_url_path = "catalog/categories"
    menu_order = 400
    list_par_page = 25

    list_display = ["name", "description", "created_at", "updated_at"]
    list_filter = [
        "created_at",
        "updated_at",
    ]
    search_fields = ["name", "created_at", "updated_at", "description"]
