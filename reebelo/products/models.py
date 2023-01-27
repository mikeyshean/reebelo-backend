import uuid
from reebelo.core.models import TimestampedModel
from django.db import models

class Product(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, help_text="Name of product", unique=True)
    price = models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=8)
    quantity = models.IntegerField(null=False, blank=False, default=0)