from django.forms import TextInput
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail_modeladmin.options import ModelAdmin

from catalog.models import ProductCharacteristics


class CharacteristicsAdmin(ModelAdmin):
    model = ProductCharacteristics
    menu_icon = "tag"
    menu_order = 600
    add_to_settings_menu = False
    add_to_admin_menu = True
    list_per_page = 25
    base_url_path = "catalog/products/characteristics/"
    list_display = ("name", "description", "created_at", "updated_at")
    list_filter = (
        "created_at",
        "updated_at",
    )
    panels = [
        FieldPanel("name"),
        FieldPanel("value"),
        FieldPanel("description"),
    ]
