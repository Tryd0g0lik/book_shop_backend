# catalog/admin/admin_category.py:1
from django.db import models
from django.db.models import QuerySet
from django.forms import ChoiceField, SelectMultiple
from modelcluster.fields import ParentalKey
from wagtail import hooks
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.contrib.forms.models import AbstractFormField
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail_modeladmin import forms
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from catalog.models import (
    BrandModel,
    CategoryModel,
    ProductGalleryImageModel,
    ProductModel,
)

# class LastnameField(Orderable):
#     user_id = ParentalKey("EmailAddress", on_delete=models.SET_NULL, related_name="%(app_label)s_%(class)s_product_characteristics_updated")


def describe_preview_preview(self):
    """Короткий превью для списка"""
    if self.describe_preview_preview:
        return self.describe_preview_preview[:12] + "..."
    return "-"


describe_preview_preview.short_description = "Preview"


def description_preview(self):
    """Короткий превью для списка"""
    if self.description_preview:
        return self.description_preview[:10] + "..."
    return "-"


description_preview.short_description = "Description"


class BlogPageViewSet(SnippetViewSet):
    icon = "product"  # "globe"
    menu_label = "Product Pages"
    add_to_admin_menu = True
    list_display = [
        "name",
        "category",
        "brand",
        "price",
        "stock_quantity",
        "discount_percent",
        "attributes",
        "attributes_additional",
        "created_at",
    ]
    model = ProductModel
    # 📝 Панели редактирования
    panels = [
        FieldPanel("name"),
        FieldPanel("price"),
        FieldPanel("discount_percent"),
        FieldPanel("category"),
        FieldPanel("brand"),
        FieldPanel("stock_quantity"),
        FieldPanel("description"),
        FieldPanel("describe_preview"),
        FieldPanel("attributes"),
        FieldPanel("attributes_additional"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("created_at", read_only=True),
                        FieldPanel("created_by", read_only=True),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel("updated_at", read_only=True),
                        FieldPanel("updated_by", required_on_save=True),
                    ]
                ),
            ]
        ),
    ]

    # 📊 Экспорт
    list_export = [
        "id",
        "name",
        "price",
        "category__name",
        "brand__name",
        "stock_quantity",
        "created_at",
    ]


register_snippet(BlogPageViewSet)


class ProductPageAdmin(ModelAdmin):
    model = ProductGalleryImageModel
    list_display = [
        "page",
        "caption",
        "image",
        "product",
    ]
    search_fields = ["page", "caption"]
    list_filter = ["created_at"]
    icon = "tag"
    add_to_admin_menu = True
    menu_label = "Produсt Page"
    menu_order = 300

    panels = [
        FieldPanel("page"),
        FieldPanel("caption"),
        FieldPanel("image"),
        FieldPanel("product"),
    ]
    # inlines = [BasicInline]


modeladmin_register(ProductPageAdmin)


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

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]


modeladmin_register(CategoryAdmin)


class BrandAdmin(ModelAdmin):
    model = BrandModel
    menu_label = "Brands"
    menu_icon = "tag"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False

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
modeladmin_register(BrandAdmin)

# class ProductAdmin(ModelAdmin):
#     model = ProductModel
#     menu_label = "Brands"
#     menu_icon = "tag"
#     menu_order = 300
#     add_to_settings_menu = False
#     exclude_from_explorer = False
#
#     list_display = ["name", "describe_preview", "description", "category", "brand", "price","stock_quantity", "discount_percent", "attributes ","attributes_additional ", "created_at"]
#     list_filter = ["created_at"]
#     search_fields = ["name", "description"]
#     list_per_page = 25
#
#     # Панели для редактирования
#     panels = [
#         "name", "description",
#     ]
#
#
# # ✅ Регистрируем ModelAdmin
# modeladmin_register(BrandAdmin)


class SnippetBrendAdmin(SnippetViewSet):
    model = BrandModel
    menu_label = "Brands Snippet"
    menu_icon = "tag"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False

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
register_snippet(SnippetBrendAdmin)
