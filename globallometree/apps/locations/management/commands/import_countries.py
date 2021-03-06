import os
import csv
import codecs

from django.db import transaction
from django.conf import settings
from django.core.management.base import BaseCommand

from globallometree.apps.locations.models import Country, Continent


class Command(BaseCommand):
    args = '<limit (optional)>'
    help = 'Imports from the old data.TreeEquation model to the new normalized structure'

    def handle(self,*args, **options):

        #First make sure we import all of the countries
        country_data = self.load_countries_csv()

        continents = {
            'AF' : 'Africa',
            'AN' : 'Antatica',
            'AS' : 'Asia',
            'EU' : 'Europe',
            'NA' : 'North America',
            'OC' : 'Oceania',
            'SA' : 'South America'
        }

        for key in continents.keys():
            name = continents[key]
            continents[key] = Continent.objects.get_or_create(Code=key, Name=name)[0]

        for cd_row in country_data:
            Country.objects.get_or_create(
                Common_name=cd_row['ISOen_name'],
                Formal_name=cd_row['ISOen_proper'],
                Common_name_fr=cd_row['ISOfr_name'],
                Formal_name_fr=cd_row['ISOfr_proper'],
                Continent=continents[cd_row['continent']],
                Iso3166a2=cd_row['ISO3166A2'],
                Iso3166a3=cd_row['ISO3166A3'],
                Iso3166n3=cd_row['ISO3166N3'],
                Centroid_latitude = cd_row['latitude'],
                Centroid_longitude = cd_row['longitude'] 
            )

    def load_countries_csv(self):
        #csv file with country lats/lons
        csv_file_path = os.path.join(settings.BASE_PATH, 'globallometree', 'apps', 'locations', 'resources', 'countries.csv')
        headers = []
        countries = []

        def clean(row):
            fields = row.replace('\r', '').replace('\n', '').replace(u'\ufeff','').split(';')
            fields = [v.strip() for v in fields]
            return fields

        with codecs.open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            for row in csv_file:
                if not len(headers):
                    headers = clean(row)
                    continue
                countries.append(dict(zip(headers, clean(row))))

        return countries
