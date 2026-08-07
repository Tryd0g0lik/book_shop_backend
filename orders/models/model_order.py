# order/models/model_order.py:1

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import (
    EmailValidator,
    MaxLengthValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

Users = get_user_model()


class OrderModel(models.Model):
    """
    Order model.
    This model is fixing all data about the steps wit   h successful orders
    """

    # === STATUS OF ORDER
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending pay")
        PAID = "paid", _("Paid")
        PROCESSING = "processing", _("In processing")
        SHIPPED = "shipped", _("Shipped")
        DELIVERED = "delivered", _("Delivered")
        CANCELLED = "cancelled", _("Cancelled")
        REFUNDED = "refunded", _("Refunded")

    # === METHODS OF PAY
    class PaymentMethod(models.TextChoices):
        CARD = "card", _("Card")
        PAYPAL = "paypal", _("PayPal")
        CRYPTO = "crypto", _("Crypto")
        BANK = "bank", _("Bank")
        CASH = "cash", _("Many upon receipt")
        ROBOKASSA = "robokassa", _("Robokassa")
        UMONEY = "UMoney", _("ЮMoney")

    # === BASIS FIELDS
    # profile = models.ForeignKey(
    #     "profiles.UserProfile",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="+",
    #     verbose_name=_("Profile"),
    # )
    profile = models.PositiveIntegerField(
        verbose_name=_("Profile ID"),
        blank=True,
        null=True,
    )
    # === INFO ABOUT THE OWNER OF THE ORDER
    customer_email = models.EmailField(
        verbose_name=_("Customer Email"),
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-][a-zA-Z0-9]?)?$"
            ),
            EmailValidator(),
        ],
        blank=True,
        null=True,
        db_index=True,
    )
    customer_phone = models.CharField(
        verbose_name=_("Customer Phone"),
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^(\+?\d{1,3}[\s\-]?)?\(?\d{2,5}\)?[\s\-]?\d{3,4}[\s\-]?\d{3,4}$"
            ),
            MaxLengthValidator(20),
        ],
        blank=True,
    )
    customer_name = models.CharField(
        max_length=50,
        verbose_name=_("Name of client"),
        validators=[
            RegexValidator(
                regex=r"(^[A-ZА-ЯЁ][a-zа-яё]+(?:[-\s][A-ZА-ЯЁ][a-zа-яЁ]+)*)$"
            ),
            MaxLengthValidator(50),
            MinLengthValidator(5),
        ],
        blank=True,
    )
    # === ADDRESS OF DELIVERY
    shipping_address = models.TextField(
        verbose_name=_("Address"),
    )
    shipping_city = models.CharField(
        verbose_name=_("City"),
    )
    shipping_country = models.CharField(
        verbose_name=_("Country"),
        default=_("Russia"),
    )
    # === FINANCE
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Amount without discount"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Discount"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    shipping_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Shipping cost"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    tax = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Tax"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Total sum"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    # === PAYMENT STATUS
    status = models.CharField(
        verbose_name=_("Status payment"),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.BANK,
        verbose_name=_("Payment Method"),
    )
    payment_status = models.CharField(
        verbose_name=_("Payment Method"),
        max_length=20,
        choices=[
            ("pending", _("Pending")),
            ("success", _("Success")),
            ("failed", _("Failed")),
            ("refunded", _("Refunded")),
        ],
        default="pending",
        db_index=True,
    )
    # === DATA OF PAYMENT
    payment_id = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Payment ID"),
        db_index=True,
    )
    payment_date = models.DateTimeField(
        verbose_name=_("Payment Date"),
        blank=True,
        null=True,
    )
    # === ADDITIONAL INFO
    comment = models.TextField(blank=True, null=True, verbose_name=_("Comment"))
    admin_comment = models.TextField(
        blank=True, null=True, verbose_name=_("Admin comment")
    )

    # === TRACKING
    tracking_number = models.CharField(
        verbose_name=_("Tracking Number"),
        max_length=100,
        blank=True,
        db_index=True,
    )
    delivery_company = models.CharField(
        verbose_name=_("Delivery Company"),
        max_length=100,
        blank=True,
    )
    # === DATA OF HISTORY
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("IP Address of client"),
    )
    user_aget = models.TextField(
        blank=True,
        verbose_name=_("User-Aget"),
    )

    # DATETIME MARK
    created_at = models.DateTimeField(
        # auto_now_add=True,
        default=timezone.now,
        verbose_name=_("Created Date"),
        db_index=True,
    )
    update_at = models.DateTimeField(
        verbose_name=_("Updated Date"),
        db_index=True,
        default=timezone.now,
    )
    completed_at = models.DateTimeField(
        blank=True,
        verbose_name=_("Completed Date"),
        db_index=True,
        null=True,
    )

    class Meta:
        db_table = "orders"
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ["-created_at"]
        indexes = [
            # models.Index(fields=["profile_id", "created_at"]),
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["payment_status", "created_at"]),
        ]

    def __str__(self):
        return _(f"Order #{self.pk} - {self.customer_name or self.customer_email}")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.total = self.subtotal - self.discount + self.shipping_cost + self.tax

        # If a payment's status is a paid
        if self.status == self.Status.PAID and not self.payment_date:
            self.payment_date = timezone.now()

        # If status is a delivered
        if (
            self.status in [self.Status.DELIVERED, self.Status.CANCELLED]
            and not self.completed_at
        ):
            self.completed_at = timezone.now()

        super().save(*args, **kwargs)

    def get_total_items(self):
        """Total quantity of items in order"""
        return self.items.aggregate(total=models.Sum("quantity"))["total"] or 0

    def can_be_cancelled(self):
        """ "Can we cansel this order or not"""
        return self.status in [
            self.Status.PENDING,
            self.Status.PAID,
            self.Status.PROCESSING,
        ]

    def mark_as_paid(self, payment_id=None):
        """Mark this order us paid"""
        self.status = self.Status.PAID
        self.payment_status = "success"
        if payment_id:
            self.payment_id = payment_id

        self.payment_date = timezone.now()
        self.save()
