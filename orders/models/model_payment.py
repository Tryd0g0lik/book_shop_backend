from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from orders.models.model_order import OrderModel


class PaymentModel(models.Model):
    """
    Model for payment details (about transaction)
    """

    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        SUCCESS = "success", _("Success")
        FAILED = "failed", _("Failed")
        REFUNDED = "refunded", _("Refunded")
        CANCELED = "canceled", _("Canceled")

    class Method(models.TextChoices):
        CARD = "card", _("Card")
        PAYPAL = "paypal", _("PayPal")
        CRYPTO = "crypto", _("Crypto")
        BANK = "bank", _("Bank")
        CASH = "cash", _("Many upon receipt")
        ROBOKASSA = "robokassa", _("Robokassa")
        UMONEY = "UMoney", _("ЮMoney")

    class UE(models.TextChoices):
        RUB = "RUB", _("Rub")
        EUR = "EUR", _("EUR")
        DOLLAR = "DOL", _("Dollar")

    order = models.ForeignKey(
        "orders.OrderModel",
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("Order"),
        db_index=True,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_("Amount"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    currency = models.CharField(
        max_length=3,
        default=UE.RUB,
        choices=UE.choices,
        verbose_name=_("Currency"),
    )
    method = models.CharField(
        max_length=20,
        choices=Method.choices,
        default=Method.CARD,
        verbose_name=_("Payment Method"),
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("Payment Status"),
        db_index=True,
    )

    # === EXTERNAL INDEXES
    payment_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Payment ID"),
        db_index=True,
    )
    provider = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name=_("Provide of payment"),
        help_text=_("Example: YooKassa, Stripe, Robokassa"),
    )

    # DATA OF A CARD (only lass of 4 numbers)
    card_last4 = models.CharField(
        max_length=4,
        blank=True,
        default="",
        verbose_name=_("Card Last 4 numbers"),
    )
    card_brand = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name=_("Card Brand"),
    )

    request_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Request Data"),
    )
    response_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Response Data"),
    )

    # TIMES OF MARK
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
        db_index=True,
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Paid at"),
    )
    refunded_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Refunded at"),
    )

    class Meta:
        db_table = "order_payment"
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order", "status"]),
            models.Index(fields=["payment_id"]),
        ]

    def __str__(self):
        return f"{self.method} - {self.amount} {self.currency} ({self.status})"

    def mark_as_success(self):
        """Mark payment as successfully paid"""
        self.status = self.Status.SUCCESS
        self.paid_at = timezone.now()
        self.save()

        self.order.mark_as_paid(self.payment_id)

    def mark_as_failed(self, error_message=None):
        self.status = self.Status.FAILED
        if error_message:
            self.response_data["error"] = error_message
        self.save()

    def refund(self):
        self.status = self.Status.REFUNDED
        self.refunded_at = timezone.now()
        self.save()

        self.order.status = OrderModel.Status.REFUNDED
        self.order.save()
