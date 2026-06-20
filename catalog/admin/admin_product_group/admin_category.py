# catalog/admin/admin_product_group/admin_category.py:1
from wagtail.admin.panels import FieldPanel
from wagtail_modeladmin.options import ModelAdmin

from catalog.models import CategoryModel


class CategoryAdmin(ModelAdmin):
    model = CategoryModel
    list_display = [
        "name",
        "description",
    ]
    search_fields = ["name", "description"]
    list_filter = ["created_at"]
    icon = "tag"
    add_to_admin_menu = True
    menu_label = "Categories"
    menu_order = 300

    panels = {
        FieldPanel("name"),
        FieldPanel("description"),
    }
