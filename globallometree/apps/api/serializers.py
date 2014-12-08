## api/views.py
from django.contrib.auth.models import User

from rest_framework import serializers, fields

from globallometree.apps.common.models import (
    DataReference,
    Institution
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
        exclude = ('Created', 'Modified',)


class InstitutionSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = Institution
        exclude = ('Created', 'Modified',)


class FamilySerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = Family
        exclude = ('Created', 'Modified',)


class GenusSerializer(HyperLinkedWithIdSerializer):
    Family = FamilySerializer(many=False)

    class Meta:
        model = Genus
        exclude = ('Created', 'Modified',)


class SpeciesLocalNameSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = SpeciesLocalName
        exclude = ('Created', 'Modified',)
             

class SpeciesSerializer(HyperLinkedWithIdSerializer):
    Genus = GenusSerializer(many=False)
    Local_names = SpeciesLocalNameSerializer(many=True)
    class Meta:
        model = Species
        exclude = ('Created', 'Modified', 'Original_ID_Species')


class SubspeciesLocalNameSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = SubspeciesLocalName
        exclude = ('Created', 'Modified')


class SubspeciesSerializer(HyperLinkedWithIdSerializer):
    Species = SpeciesSerializer(many=False)
    Local_names = SubspeciesLocalNameSerializer(many=True)
    class Meta:
        model = Subspecies
        exclude = ('Created', 'Modified',)


class SpeciesGroupSerializer(HyperLinkedWithIdSerializer):
    Subspecies = SubspeciesSerializer(many=True) 
    Species = SpeciesSerializer(many=True)
    class Meta:
        model = SpeciesGroup
        exclude = ('Created', 'Modified', 'Original_ID_Group')


class PopulationSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = Population
        exclude = ('Created', 'Modified',)


class EcosystemSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = Ecosystem
        exclude = ('Created', 'Modified',)


class ContinentSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = Continent
        exclude = ('Created', 'Modified',)


class CountrySerializer(HyperLinkedWithIdSerializer):
    Continent = ContinentSerializer(many=False)
    class Meta:
        model = Country
        exclude = ('Created', 'Modified',)


class BiomeFAOSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = BiomeFAO
        exclude = ('Created', 'Modified',)


class BiomeUdvardySerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = BiomeUdvardy
        exclude = ('Created', 'Modified',)


class BiomeWWFSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = BiomeWWF
        exclude = ('Created', 'Modified',)


class DivisionBaileySerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = DivisionBailey
        exclude = ('Created', 'Modified',)


class BiomeHoldridgeSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = BiomeHoldridge
        exclude = ('Created', 'Modified',)


class LocationSerializer(HyperLinkedWithIdSerializer):
    Country = CountrySerializer(many=False)
    Biome_FAO = BiomeFAOSerializer(many=False)
    Biome_UDVARDY = BiomeUdvardySerializer(many=False)
    Biome_WWF = BiomeWWFSerializer(many=False)
    Division_BAILEY = DivisionBaileySerializer(many=False)
    Biome_HOLDRIDGE = BiomeHoldridgeSerializer(many=False)
    class Meta:
        model = Location
        exclude = ('Created', 'Modified', 'Original_ID_Location')


class LocationGroupSerializer(HyperLinkedWithIdSerializer):
    Locations = LocationSerializer(many=True)
    class Meta:
        model = LocationGroup    
        exclude = ('Created', 'Modified', 'Original_Group_Location')


class AllometricEquationSerializer(HyperLinkedWithIdSerializer):
    Species_group = SpeciesGroupSerializer(many=False)
    Location_group = LocationGroupSerializer(many=False)
    Population = PopulationSerializer(many=False) 
    Ecosystem = EcosystemSerializer(many=False)
    Reference = DataReferenceSerializer(many=False)
    class Meta:
        model = AllometricEquation
        exclude = ('Created', 'Modified', 'ID_REF', 'Data_submission')


class WoodDensitySerializer(HyperLinkedWithIdSerializer):
    Species = SpeciesSerializer(many=False)
    Subspecies = SubspeciesSerializer(many=False)
    Population = PopulationSerializer(many=False) 
    Ecosystem = EcosystemSerializer(many=False)
    Reference = DataReferenceSerializer(many=False)
    class Meta:
        model = AllometricEquation
        exclude = ('Created', 'Modified',)


class DataSharingAgreementSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = DataSharingAgreement
        exclude = ('Created', 'Modified',)


class DataSetSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = DataSet
        exclude = ('Created', 'Modified',)


class DataAccessRequestSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = DataAccessRequest
        exclude = ('Created', 'Modified',)



########################################################################
#############   SIMPLE SERIALIZERS #####################################
########################################################################


class SimpleInstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ('Name',)


class SimpleSpeciesLocalNameSerializer(serializers.ModelSerializer):
    Language = fields.CharField(source="Language_iso_639_3")
    class Meta:
        model = SpeciesLocalName
        fields = ('Local_name', 'Language')


class SimpleSubspeciesLocalNameSerializer(serializers.ModelSerializer):
    Language = fields.CharField(source="Language_iso_639_3")
    class Meta:
        model = SubspeciesLocalName
        fields = ('Local_name', 'Language')


class SimpleFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ('Name',)


class SimpleGenusSerializer(serializers.ModelSerializer):
    Family = fields.CharField(source="Family.Name")
    class Meta:
        model = Genus
        fields = ('Name', 'Family')


class SimpleSpeciesSerializer(serializers.ModelSerializer):
    Family = fields.CharField(source="Genus.Family.Name")
    Genus = fields.CharField(source="Genus.Name")
    Species = fields.CharField(source="Name")
    Species_local_names = SimpleSpeciesLocalNameSerializer(
        many = True,
        source = 'Local_names'
        )

    class Meta:
        model = Species
        fields = ('Species', 'Genus', 'Family', 'Species_local_names')


class SimpleSubspeciesSerializer(serializers.ModelSerializer):
    Family = fields.CharField(source="Species.Genus.Family.Name")
    Genus = fields.CharField(source="Species.Genus.Name")
    Species = fields.CharField(source="Species.Name")
    Species_local_names = SimpleSpeciesLocalNameSerializer(
        many = True,
        source = 'Species.Local_names'
        )
    Subspecies = fields.CharField(source="Name")
    Subspecies_local_names = SimpleSubspeciesLocalNameSerializer(
        many=True,
        source='Local_names')

    Species_local_names = SimpleSpeciesLocalNameSerializer(
        many=True,
        source='Species.Local_names')

    class Meta:
        model = Species
        fields = ('Subspecies', 'Genus', 'Family', 'Species', 'Species_local_names', 'Subspecies_local_names')


class SpeciesGroupMixin(object):

    def get_Species_group(self, obj):

        if(hasattr(obj, 'Species_group')):
            group = obj.Species_group
        else:
            group = obj
        data = []
        for species in group.Species.all():
            data.append(SimpleSpeciesSerializer(instance=species, many=False).data)

        for subspecies in group.Subspecies.all():
            data.append(SimpleSubspeciesSerializer(instance=subspecies, many=False).data)
        return data


class SimpleSpeciesGroupSerializer(SpeciesGroupMixin, serializers.ModelSerializer):
    species_group = fields.SerializerMethodField()
    class Meta: 
        model = SpeciesGroup
        fields = ('Species_group', )




class LocationGroupMixin(object):

    def get_Location_group(self, obj):

        if(hasattr(obj, 'Location_group')):
            group = obj.Location_group
        else:
            group = obj
        data = []
        for location in group.Locations.all():
            data.append(SimpleLocationSerializer(instance=location, many=False).data)
        return data


class SimpleBiomeFAOSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiomeFAO
        fields = ('Name',)


class SimpleBiomeUdvardySerializer(serializers.ModelSerializer):
    class Meta:
        model = BiomeUdvardy
        fields = ('Name',)


class SimpleBiomeWWFSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiomeWWF
        fields = ('Name',)


class SimpleBiomeHoldridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiomeHoldridge
        fields = ('Name',)


class SimpleDivisionBaileySerializer(serializers.ModelSerializer):
    class Meta:
        model = DivisionBailey
        fields = ('Name',)




class SimpleLocationSerializer(serializers.ModelSerializer):
    Country = fields.CharField(source="Country.Formal_name")
    Biome_FAO = fields.CharField(source="Biome_FAO.Name")
    Biome_UDVARDY = fields.CharField(source="Biome_UDVARDY.Name")
    Biome_WWF = fields.CharField(source="Biome_WWF.Name")
    Division_BAILEY = fields.CharField(source="Division_BAILEY.Name")
    Biome_HOLDRIDGE = fields.CharField(source="Biome_HOLDRIDGE.Name")

    class Meta: 
        model = Location
        exclude = ('Created', 'Modified', 'ID', "Original_ID_Location")


class SimpleLocationGroupSerializer(LocationGroupMixin, 
                                    serializers.ModelSerializer):
    Location_group = fields.SerializerMethodField()

    class Meta:
        model = AllometricEquation
        fields = ('Location_group',)


class SimplePopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Population
        fields = ('Name',)


class SimpleEcosystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ecosystem
        fields = ('Name',)


class SimpleContinentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Continent
        fields = ('Name',)


class SimpleCountrySerializer(serializers.ModelSerializer):
    Name = fields.CharField(source='Formal_name')
    Code = fields.CharField(source='Iso3166a3')
    Continent = fields.CharField(source="Continent.Name")
    class Meta:
        model = Country
        fields = ('Name', 'Code', 'Continent')   


class SimpleDataReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataReference
        fields = ('Label', 'Author', 'Year', 'Reference')


class SimpleAllometricEquationSerializer(SpeciesGroupMixin, 
                                         LocationGroupMixin, 
                                         serializers.ModelSerializer):

    Species_group = fields.SerializerMethodField()
    Location_group = fields.SerializerMethodField()

    class Meta:
        model = AllometricEquation
        exclude = ('Created', 'Modified', 'Data_submission' )


class SimpleWoodDensitySerializer(SpeciesGroupMixin, 
                                  LocationGroupMixin, 
                                  serializers.ModelSerializer):

    Species_group = fields.SerializerMethodField()
    Location_group = fields.SerializerMethodField()

    class Meta:
        model = WoodDensity
        exclude = ('Created', 'Modified', )
        
       
              



