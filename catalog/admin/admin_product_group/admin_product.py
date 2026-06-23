# # catalog/admin/admin_product_group/admin_product.py:1
#
# from django.forms import SelectMultiple, Select
# from django.utils.translation import gettext_lazy as _
# from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel, InlinePanel
# from wagtail_modeladmin.options import ModelAdmin
#
# from catalog.admin.witgets import JSONSelectMultipleWidget
# from catalog.models import ProductGalleryImageModel, ProductModel
# from django import forms
#
#
# class ProductAdmin(ModelAdmin):
#     """Menu position of catalog and common list of products
#     This page this only data of product which will be displayed in the general catalog.
#     """
#
#     model = ProductGalleryImageModel
#     icon = "product"  # "globe"
#     menu_icon = "product"  # "globe"
#     menu_label = _("List of products")
#     menu_order = 000
#     # add_to_admin_menu = True
#     list_display = ["is_active",  "caption", "version", "published_at"]
#
#     # list_display = [
#     #     "is_active",
#     #     "category",
#     #     "brand",
#     #     "price",
#     #     "stock_quantity",
#     #     "discount_percent",
#     #     "attributes",
#     #     "attributes_additional",
#     #     "created_at",
#     #     "id",
#     # ]
#
#     # # 📝 Панели редактирования
#     # panels = [
#     #     MultiFieldPanel(
#     #         [
#     #             FieldPanel("id"),
#     #             FieldRowPanel(
#     #                 [
#     #                     FieldPanel("name"),
#     #                     FieldPanel("stock_quantity"),
#     #                     FieldPanel("is_active"),
#     #                 ]
#     #             ),
#     #             FieldRowPanel(
#     #                 [
#     #                     FieldPanel("price"),
#     #                     FieldPanel("discount_percent"),
#     #                 ]
#     #             ),
#     #             FieldRowPanel(
#     #                 [
#     #                     FieldPanel("category"),
#     #                     FieldPanel("brand"),
#     #                 ]
#     #             ),
#     #         ]
#     #     ),
#     #     FieldPanel("describe_preview"),
#     #     FieldPanel("description"),
#     #     FieldPanel("attributes", widget=SelectMultiple),
#     #     FieldPanel("attributes_additional", widget=JSONSelectMultipleWidget),
#     #     MultiFieldPanel(
#     #         [
#     #             FieldRowPanel(
#     #                 [
#     #                     FieldPanel("created_at", read_only=True),
#     #                     FieldPanel("created_by", read_only=True),
#     #                 ]
#     #             ),
#     #             FieldRowPanel(
#     #                 [
#     #                     FieldPanel("updated_at", read_only=True),
#     #                     FieldPanel("updated_by", required_on_save=True),
#     #                 ]
#     #             ),
#     #         ]
#     #     ),
#     # ]
#
#     # 📊 Экспорт
#     # list_export = [
#     #     "id",
#     #     "name",
#     #     "price",
#     #     "category__name",
#     #     "brand__name",
#     #     "stock_quantity",
#     #     "created_at",
#     # ]
