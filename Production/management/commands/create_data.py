import json
import os
import random

from django.conf import settings
from django.core.management.base import BaseCommand

from Production.models import Crop, District, Region, RegionalPrices


List_crops = [
    {'name': 'Maize', 'crop_type': 'Food'},
    {'name': 'Sorghum', 'crop_type': 'Food'},
    {'name': 'Rice', 'crop_type': 'Food'},
    {'name': 'Wheat', 'crop_type': 'Food'},
    {'name': 'Barley', 'crop_type': 'Food'},
    {'name': 'Cassava', 'crop_type': 'Food'},
    {'name': 'Potatoes', 'crop_type': 'Food'},
    {'name': 'Sweet potatoes', 'crop_type': 'Food'},
    {'name': 'Beans', 'crop_type': 'Food'},
    {'name': 'Peas', 'crop_type': 'Food'},
    {'name': 'Bananas', 'crop_type': 'Food'},
    {'name': 'Pineapples', 'crop_type': 'Food'},
    {'name': 'Mangoes', 'crop_type': 'Food'},
    {'name': 'Oranges', 'crop_type': 'Food'},
    {'name': 'Grapes', 'crop_type': 'Food'},
    {'name': 'Tomatoes', 'crop_type': 'Food'},
    {'name': 'Onions', 'crop_type': 'Food'},
    {'name': 'Cabbages', 'crop_type': 'Food'},
    {'name': 'Carrots', 'crop_type': 'Food'},
    {'name': 'Spinach', 'crop_type': 'Food'},
    {'name': 'Pumpkins', 'crop_type': 'Food'},
    {'name': 'Eggplants', 'crop_type': 'Food'},
    {'name': 'Peppers', 'crop_type': 'Food'},
]


class Command(BaseCommand):
    help = 'Populates crops, regions, districts and regional market prices into the database.'

    def handle(self, *args, **options):

        # 1. Populate crops
        for c in List_crops:
            obj, created = Crop.objects.get_or_create(
                name=c['name'], defaults={'crop_type': c['crop_type']}
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Crop "{obj.name}" {"created" if created else "already exists"}.'
                )
            )

        # 2. Populate regions and their districts from the JSON file
        file_path = os.path.join(settings.BASE_DIR, 'Tanzania_regions.json')
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            for region_name, district_names in data.items():
                region, _ = Region.objects.get_or_create(name=region_name)
                for district_name in district_names:
                    district, _ = District.objects.get_or_create(name=district_name)
                    region.districts.add(district)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Region "{region_name}" populated with {len(district_names)} districts.'
                    )
                )

        # 3. Generate regional market prices for every crop in every region
        crops = Crop.objects.all()
        regions = Region.objects.all()
        added = 0
        for region in regions:
            for crop in crops:
                _, created = RegionalPrices.objects.get_or_create(
                    region=region,
                    crop=crop,
                    defaults={'price': float(random.randint(500, 5000))},
                )
                added += int(created)
        self.stdout.write(self.style.SUCCESS(f'Regional prices added: {added}.'))

        self.stdout.write(self.style.SUCCESS('Data population completed successfully.'))