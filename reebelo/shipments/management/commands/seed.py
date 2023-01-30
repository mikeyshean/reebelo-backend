from django.core.management.base import BaseCommand
from django.db import transaction

from reebelo.shipments.models import TrackingCompany


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, **options):
        if TrackingCompany.objects.count() == 0:
            tracking_companies = ["DHL", "UPS", "FedEx", "Standard Mail Carrier"]
            for item in tracking_companies:
                TrackingCompany.objects.create(name=item)
