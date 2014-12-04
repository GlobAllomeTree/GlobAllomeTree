from rest_framework import viewsets

from globallometree.apps.api.mixins import SimpleSerializerMixin

from globallometree.apps.common.models import (
    DataReference
	)

from globallometree.apps.data_sharing.models import (
    DataSharingAgreement, 
    DataSet, 
    DataAccessRequest
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
    SpeciesLocalNameSerializer,
	SubspeciesSerializer,
    SubspeciesLocalNameSerializer,
    SpeciesGroupSerializer,
	PopulationSerializer,
	EcosystemSerializer,
	ContinentSerializer,
	CountrySerializer,
	BiomeFAOSerializer, 
    BiomeUdvardySerializer, 
    BiomeWWFSerializer, 
    DivisionBaileySerializer, 
    BiomeHoldridgeSerializer,
    AllometricEquationSerializer,
    WoodDensitySerializer, 
    LocationSerializer,
    LocationGroupSerializer,
    DataSharingAgreementSerializer, 
    DataSetSerializer, 
    DataAccessRequestSerializer,
    SimpleGenusSerializer,
    SimpleFamilySerializer,
    SimpleSpeciesSerializer,
    SimpleAllometricEquationSerializer,
	)


class DataReferenceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = DataReference.objects.all()
    serializer_class = DataReferenceSerializer


class FamilyViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    simple_serializer_class = SimpleFamilySerializer


class GenusViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Genus.objects.all()
    serializer_class = GenusSerializer
    simple_serializer_class = SimpleGenusSerializer


class SpeciesViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    simple_serializer_class = SimpleSpeciesSerializer

class SubspeciesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Subspecies.objects.all()
    serializer_class = SubspeciesSerializer

class SpeciesGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = SpeciesGroup.objects.all()
    serializer_class = SpeciesGroupSerializer


class SpeciesLocalNameViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = SpeciesLocalName.objects.all()
    serializer_class = SpeciesLocalNameSerializer


class SubspeciesLocalNameViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = SubspeciesLocalName.objects.all()
    serializer_class = SubspeciesLocalNameSerializer


class PopulationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Population.objects.all()
    serializer_class = PopulationSerializer


class EcosystemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Ecosystem.objects.all()
    serializer_class = EcosystemSerializer


class ContinentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class BiomeFAOViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = BiomeFAO.objects.all()
    serializer_class = BiomeFAOSerializer


class BiomeUdvardyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = BiomeUdvardy.objects.all()
    serializer_class = BiomeUdvardySerializer


class BiomeWWFViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = BiomeWWF.objects.all()
    serializer_class = BiomeWWFSerializer


class DivisionBaileyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = DivisionBailey.objects.all()
    serializer_class = DivisionBaileySerializer


class BiomeHoldridgeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = BiomeHoldridge.objects.all()
    serializer_class = BiomeHoldridgeSerializer


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = LocationGroup.objects.all()
    serializer_class = LocationGroupSerializer


class AllometricEquationViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = AllometricEquation.objects.all()
    serializer_class = AllometricEquationSerializer
    simple_serializer_class = SimpleAllometricEquationSerializer

   
class WoodDensityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = WoodDensity.objects.all()
    serializer_class = WoodDensitySerializer


class DataSharingAgreementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = DataSharingAgreement.objects.all()
    serializer_class = DataSharingAgreementSerializer


class DataSetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer


class DataAccessRequestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = DataAccessRequest.objects.all()
    serializer_class = DataAccessRequestSerializer

