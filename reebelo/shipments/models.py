import uuid

from django.db import models

from reebelo.core.models import TimestampedModel


class TrackingCompany(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=128,
        help_text="Name of tracking company provider",
        null=True,
        blank=False,
        default=None,
        unique=True,
    )


class Shipment(TimestampedModel):
    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="order",
        null=False,
        blank=False,
        help_text="Order associated with shipment",
        primary_key=True,
    )
    tracking_number = models.CharField(
        max_length=128,
        help_text="Tracking number for order",
        null=True,
        blank=False,
        default=None,
    )
    tracking_company = models.ForeignKey(
        "TrackingCompany",
        on_delete=models.PROTECT,
        related_name="tracking_company",
        null=True,
        blank=False,
        default=None,
        help_text="Tracking company associated with shipment",
    )
    recipient_name = models.CharField(
        max_length=128,
        help_text="Full name of order recipient",
        null=True,
        blank=False,
        default=None,
    )
