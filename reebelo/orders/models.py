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
