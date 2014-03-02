from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from globallometree.apps.data.models import TreeEquation
from globallometree.apps.taxonomy.models import Species, Family, Genus, SpeciesGroup

class Command(BaseCommand):
    help = 'Cleans out all data from new normalized apps'

    def handle(self,*args, **options):
        Species.objects.all().delete()
        Genus.objects.all().delete()
        Family.objects.all().delete()
        SpeciesGroup.objects.all().delete()
