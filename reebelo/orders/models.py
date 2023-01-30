import uuid

from django.db import models

from reebelo.core.models import TimestampedModel


class Order(TimestampedModel):
    PROCESSING = "processing"
    CANCELLED = "cancelled"
    DELIVERED = "delivered"

    STATUS_CHOICES = [
        (PROCESSING, "Processing"),
        (CANCELLED, "Cancelled"),
        (DELIVERED, "Delivered"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(
        max_length=128,
        choices=STATUS_CHOICES,
        help_text="Status of order",
        null=False,
        blank=False,
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="product",
        null=False,
        blank=False,
        help_text="Product associated with order",
    )
    quantity = models.IntegerField(null=False, blank=False, default=0)
    amount_per_unit = models.DecimalField(
        null=False, blank=False, decimal_places=2, max_digits=8, default=0.00
    )
    amount_total = models.DecimalField(
        null=False, blank=False, decimal_places=2, max_digits=8, default=0.00
    )
