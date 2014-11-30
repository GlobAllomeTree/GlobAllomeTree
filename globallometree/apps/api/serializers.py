## api/views.py
from django.contrib.auth.models import User

from rest_framework import serializers

from globallometree.apps.common.models import (
    DataReference, 
    Institution, 
    Operator
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

class FamilySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Family
        fields = ('id', 'url', 'id', 'name')


class GenusSerializer(serializers.HyperlinkedModelSerializer):
    family = FamilySerializer(many=False)
    class Meta:
        model = Genus
        fields = ('id', 'url','name', 'family')


class SpeciesLocalNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeciesLocalName
        fields = ('id', 'local_name','local_name_latin', 'language_iso_639_3')
             

class SpeciesSerializer(serializers.HyperlinkedModelSerializer):
    genus = GenusSerializer(many=False)
    local_names = SpeciesLocalNameSerializer(many=True)
    class Meta:
        model = Species
        fields = ('id', 'url','name', 'genus', 'local_names')


class SubspeciesLocalNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubspeciesLocalName
        fields = ('id', 'local_name','local_name_latin', 'language_iso_639_3')


class SubspeciesSerializer(serializers.HyperlinkedModelSerializer):
    species = SpeciesSerializer(many=False)
    local_names = SubspeciesLocalNameSerializer(many=True)
    class Meta:
        model = Subspecies
        fields = ('id', 'url','name', 'species', 'local_names')


class PopulationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Population


class EcosystemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ecosystem


class ContinentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Continent
        fields = ('id', 'url','code', 'name')


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    continent = ContinentSerializer(many=False)
    class Meta:
        model = Country
        fields = ('id', 'common_name','formal_name', 'common_name_fr', 'formal_name_fr',
                  'iso3166a2', 'iso3166a3', 'iso3166n3', 'continent', 'centroid_latitude',
                  'centroid_latitude')


class BiomeFAOSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BiomeFAO
        fields = ('id', 'url', 'name')


class BiomeUdvardySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BiomeUdvardy
        fields = ('id', 'url', 'name')


class BiomeWWFSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BiomeWWF
        fields = ('id', 'url', 'name')


class DivisionBaileySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DivisionBailey
        fields = ('id', 'url', 'name')


class BiomeHoldridgeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BiomeHoldridge
        fields = ('id', 'url', 'name')


