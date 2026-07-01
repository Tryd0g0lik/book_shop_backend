from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from catalog.models import ProductModel


def toggle_product_active(request, pk):
    """Переключает is_active для конкретного продукта"""
    product = get_object_or_404(ProductModel, pk=pk)
    product.is_active = not product.is_active
    product.save()

    status = "активирован" if product.is_active else "деактивирован"
    messages.success(request, f'Продукт "{product.name}" {status}')

    # Перенаправляем обратно на список
    return HttpResponseRedirect(
        request.META.get("HTTP_REFERER", "/admin/catalog/product/")
    )
