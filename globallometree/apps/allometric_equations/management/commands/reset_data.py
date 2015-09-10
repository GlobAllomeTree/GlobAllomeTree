from django.conf import settings
from django.core.management.base import BaseCommand
from globallometree.apps.taxonomy.models import Subspecies, Species, Family, Genus, SpeciesGroup
from globallometree.apps.allometric_equations.models import AllometricEquation, Population
from globallometree.apps.locations.models import ZoneFAO, EcoregionUdvardy, EcoregionWWF, DivisionBailey, ZoneHoldridge
from globallometree.apps.locations.models import Location, Country, Continent, LocationGroup
from globallometree.apps.source.models import Reference, Institution
from globallometree.apps.data_sharing.models import Dataset
from globallometree.apps.identification.models import TreeType, VegetationType
from globallometree.apps.wood_densities.models import WoodDensity


class Command(BaseCommand):
    help = 'Cleans out all data from new normalized globallometree.apps'

    def handle(self,*args, **options):

        if not settings.DEBUG:
            print "Holy *&$#$, don't do it!"
            return

        AllometricEquation.objects.all().delete()
        WoodDensity.objects.all().delete()
        Subspecies.objects.all().delete()
        Species.objects.all().delete()
        Genus.objects.all().delete()
        Family.objects.all().delete()
        SpeciesGroup.objects.all().delete()
        LocationGroup.objects.all().delete()
        Location.objects.all().delete()
        Reference.objects.all().delete()
        Institution.objects.all().delete()
        WoodDensity.objects.all().delete()