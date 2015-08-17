import os
import sys
import csv
import codecs

from time import sleep
from django.conf import settings
from django.core.management.base import BaseCommand

from pygeocoder import Geocoder
from pygeolib import GeocoderError

from apps.accounts.models import UserProfile
from apps.locations.models import Country

class Command(BaseCommand):
    args = '<limit (optional)>'
    help = 'Imports from the old data.TreeEquation model to the new normalized structure'

    def get_country_code(self, geocodes):
        for component in geocodes.raw[0]['address_components']:
            if 'country' in component['types']: 
                return component['short_name']

    def handle(self,*args, **options):

        if len(args) == 1:
            limit = int(args[0])
        elif len(args) > 1:
            exit('Command only takes one argument <limit>')
        else:
            limit = 0

        n = 0
       

        for profile in UserProfile.objects.filter(location_latitude=None).iterator():
            if limit and n > limit: break;
            n = n + 1; 

            #First try the user provided address

            list_1 = [profile.address, 
                                   profile.subregion, 
                                   profile.region, 
                                   profile.country]

            geostring_1 = ', '.join([i for i in list_1 if i != ''])

            #Failing that, try the organisation address
            list_2 = [ profile.institution_address, 
                       profile.country]

            geostring_2 = ', '.join([i for i in list_2 if i != ''])

            #Otherwise, just try to geocode the country
            geostring_3 = profile.country

            try:
                geocodes = Geocoder.geocode(geostring_1)
                sleep(1)
            except GeocoderError:
                try:
                    geocodes = Geocoder.geocode(geostring_2)
                    sleep(1)
                except GeocoderError:
                    try:
                        geocodes = Geocoder.geocode(geostring_3)
                        sleep(1)
                    except GeocoderError:
                        print "Profile id %s - No results for '%s' or for '%s' " % (profile.pk, geostring_1, geostring_2)
                        continue
                   
            country_code = self.get_country_code(geocodes)
            latitude = geocodes.raw[0]['geometry']['location']['lat']
            longitude = geocodes.raw[0]['geometry']['location']['lng']


            print latitude, longitude, country_code

            try: 
                country = Country.objects.get(Iso3166a2=country_code)
                profile.location_country = country
            except Country.DoesNotExist:
                print "Profile id %s - No results for country %s" % (profile.pk, country_code)

            profile.location_latitude = str(latitude)
            profile.location_longitude = str(longitude)
            

            profile.save()

# #(Pdb) pp geocode.raw[0]
# {u'address_components': [{u'long_name': u'Meurthe-et-Moselle',
#                           u'short_name': u'54',
#                           u'types': [u'administrative_area_level_2',
#                                      u'political']},
#                          {u'long_name': u'Lorraine',
#                           u'short_name': u'Lorraine',
#                           u'types': [u'administrative_area_level_1',
#                                      u'political']},
#                          {u'long_name': u'France',
#                           u'short_name': u'FR',
#                           u'types': [u'county', u'political']}],
#  u'formatted_address': u'Meurthe-et-Moselle, France',
#  u'geometry': {u'bounds': {u'northeast': {u'lat': 49.56326800000001,
#                                           u'lng': 7.123213100000001},
#                            u'southwest': {u'lat': 48.348987,
#                                           u'lng': 5.426108}},
#                u'location': {u'lat': 48.7997007, u'lng': 6.094701400000001},
#                u'location_type': u'APPROXIMATE',
#                u'viewport': {u'northeast': {u'lat': 49.56326800000001,
#                                             u'lng': 7.123213100000001},
#                              u'southwest': {u'lat': 48.348987,
#                                             u'lng': 5.426108}}},
#  u'partial_match': True,
#  u'types': [u'administrative_area_level_2', u'political']}