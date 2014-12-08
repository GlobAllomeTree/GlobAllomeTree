from rest_framework import viewsets

from globallometree.apps.api.mixins import SimpleSerializerMixin

from globallometree.apps.common.models import (
    DataReference, 
    Institution
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
    
	############## Full Serializers ##############
    DataReferenceSerializer,
    InstitutionSerializer,
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

    ############# Simple Serializers ################
    SimpleGenusSerializer,
    SimpleFamilySerializer,
    SimpleSpeciesSerializer,
    SimpleSubspeciesSerializer,
    SimpleSpeciesLocalNameSerializer,
    SimpleSubspeciesLocalNameSerializer,   
    SimpleAllometricEquationSerializer,
    SimpleSpeciesGroupSerializer,
    SimpleBiomeFAOSerializer, 
    SimpleBiomeUdvardySerializer, 
    SimpleBiomeWWFSerializer, 
    SimpleDivisionBaileySerializer, 
    SimpleBiomeHoldridgeSerializer,
    SimplePopulationSerializer,
    SimpleLocationSerializer,
    SimpleLocationGroupSerializer,
    SimpleContinentSerializer,
    SimpleCountrySerializer,
    SimpleDataReferenceSerializer,
    SimpleEcosystemSerializer,
    SimpleWoodDensitySerializer,
    SimpleInstitutionSerializer
	)


class DataReferenceViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = DataReference.objects.all()
    serializer_class = DataReferenceSerializer
    simple_serializer_class = SimpleDataReferenceSerializer


class InstitutionViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    simple_serializer_class = SimpleInstitutionSerializer


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


class SubspeciesViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Subspecies.objects.all()
    serializer_class = SubspeciesSerializer
    simple_serializer_class = SimpleSubspeciesSerializer


class SpeciesGroupViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = SpeciesGroup.objects.all()
    serializer_class = SpeciesGroupSerializer
    simple_serializer_class = SimpleSpeciesGroupSerializer


class SpeciesLocalNameViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = SpeciesLocalName.objects.all()
    serializer_class = SpeciesLocalNameSerializer
    simple_serializer_class = SimpleSpeciesLocalNameSerializer


class SubspeciesLocalNameViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = SubspeciesLocalName.objects.all()
    serializer_class = SubspeciesLocalNameSerializer
    simple_serializer_class = SimpleSubspeciesLocalNameSerializer


class PopulationViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Population.objects.all()
    serializer_class = PopulationSerializer
    simple_serializer_class = SimplePopulationSerializer


class EcosystemViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Ecosystem.objects.all()
    serializer_class = EcosystemSerializer
    simple_serializer_class = SimpleEcosystemSerializer


class ContinentViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer
    simple_serializer_class = SimpleContinentSerializer


class CountryViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    simple_serializer_class = SimpleCountrySerializer

class BiomeFAOViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = BiomeFAO.objects.all()
    serializer_class = BiomeFAOSerializer
    simple_serializer_class = SimpleBiomeFAOSerializer


class BiomeUdvardyViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = BiomeUdvardy.objects.all()
    serializer_class = BiomeUdvardySerializer
    simple_serializer_class = SimpleBiomeUdvardySerializer


class BiomeWWFViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = BiomeWWF.objects.all()
    serializer_class = BiomeWWFSerializer
    simple_serializer_class = SimpleBiomeWWFSerializer


class DivisionBaileyViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = DivisionBailey.objects.all()
    serializer_class = DivisionBaileySerializer
    simple_serializer_class = SimpleDivisionBaileySerializer


class BiomeHoldridgeViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = BiomeHoldridge.objects.all()
    serializer_class = BiomeHoldridgeSerializer
    simple_serializer_class = SimpleBiomeHoldridgeSerializer


class LocationViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    simple_serializer_class = SimpleLocationSerializer


class LocationGroupViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = LocationGroup.objects.all()
    serializer_class = LocationGroupSerializer
    simple_serializer_class = SimpleLocationGroupSerializer


class AllometricEquationViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = AllometricEquation.objects.all()
    serializer_class = AllometricEquationSerializer
    simple_serializer_class = SimpleAllometricEquationSerializer

   
class WoodDensityViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = WoodDensity.objects.all()
    serializer_class = WoodDensitySerializer
    simple_serializer_class = SimpleWoodDensitySerializer


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

