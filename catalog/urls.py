from django.urls import path, reverse

from catalog.views import toggle_product_active

urlpatterns = [
    path(
        "product/toggle-active/<int:pk>/",
        toggle_product_active,
        name="catalog_productmodel_toggle_active",
    ),
]
