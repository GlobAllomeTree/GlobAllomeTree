from django.core.management.base import BaseCommand
from globallometree.apps.taxonomy.models import Species, Family, Genus, SpeciesGroup
from globallometree.apps.allometric_equations.models import AllometricEquation, AllometricEquationSubmission
from globallometree.apps.allometric_equations.models import AllometricEquationPopulation, AllometricEquationEcosystem
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
        BiomeFAO.objects.all().delete()
        BiomeUdvardy.objects.all().delete()
        BiomeWWF.objects.all().delete()
        DivisionBailey.objects.all().delete()
        BiomeHoldridge.objects.all().delete()
        LocationGroup.objects.all().delete()
        Location.objects.all().delete()
        Continent.objects.all().delete()
        Country.objects.all().delete()
        AllometricEquationPopulation.objects.all().delete()
        AllometricEquationEcosystem.objects.all().delete()
        AllometricEquationSubmission.objects.all().delete()
        DataReference.objects.all().delete()
        Institution.objects.all().delete()