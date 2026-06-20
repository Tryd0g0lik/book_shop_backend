# catalog/admin/admin_product_group/admin_product_characteristics.py:1
from django.utils.translation import gettext_lazy as _
from wagtail_modeladmin.options import ModelAdmin

from catalog.models import ProductCharacteristics


class ProductCharacteristicsAdmin(ModelAdmin):
    model = ProductCharacteristics
    add_to_admin_menu = False
    list_display = ["name", "value", "description", "created_at", "updated_at", "id"]
    menu_order = 200
    menu_icon = "fa-user"
    list_per_page = 25
    menu_label = _("Product Characteristics")

    panels = [
        "name",
        "value",
        "description",
    ]
