# catalog/admin/admin_product_group/admin_product.py:1
from django.forms import TextInput
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from wagtail.admin import messages
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail_modeladmin.options import ModelAdmin

from catalog.models import ProductModel


class ProductAdmin(ModelAdmin):
    model = ProductModel
    menu_icon = "tag"
    menu_label = _("Products")
    add_to_settings_menu = True
    exclude_from_explorer = False
    base_url_path = "catalog/product"
    menu_order = 500
    list_per_page = 25
    list_display = [
        "id",
        "name",
        "category",
        "brand",
        "price",
        "stock_quantity",
        "is_active_toggle",
    ]
    search_fields = ["name", "brand", "category"]

    def is_active_toggle(self, obj):
        """Переключатель статуса прямо в списке"""
        if obj.is_active:
            icon = "🟢"
            status = _("Active")
            color = "green"
        else:
            icon = "🔴"
            status = _("Inactive")
            color = "red"
        toggle_url = reverse(
            "catalog:catalog_productmodel_toggle_active", args=[obj.id]
        )

        return format_html(
            '<a href="{}" style="color: {}; text-decoration: none; font-weight: bold;" title="Нажмите для переключения">{} {}</a>',
            toggle_url,
            color,
            icon,
            status,
        )

    is_active_toggle.short_description = _("Status")

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions["activate_products"] = (
            self.activate_products,
            "activate_products",
            _("Активировать выбранные"),
        )
        actions["deactivate_products"] = (
            self.deactivate_products,
            "deactivate_products",
            _("Деактивировать выбранные"),
        )
        return actions

    def activate_products(self, request, queryset):
        count = queryset.update(is_active=True)
        messages.success(request, f"{count} продуктов активировано")

    def deactivate_products(self, request, queryset):
        count = queryset.update(is_active=False)
        messages.success(request, f"{count} продуктов деактивировано")
