## api/views.py
from django.contrib.auth.models import User

from rest_framework import serializers, fields

from globallometree.apps.common.models import (
    DataReference
)

from globallometree.apps.allometric_equations.models import (
    Population, 
    Ecosystem, 
    Submission, 
    AllometricEquation
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


class HyperLinkedWithIdSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(HyperLinkedWithIdSerializer, self).__init__(*args, **kwargs)
        self.fields[self.Meta.model._meta.pk.name] = fields.IntegerField()


class DataReferenceSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = DataReference
        #exclude = ('created', 'modified',)


class FamilySerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = Family
        exclude = ('created', 'modified',)


class GenusSerializer(HyperLinkedWithIdSerializer):
    family = FamilySerializer(many=False)

    class Meta:
        model = Genus
        exclude = ('created', 'modified',)


class SpeciesLocalNameSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = SpeciesLocalName
        exclude = ('created', 'modified',)
             

class SpeciesSerializer(HyperLinkedWithIdSerializer):
    genus = GenusSerializer(many=False)
    local_names = SpeciesLocalNameSerializer(many=True)
    class Meta:
        model = Species
        exclude = ('created', 'modified', 'original_ID_Species')


class SubspeciesLocalNameSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = SubspeciesLocalName
        exclude = ('created', 'modified',)


class SubspeciesSerializer(HyperLinkedWithIdSerializer):
    species = SpeciesSerializer(many=False)
    local_names = SubspeciesLocalNameSerializer(many=True)
    class Meta:
        model = Subspecies
        exclude = ('created', 'modified',)


class SpeciesGroupSerializer(HyperLinkedWithIdSerializer):
    subspecies = SubspeciesSerializer(many=True) 
    species = SpeciesSerializer(many=True)
    class Meta:
        model = SpeciesGroup
        exclude = ('created', 'modified', 'original_ID_Group')


class PopulationSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = Population
        #exclude = ('created', 'modified',)


class EcosystemSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = Ecosystem
        #exclude = ('created', 'modified',)


class ContinentSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = Continent
        exclude = ('created', 'modified',)


class CountrySerializer(HyperLinkedWithIdSerializer):
    continent = ContinentSerializer(many=False)
    class Meta:
        model = Country
        exclude = ('created', 'modified',)


class BiomeFAOSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = BiomeFAO
        exclude = ('created', 'modified',)


class BiomeUdvardySerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = BiomeUdvardy
        exclude = ('created', 'modified',)


class BiomeWWFSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = BiomeWWF
        exclude = ('created', 'modified',)


class DivisionBaileySerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = DivisionBailey
        exclude = ('created', 'modified',)


class BiomeHoldridgeSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = BiomeHoldridge
        exclude = ('created', 'modified',)


class LocationSerializer(HyperLinkedWithIdSerializer):
    biome_fao = BiomeFAOSerializer(many=False)
    biome_udvardy = BiomeUdvardySerializer(many=False)
    biome_wwf = BiomeWWFSerializer(many=False)
    division_bailey = DivisionBaileySerializer(many=False)
    biome_holdridge = BiomeHoldridgeSerializer(many=False)
    country = CountrySerializer(many=False)
    class Meta:
        model = Location
        exclude = ('created', 'modified', 'original_ID_Location')


class LocationGroupSerializer(HyperLinkedWithIdSerializer):
    locations = LocationSerializer(many=True)
    class Meta:
        model = LocationGroup    
        exclude = ('created', 'modified', 'original_Group_Location')


class AllometricEquationSerializer(HyperLinkedWithIdSerializer):
    species_group = SpeciesGroupSerializer(many=False)
    location_group = LocationGroupSerializer(many=False)
    population = PopulationSerializer(many=False) 
    ecosystem = EcosystemSerializer(many=False)
    reference = DataReferenceSerializer(many=False)
    class Meta:
        model = AllometricEquation
        exclude = ('created', 'ID_REF')


class WoodDensitySerializer(HyperLinkedWithIdSerializer):
    species = SpeciesSerializer(many=False)
    subspecies = SubspeciesSerializer(many=False)
    population = PopulationSerializer(many=False) 
    ecosystem = EcosystemSerializer(many=False)
    reference = DataReferenceSerializer(many=False)
    class Meta:
        model = AllometricEquation
        exclude = ('created',)


class DataSharingAgreementSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = DataSharingAgreement


class DataSetSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = DataSet


class DataAccessRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataAccessRequest



########################################################################
#############   SIMPLE SERIALIZERS #####################################
########################################################################


class SimpleSpeciesLocalNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeciesLocalName
        fields = ('local_name', )

class SimpleFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ('name',)


class SimpleGenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genus
        fields = ('name', 'family')


class SimpleSpeciesSerializer(serializers.ModelSerializer):
    local_names = SimpleSpeciesLocalNameSerializer(many=True)
    class Meta:
        model = Species
        fields = ('name', 'genus', 'local_names')


class SimpleAllometricEquationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllometricEquation





