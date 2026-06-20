# catalog/admin/admin_product_group/admin_product.py:1
from django.forms import Select
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel

# from wagtail.snippets.models import register_snippet
# from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail_modeladmin.options import ModelAdmin

from catalog.models import ProductModel


class ProductAdmin(ModelAdmin):
    icon = "product"  # "globe"
    menu_icon = "product"  # "globe"
    menu_label = "Product Page 1"
    menu_order = 000
    # add_to_admin_menu = True
    list_display = [
        "is_active",
        "name",
        "category",
        "brand",
        "price",
        "stock_quantity",
        "discount_percent",
        "attributes",
        "attributes_additional",
        "created_at",
        "id",
    ]
    model = ProductModel
    # 📝 Панели редактирования
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("id"),
                FieldRowPanel(
                    [
                        FieldPanel("name"),
                        FieldPanel("stock_quantity"),
                        FieldPanel("is_active"),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel("price"),
                        FieldPanel("discount_percent"),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel("category"),
                        FieldPanel("brand"),
                    ]
                ),
            ]
        ),
        FieldPanel("describe_preview"),
        FieldPanel("description"),
        FieldPanel("attributes", widget=Select),
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
                        # FieldPanel("published_at", read_only=True),
                        # FieldPanel("version", read_only=True),
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


# register_snippet(BlogPageViewSet)
