from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from globallometree.apps.api.permissions import IsOwnerOrReadOnly

from globallometree.apps.api.mixins import NameQueryMixin

from globallometree.apps.source.models import (
    Reference, 
    Institution
	)

from globallometree.apps.data_sharing.models import (
    DataLicense, 
    Dataset, 
#    DataRequest
)

from globallometree.apps.taxonomy.models import (
    Family, 
    Genus, 
    Species, 
    Subspecies, 
    SpeciesLocalName, 
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
    ForestType,
	)

from globallometree.apps.api.serializers import (
    
    GenusSerializer,
    FamilySerializer,
    SpeciesSerializer,
    SubspeciesSerializer,
    SpeciesLocalNameSerializer,
    AllometricEquationSerializer,
    SpeciesGroupSerializer,
    ForestTypeSerializer,
    BiomeFAOSerializer, 
    BiomeUdvardySerializer, 
    BiomeWWFSerializer, 
    DivisionBaileySerializer, 
    BiomeHoldridgeSerializer,
    PopulationSerializer,
    LocationSerializer,
    LocationGroupSerializer,
    ContinentSerializer,
    CountrySerializer,
    ReferenceSerializer,
    WoodDensitySerializer,
    RawDataSerializer,
    InstitutionSerializer,
    DatasetSerializer,
    DataLicenseSerializer,
    BiomassExpansionFactorSerializer,
	)



class ReferenceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer


class InstitutionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class FamilyViewSet(NameQueryMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Family.objects.all()
    serializer_class = FamilySerializer


class GenusViewSet(NameQueryMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Genus.objects.all()
    serializer_class = GenusSerializer


class SpeciesViewSet(NameQueryMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer


class SubspeciesViewSet(NameQueryMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Subspecies.objects.all()
    serializer_class = SubspeciesSerializer


class SpeciesGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = SpeciesGroup.objects.all()
    serializer_class = SpeciesGroupSerializer


class SpeciesLocalNameViewSet(NameQueryMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = SpeciesLocalName.objects.all()
    serializer_class = SpeciesLocalNameSerializer


class PopulationViewSet(NameQueryMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Population.objects.all()
    serializer_class = PopulationSerializer


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


class ForestTypeViewSet(NameQueryMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = ForestType.objects.all()
    serializer_class = ForestTypeSerializer


class BiomeFAOViewSet(NameQueryMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = BiomeFAO.objects.all()
    serializer_class = BiomeFAOSerializer


class BiomeUdvardyViewSet(NameQueryMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = BiomeUdvardy.objects.all()
    serializer_class = BiomeUdvardySerializer


class BiomeWWFViewSet(NameQueryMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = BiomeWWF.objects.all()
    serializer_class = BiomeWWFSerializer


class DivisionBaileyViewSet(NameQueryMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = DivisionBailey.objects.all()
    serializer_class = DivisionBaileySerializer


class BiomeHoldridgeViewSet(NameQueryMixin, viewsets.ReadOnlyModelViewSet):
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


class AllometricEquationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = AllometricEquation.objects.all()
    serializer_class = AllometricEquationSerializer

   
class WoodDensityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = WoodDensity.objects.all()
    serializer_class = WoodDensitySerializer


class RawDataViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = RawData.objects.all()
    serializer_class = RawDataSerializer


class DataLicenseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = DataLicense.objects.all()
    serializer_class = DataLicenseSerializer


class DatasetViewSet(viewsets.ModelViewSet):
    """
        Users are able to create or edit their own datasets through the API
    """
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


# class DataRequestViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     """
#     queryset = DataRequest.objects.all()
#     serializer_class = DataRequestSerializer


class BiomassExpansionFactorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = BiomassExpansionFactor.objects.all()
    serializer_class = BiomassExpansionFactorSerializer
