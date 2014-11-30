from rest_framework import viewsets

from globallometree.apps.common.models import (
    DataReference
	)

from globallometree.apps.taxonomy.models import (
    Family, 
    Genus, 
    Species, 
    Subspecies, 
    SpeciesLocalName, 
    SubspeciesLocalName, 
    SpeciesGroup
	)

from globallometree.apps.allometric_equations.models import (
    Population, 
    Ecosystem, 
    Submission, 
    AllometricEquation
	)	

from globallometree.apps.wood_densities.models import (
    WoodDensity
	)

from globallometree.apps.locations.models import (
    Continent, 
    Country, 
    BiomeFAO, 
    BiomeUdvardy, 
    BiomeWWF, 
    DivisionBailey, 
    BiomeHoldridge, 
    LocationGroup, 
    Location
	)

from globallometree.apps.api.serializers import (
	DataReferenceSerializer,
	FamilySerializer,
	GenusSerializer,
	SpeciesSerializer,
	SubspeciesSerializer,
	PopulationSerializer,
	EcosystemSerializer,
	ContinentSerializer,
	CountrySerializer,
	BiomeFAOSerializer, 
    BiomeUdvardySerializer, 
    BiomeWWFSerializer, 
    DivisionBaileySerializer, 
    BiomeHoldridgeSerializer
	)


class DataReferenceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Scientific references from journals
    """
    queryset = DataReference.objects.all()
    serializer_class = DataReferenceSerializer


class FamilyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing families.
    """
    queryset = Family.objects.all()
    serializer_class = FamilySerializer


class GenusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing genera.
    """
    queryset = Genus.objects.all()
    serializer_class = GenusSerializer


class SpeciesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing species.
    """
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer

class SubspeciesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing subspecies.
    """
    queryset = Subspecies.objects.all()
    serializer_class = SubspeciesSerializer

class PopulationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing populations.
    """
    queryset = Population.objects.all()
    serializer_class = PopulationSerializer

class EcosystemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing ecosystems.
    """
    queryset = Ecosystem.objects.all()
    serializer_class = EcosystemSerializer

class ContinentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing continents.
    """
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing countries.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class BiomeFAOViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing fao biomes.
    """
    queryset = BiomeFAO.objects.all()
    serializer_class = BiomeFAOSerializer


class BiomeUdvardyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing udvardy biomes.
    """
    queryset = BiomeUdvardy.objects.all()
    serializer_class = BiomeUdvardySerializer


class BiomeWWFViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing wwf biomes.
    """
    queryset = BiomeWWF.objects.all()
    serializer_class = BiomeWWFSerializer


class DivisionBaileyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing countries.
    """
    queryset = DivisionBailey.objects.all()
    serializer_class = DivisionBaileySerializer


class BiomeHoldridgeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing countries.
    """
    queryset = BiomeHoldridge.objects.all()
    serializer_class = BiomeHoldridgeSerializer

