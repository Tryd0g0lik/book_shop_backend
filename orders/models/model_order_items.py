# orders/models/model_order_items.py:1order
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderItemModel(models.Model):
    """Number of product in the order"""

    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Order"),
        db_index=True,
    )
    product = models.ForeignKey(
        "products.ProductModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items",
        verbose_name=_("Product"),
    )

    # === DATA OF PRODUCT ON MOMENT OF ORDER
    product_name = models.CharField(
        max_length=255,
        verbose_name=_("Product Name"),
    )
    product_sku = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name=_("Product SKU"),
        db_index=True,
    )
    product_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Product Price on the order moment"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    product_discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_("Product Discount on the order moment"),
        validators=[MinValueValidator(Decimal("0.00"))],
        default=Decimal("0.00"),
    )

    # === QUANTITY
    quantity = models.PositiveIntegerField(
        default=1,
        help_text=_("The quantity of the product"),
        verbose_name=_("Quantity"),
        validators=[MinValueValidator(1)],
    )
    # TOTAL SUMM OF THE ONE POSITION
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Subtotal"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Total"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    # OPTION
    options = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Options of the one product"),
        help_text=_("Example: {'color': 'red', 'size': 'M'}"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "order_item"
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
        ordering = ["created_at"]

    def __str__(self):
        return _(f"Item {self.product_name} x {self.quantity} (Order #{self.order.id})")

    def save(self, *args, **kwargs):
        self.subtotal = self.product_price * self.quantity
        self.total = (self.product_price - self.product_discount) * self.quantity
