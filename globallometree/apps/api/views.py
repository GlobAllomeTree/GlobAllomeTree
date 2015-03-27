from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from globallometree.apps.api.permissions import IsOwnerOrReadOnly

from globallometree.apps.api.mixins import SimpleSerializerMixin, NameQueryMixin

from globallometree.apps.source.models import (
    Reference, 
    Institution
	)

from globallometree.apps.data_sharing.models import (
    DataLicense, 
    Dataset, 
    DataRequest
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
    TreeType, 
    AllometricEquation
	)	

from globallometree.apps.wood_densities.models import (
    WoodDensity
	)

from globallometree.apps.raw_data.models import (
    RawData
    )

from globallometree.apps.biomass_expansion_factors.models import (
    BiomassExpansionFactor
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
    Location, 
    Plot,
    ForestType,
	)

from globallometree.apps.api.serializers import (
    
	############## Full Serializers ##############
    ReferenceSerializer,
    InstitutionSerializer,
	FamilySerializer,
	GenusSerializer,
	SpeciesSerializer,
    SpeciesLocalNameSerializer,
	SubspeciesSerializer,
    SubspeciesLocalNameSerializer,
    SpeciesGroupSerializer,
	PopulationSerializer,
	ContinentSerializer,
	CountrySerializer,
    ForestTypeSerializer,
	BiomeFAOSerializer, 
    BiomeUdvardySerializer, 
    BiomeWWFSerializer, 
    DivisionBaileySerializer, 
    BiomeHoldridgeSerializer,
    AllometricEquationSerializer,
    WoodDensitySerializer,
    RawDataSerializer,
    PlotSerializer, 
    LocationSerializer,
    LocationGroupSerializer,
    DataLicenseSerializer, 
    DatasetSerializer, 
    DataRequestSerializer,
    BiomassExpansionFactorSerializer,

    ############# Simple Serializers ################
    SimpleGenusSerializer,
    SimpleFamilySerializer,
    SimpleSpeciesSerializer,
    SimpleSubspeciesSerializer,
    SimpleSpeciesLocalNameSerializer,
    SimpleSubspeciesLocalNameSerializer,   
    SimpleAllometricEquationSerializer,
    SimpleSpeciesGroupSerializer,
    SimpleForestTypeSerializer,
    SimpleBiomeFAOSerializer, 
    SimpleBiomeUdvardySerializer, 
    SimpleBiomeWWFSerializer, 
    SimpleDivisionBaileySerializer, 
    SimpleBiomeHoldridgeSerializer,
    SimplePopulationSerializer,
    SimplePlotSerializer, 
    SimpleLocationSerializer,
    SimpleLocationGroupSerializer,
    SimpleContinentSerializer,
    SimpleCountrySerializer,
    SimpleReferenceSerializer,
    SimpleWoodDensitySerializer,
    SimpleRawDataSerializer,
    SimpleInstitutionSerializer,
    SimpleDatasetSerializer,
    SimpleDataLicenseSerializer,
    SimpleBiomassExpansionFactorSerializer,
	)


class ReferenceViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    simple_serializer_class = SimpleReferenceSerializer


class InstitutionViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    simple_serializer_class = SimpleInstitutionSerializer


class FamilyViewSet(NameQueryMixin, SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    simple_serializer_class = SimpleFamilySerializer


class GenusViewSet(NameQueryMixin, SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Genus.objects.all()
    serializer_class = GenusSerializer
    simple_serializer_class = SimpleGenusSerializer


class SpeciesViewSet(NameQueryMixin, SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    simple_serializer_class = SimpleSpeciesSerializer


class SubspeciesViewSet(NameQueryMixin, SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
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


class ForestTypeViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = ForestType.objects.all()
    serializer_class = ForestTypeSerializer
    simple_serializer_class = SimpleForestTypeSerializer


class BiomeFAOViewSet(NameQueryMixin, SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = BiomeFAO.objects.all()
    serializer_class = BiomeFAOSerializer
    simple_serializer_class = SimpleBiomeFAOSerializer


class BiomeUdvardyViewSet(NameQueryMixin, SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = BiomeUdvardy.objects.all()
    serializer_class = BiomeUdvardySerializer
    simple_serializer_class = SimpleBiomeUdvardySerializer


class BiomeWWFViewSet(NameQueryMixin, SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = BiomeWWF.objects.all()
    serializer_class = BiomeWWFSerializer
    simple_serializer_class = SimpleBiomeWWFSerializer


class DivisionBaileyViewSet(NameQueryMixin, SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = DivisionBailey.objects.all()
    serializer_class = DivisionBaileySerializer
    simple_serializer_class = SimpleDivisionBaileySerializer


class BiomeHoldridgeViewSet(NameQueryMixin, SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
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


class PlotViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Plot.objects.all()
    serializer_class = PlotSerializer
    simple_serializer_class = SimplePlotSerializer


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


class RawDataViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = RawData.objects.all()
    serializer_class = RawDataSerializer
    simple_serializer_class = SimpleRawDataSerializer


class DataLicenseViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = DataLicense.objects.all()
    serializer_class = DataLicenseSerializer
    simple_serializer_class = SimpleDataLicenseSerializer


class DatasetViewSet(SimpleSerializerMixin, viewsets.ModelViewSet):
    """
        Users are able to create or edit their own datasets through the API
    """
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    simple_serializer_class = SimpleDatasetSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


class DataRequestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = DataRequest.objects.all()
    serializer_class = DataRequestSerializer


class BiomassExpansionFactorViewSet(SimpleSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = BiomassExpansionFactor.objects.all()
    serializer_class = BiomassExpansionFactorSerializer
    simple_serializer_class = SimpleBiomassExpansionFactorSerializer
