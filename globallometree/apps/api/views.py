from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.api.permissions import IsOwnerOrReadOnly

from apps.api.mixins import NameQueryMixin

from apps.source.models import (
    Reference, 
    Institution
	)

from apps.data_sharing.models import (
    DataLicense, 
    Dataset, 
#    DataRequest
)

from apps.taxonomy.models import (
    Family, 
    Genus, 
    Species, 
    Subspecies, 
    SpeciesLocalName, 
    SpeciesGroup
	)

from apps.allometric_equations.models import (
    Population, 
    TreeType, 
    AllometricEquation
	)	

from apps.wood_densities.models import (
    WoodDensity
	)

from apps.raw_data.models import (
    RawData
    )

from apps.biomass_expansion_factors.models import (
    BiomassExpansionFactor
    )

from apps.locations.models import (
    Continent, 
    Country, 
    ZoneFAO, 
    EcoregionUdvardy, 
    EcoregionWWF, 
    DivisionBailey, 
    ZoneHoldridge, 
    LocationGroup, 
    Location, 
    ForestType,
	)

from apps.api.serializers import (
    AllometricEquationSerializer,
    PopulationSerializer,
    PopulationSerializer,
    ReferenceSerializer,
    WoodDensitySerializer,
    RawDataSerializer,
    InstitutionSerializer,
    BiomassExpansionFactorSerializer,
	)


from apps.api.serializers_data_sharing import (
    DataLicenseSerializer,
    DatasetSerializer,
    )

from apps.api.serializers_location import (
    ZoneFAOSerializer, 
    EcoregionUdvardySerializer, 
    EcoregionWWFSerializer, 
    DivisionBaileySerializer, 
    ZoneHoldridgeSerializer,
    ForestTypeSerializer,
    LocationSerializer,
    LocationGroupSerializer,
    ContinentSerializer,
    CountrySerializer,
    )


from apps.api.serializers_taxonomy import (
    GenusSerializer,
    FamilySerializer,
    SpeciesSerializer,
    SubspeciesSerializer,
    SpeciesLocalNameSerializer,
    SpeciesGroupSerializer,
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


class ZoneFAOViewSet(NameQueryMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = ZoneFAO.objects.all()
    serializer_class = ZoneFAOSerializer


class EcoregionUdvardyViewSet(NameQueryMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = EcoregionUdvardy.objects.all()
    serializer_class = EcoregionUdvardySerializer


class EcoregionWWFViewSet(NameQueryMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = EcoregionWWF.objects.all()
    serializer_class = EcoregionWWFSerializer


class DivisionBaileyViewSet(NameQueryMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = DivisionBailey.objects.all()
    serializer_class = DivisionBaileySerializer


class ZoneHoldridgeViewSet(NameQueryMixin, viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = ZoneHoldridge.objects.all()
    serializer_class = ZoneHoldridgeSerializer


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
