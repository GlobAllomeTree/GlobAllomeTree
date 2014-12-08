from django.core.management.base import BaseCommand
from globallometree.apps.taxonomy.models import Species, Family, Genus, SpeciesGroup
from globallometree.apps.allometric_equations.models import AllometricEquation, Submission
from globallometree.apps.allometric_equations.models import Population, Ecosystem
from globallometree.apps.locations.models import BiomeFAO, BiomeUdvardy, BiomeWWF, DivisionBailey, BiomeHoldridge
from globallometree.apps.locations.models import Location, Country, Continent, LocationGroup
from globallometree.apps.common.models import DataReference, Institution

class Command(BaseCommand):
    help = 'Cleans out all data from new normalized apps'

    def handle(self,*args, **options):
        AllometricEquation.objects.all().delete()
        Species.objects.all().delete()
        Genus.objects.all().delete()
        Family.objects.all().delete()
        SpeciesGroup.objects.all().delete()
        LocationGroup.objects.all().delete()
        Location.objects.all().delete()
        Population.objects.all().delete()
        Ecosystem.objects.all().delete()
        Submission.objects.all().delete()
        DataReference.objects.all().delete()
        Institution.objects.all().delete()
