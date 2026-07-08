# orders/models/model_order_log.py:1
from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderLogModel(models.Model):
    """History of changes by status of order"""

    order = models.ForeignKey(
        "orders.OrderModel",
        on_delete=models.CASCADE,
        related_name="logs",
        verbose_name=_("Order"),
        db_index=True,
    )

    # === WHO CHANGED
    user = models.ForeignKey(
        "persons.Users",
        on_delete=models.SET_NULL,
        verbose_name="User",
        related_name="order_logs",
        blank=True,
        null=True,
    )

    # === WHAT WAS CHANGED
    old_status = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Old status"),
    )
    new_status = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("New status"),
    )

    comment = models.TextField(
        blank=True,
        verbose_name=_("Comment"),
    )

    # === TIME
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Create at"),
        db_index=True,
    )

    class Meta:
        db_table = "order_log"
        verbose_name = _("Log a history of order")
        verbose_name_plural = _("Logs a history of orders")
        ordering = ["-create_at"]

    def __str__(self):
        return _(f"{self.order} - {self.new_status} ({self.create_at})")
