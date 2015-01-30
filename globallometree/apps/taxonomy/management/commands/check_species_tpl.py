import requests
import urllib
import unicodecsv as csv
from StringIO import StringIO

from django.conf import settings
from django.core.management.base import BaseCommand
from globallometree.apps.taxonomy.models import Subspecies, Species, Family, Genus, SpeciesGroup

class Command(BaseCommand):
    help = 'Runs through all species, families, genera, and subspecies \
            to chack them against the plant list'

    def handle(self,*args, **options):
        for sp in Species.objects.filter(TPL_Status=None):
            results = self.search(' '.join([sp.Genus.Name, sp.Name]))
            for row in results:
                if  row['Species'] == sp.Name and \
                    row['Genus'] == sp.Genus.Name and \
                    row['Family'] == sp.Genus.Family.Name:
                    sp.TPL_Status = row['Taxonomic status in TPL']
                    sp.TPL_ID = row['ID']
                    sp.TPL_Confidence_level = row['Confidence level']
                    sp.save()
                    print sp.Genus.Name, sp.Name, sp.TPL_ID
                    # We just want the one with the highest confidence
                    break
            if not sp.TPL_ID:
                print sp.Genus.Name, sp.Name, None 

            sleep(2)

    def search(self, query):
        params = urllib.urlencode({ 'q' : query, 'csv' : 1})
        url = 'http://www.theplantlist.org/tpl1.1/search?%s' % params
        request = requests.get(url)
        if request.status_code == 200:
            content = request.content.decode("utf-8-sig").encode("utf-8")
            data = csv.DictReader(StringIO(content))
            return data
        else:
            print 'Failed request (%s): %s' % (request.status_code, url)
            return []
        