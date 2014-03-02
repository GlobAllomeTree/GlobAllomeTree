from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from globallometree.apps.data.models import TreeEquation
from globallometree.apps.taxonomy.models import Species, Family, Genus, SpeciesGroup
from globallometree.apps.allometric_equations.models import AllometricEquation
from globallometree.apps.locations.models import BiomeFAO, BiomeUdvardy, BiomeWWF, DivisionBailey, BiomeHoldridge
from globallometree.apps.locations.models import Location, Country, Continent, LocationGroup

class Command(BaseCommand):
    help = 'Cleans out all data from new normalized apps'

    def handle(self,*args, **options):
        AllometricEquation.objects.all().delete()
        Species.objects.all().delete()
        Genus.objects.all().delete()
        Family.objects.all().delete()
        SpeciesGroup.objects.all().delete()
        BiomeFAO.objects.all().delete()
        BiomeUdvardy.objects.all().delete()
        BiomeWWF.objects.all().delete()
        DivisionBailey.objects.all().delete()
        BiomeHoldridge.objects.all().delete()
        LocationGroup.objects.all().delete()
        Location.objects.all().delete()
        Continent.objects.all().delete()
        Country.objects.all().delete()