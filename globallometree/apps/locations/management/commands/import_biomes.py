import os
import csv
import codecs

from django.db import transaction
from django.conf import settings
from django.core.management.base import BaseCommand

from globallometree.apps.locations.models import EcoregionUdvardy, ZoneFAO, EcoregionWWF, ZoneHoldridge, DivisionBailey

class Command(BaseCommand):
    args = '<limit (optional)>'
    help = 'Imports from the old data.TreeEquation model to the new normalized structure'

    def handle(self,*args, **options):
        data = self.load_csv('biomes_udvardy.csv')
        for row in data:
            EcoregionUdvardy.objects.create(
                pk = row['ID'], 
                Name = row['Name']
            )

        data = self.load_csv('biomes_fao.csv')
        for row in data:
            ZoneFAO.objects.create(
                pk = row['ID'], 
                Name = row['Name']
            )

        data = self.load_csv('biomes_wwf.csv')
        for row in data:
            EcoregionWWF.objects.create(
                pk = row['ID'], 
                Name = row['Name']
            )

        data = self.load_csv('biomes_holdridge.csv')
        for row in data:
            ZoneHoldridge.objects.create(
                pk = row['ID'], 
                Name = row['Name']
            )

        data = self.load_csv('division_bailey.csv')
        for row in data:
            DivisionBailey.objects.create(
                pk = row['ID'], 
                Name = row['Name']
            )

    def load_csv(self, file_name):
        #csv file with country lats/lons
        csv_file_path = os.path.join(settings.BASE_PATH, 'globallometree', 'apps', 'locations', 'resources', file_name)
        headers = []
        data = []

        def clean(row):
            fields = row.replace('\r', '').replace('\n', '').replace(u'\ufeff','').split(';')
            fields = [v.strip() for v in fields]
            return fields

        with codecs.open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            for row in csv_file:
                if not len(headers):
                    headers = clean(row)
                    continue
                data.append(dict(zip(headers, clean(row))))

        return data
