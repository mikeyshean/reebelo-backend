import json
import logging
import random
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from reebelo.products.models import Product

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, **options):
        """
        Seed database with cpu_hours.csv data
        """

        base_path = Path(__file__).parent
        file_path = (base_path / "devices.json").resolve()

        with open(file_path, newline="") as jsonfile:
            data = json.load(jsonfile)
            devices = data["RECORDS"]
            batch = []
            count_batch_items = 0
            count_total_processed = 0
            for device in devices:
                try:
                    batch.append(
                        Product(
                            name=device["name"],
                            price=round(random.uniform(200.00, 2000.00), 2),
                            quantity=random.randint(0, 2000),
                        )
                    )
                    count_batch_items += 1
                    if count_batch_items % 1000 == 0:
                        products = Product.objects.bulk_create(
                            batch, 1000, ignore_conflicts=True
                        )
                        batch = []
                        count_batch_items = 0
                        count_total_processed += len(products)
                        print(f"Total process: {count_total_processed}...")
                except IntegrityError:
                    print("ignore, just seed anything")
