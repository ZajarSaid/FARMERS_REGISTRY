import json
from django.core.management.base import BaseCommand
from Production.models import Region, District, Crop
from django.conf import settings
import os
from django.utils import timezone
import random



class Command(BaseCommand):
    help = 'Creating sample region and districts data'

    # import crops

    def handle(self, *args, **kwargs):

        # populate crops

        List_crops = [
            
            {'name': 'Maize', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Sorghum', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Rice', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Wheat', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Barley', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Cassava', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Potatoes', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Sweet potatoes', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Beans', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Peas', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Bananas', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Pineapples', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Mangoes', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Oranges', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Grapes', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Tomatoes', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Onions', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Cabbages', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Carrots', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Spinach', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Pumpkins', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Eggplants', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
            {'name': 'Peppers', 'crop_type': 'Food', 'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 365))},
        ]

        for c in List_crops:
            Crop.objects.create(**c)

        crops = Crop.objects.all()

        


    
    # Populate Region model with data from  JSON file

    # def handle(self, *args, **kwargs):
    #     File_path = os.path.join(settings.BASE_DIR, 'Tanzania_regions.json')

    #     with open(File_path, 'r') as json_file:
    #         data = json.load(json_file)
    #         for region_name, district_names in data.items():
    #             region, created = Region.objects.get_or_create(name=region_name)
    #             for district_name in district_names:
    #                 district, created = District.objects.get_or_create(name=district_name)
    #                 region.districts.add(district)
    #             self.stdout.write(self.style.SUCCESS(f'Region "{region_name}" populated with districts.'))
