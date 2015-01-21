## api/views.py
import Geohash

from django.contrib.auth.models import User

from rest_framework import serializers, fields

from globallometree.apps.source.models import (
    Reference,
    Institution
)

from globallometree.apps.allometric_equations.models import (
    Population, 
    TreeType, 
    AllometricEquation
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
    Location,
    ForestType
)


class HyperLinkedWithIdSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(HyperLinkedWithIdSerializer, self).__init__(*args, **kwargs)
        self.fields[self.Meta.model._meta.pk.name] = fields.IntegerField()


class ReferenceSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = Reference
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
        exclude = ('Created', 'Modified')


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
        exclude = ('Created', 'Modified')


class PopulationSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = Population
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


class ForestTypeSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = ForestType   
        exclude = ('Created', 'Modified')


class LocationSerializer(HyperLinkedWithIdSerializer):
    Country = CountrySerializer(many=False)
    Biome_FAO = BiomeFAOSerializer(many=False)
    Biome_UDVARDY = BiomeUdvardySerializer(many=False)
    Biome_WWF = BiomeWWFSerializer(many=False)
    Division_BAILEY = DivisionBaileySerializer(many=False)
    Biome_HOLDRIDGE = BiomeHoldridgeSerializer(many=False)
    Forest_type = ForestTypeSerializer(many=False)

    class Meta:
        model = Location
        exclude = ('Created', 'Modified')


class LocationGroupSerializer(HyperLinkedWithIdSerializer):
    Locations = LocationSerializer(many=True)
    class Meta:
        model = LocationGroup    
        exclude = ('Created', 'Modified')


class TreeTypeSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = TreeType   
        exclude = ('Created', 'Modified')


class AllometricEquationSerializer(HyperLinkedWithIdSerializer):
    Species_group = SpeciesGroupSerializer(many=False)
    Location_group = LocationGroupSerializer(many=False)
    Population = PopulationSerializer(many=False) 
    Tree_type = TreeTypeSerializer(many=False)
    Reference = ReferenceSerializer(many=False)
    class Meta:
        model = AllometricEquation
        exclude = ('Created', 'Modified',)


class WoodDensitySerializer(HyperLinkedWithIdSerializer):
    Species = SpeciesSerializer(many=False)
    Subspecies = SubspeciesSerializer(many=False)
    Population = PopulationSerializer(many=False) 
    Reference = ReferenceSerializer(many=False)
    class Meta:
        model = AllometricEquation
        exclude = ('Created', 'Modified',)


class DataLicenseSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = DataLicense
        exclude = ('Created', 'Modified',)


class DatasetSerializer(HyperLinkedWithIdSerializer):

    class Meta:
        model = Dataset
        exclude = ('Created', 'Modified', 'User', 'Uploaded_data_file')


class DataRequestSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = DataRequest
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
    Family_ID = fields.IntegerField(source="Genus.Family.Family_ID")
    Genus_ID = fields.IntegerField(source="Genus.Genus_ID")

    Scientific_name = fields.SerializerMethodField()

    def get_Scientific_name(self, obj):
       return ' '.join([obj.Genus.Family.Name,
                        obj.Genus.Name,
                        obj.Name])

    class Meta:
        model = Species
        fields = (
                  'Scientific_name',
                  'Family', 
                  'Genus',
                  'Species',
                  'Family_ID',
                  'Genus_ID',
                  'Species_ID',
                  'Species_local_names'
                  )

class SimpleSubspeciesSerializer(SimpleSpeciesSerializer):
    
    Family = fields.CharField(source="Species.Genus.Family.Name")
    Genus = fields.CharField(source="Species.Genus.Name")
    Species = fields.CharField(source="Species.Name")
    Species_local_names = SimpleSpeciesLocalNameSerializer(
        many = True,
        source = 'Species.Local_names'
        )
    Species_ID = fields.IntegerField(source="Species.Species_ID")
    Family_ID = fields.IntegerField(source="Species.Genus.Family.Family_ID")
    Genus_ID = fields.IntegerField(source="Species.Genus.Genus_ID")

    Subspecies = fields.CharField(source="Name")
    Subspecies_local_names = SimpleSubspeciesLocalNameSerializer(
        many=True,
        source='Local_names')

    def get_Scientific_name(self, obj):
        try:
           return ' '.join([obj.Species.Genus.Family.Name,
                            obj.Species.Genus.Name,
                            obj.Species.Name,
                            obj.Name])
        
        except:
            import pdb; pdb.set_trace()

    class Meta:
        model = Subspecies
        fields = (
                  'Family', 
                  'Genus',
                  'Species',
                  'Subspecies',
                  'Family_ID',
                  'Genus_ID',
                  'Species_ID',
                  'Subspecies_ID',
                  'Species_local_names',
                  'Subspecies_local_names',
                  'Scientific_name')


class SpeciesGroupMixin(object):

    def get_Species(self, obj):

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
    Species = fields.SerializerMethodField()
    class Meta: 
        model = SpeciesGroup
        fields = ('Species_group_ID', 'Species')


class SimpleForestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiomeFAO
        fields = ('Forest_type_ID', 'Name',)


class SimpleBiomeFAOSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiomeFAO
        fields = ('Biome_FAO_ID', 'Name',)


class SimpleBiomeUdvardySerializer(serializers.ModelSerializer):
    class Meta:
        model = BiomeUdvardy
        fields = ('Biome_UDVARDY_ID', 'Name',)


class SimpleBiomeWWFSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiomeWWF
        fields = ('Biome_WWF_ID', 'Name',)


class SimpleBiomeHoldridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiomeHoldridge
        fields = ('Biome_HOLDRIDGE_ID','Name',)


class SimpleDivisionBaileySerializer(serializers.ModelSerializer):
    class Meta:
        model = DivisionBailey
        fields = ('Division_BAILEY_ID', 'Name',)


class SimpleLocationSerializer(serializers.ModelSerializer):
   
    Country = fields.CharField(source="Country.Formal_name")
    Biome_FAO = fields.CharField(source="Biome_FAO.Name")
    Biome_UDVARDY = fields.CharField(source="Biome_UDVARDY.Name")
    Biome_WWF = fields.CharField(source="Biome_WWF.Name")
    Division_BAILEY = fields.CharField(source="Division_BAILEY.Name")
    Biome_HOLDRIDGE = fields.CharField(source="Biome_HOLDRIDGE.Name")
    Forest_type = fields.CharField(source="Forest_type.Name")
    
    Country_ID = fields.IntegerField(source="Country.Country_ID")
    Country_3166_3 = fields.CharField(source="Country.Iso3166a3")

    Biome_FAO_ID = fields.IntegerField(source="Biome_FAO.Biome_FAO_ID")
    Biome_UDVARDY_ID = fields.IntegerField(source="Biome_UDVARDY.Biome_UDVARDY_ID")
    Biome_WWF_ID = fields.IntegerField(source="Biome_WWF.Biome_WWF_ID")    
    Division_BAILEY_ID = fields.IntegerField(source="Division_BAILEY.Division_BAILEY_ID") 
    Biome_HOLDRIDGE_ID = fields.IntegerField(source="Biome_HOLDRIDGE.Biome_HOLDRIDGE_ID") 
    Forest_type_ID = fields.IntegerField(source="Forest_type.Forest_type_ID") 
    Geohash = fields.SerializerMethodField()
    LatLonString = fields.SerializerMethodField()

    # Geohash and LatLonString are designed to help out with elasticsearch queries 
    def get_Geohash(self, obj):
        if obj.Latitude and obj.Longitude:
            return Geohash.encode(obj.Latitude, obj.Longitude)
        else:
            return None

    def get_LatLonString(self, obj):
        if obj.Latitude:
            lat_lon_string = "%s,%s" % (obj.Latitude,obj.Longitude)
        else:
            lat_lon_string = None  
        return lat_lon_string

    class Meta: 
        model = Location
        fields = (
            "Location_ID",
            "Name",
            "Commune",
            "Province",
            "Region",
            "Country",
            "Country_3166_3", 
            "Biome_FAO",
            "Biome_HOLDRIDGE", 
            "Biome_UDVARDY", 
            "Biome_WWF",
            "Division_BAILEY",
            "Forest_type",
            "Geohash", 
            "Latitude",
            "Longitude",
            "LatLonString",
            "Biome_FAO_ID",
            "Biome_UDVARDY_ID",
            "Biome_HOLDRIDGE_ID", 
            "Biome_WWF_ID",
            "Division_BAILEY_ID", 
            "Country_ID",
            "Forest_type_ID",
            )


class SimpleLocationGroupSerializer(serializers.ModelSerializer):
    Locations = SimpleLocationSerializer(many=True)

    class Meta:
        model = LocationGroup
        fields = ('Location_group_ID', 'Locations',)


class SimplePopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Population
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
        fields = ('Country_ID', 'Name', 'Code', 'Continent')   


class SimpleDataLicenseSerializer(serializers.ModelSerializer):
    Permitted_use_text = fields.SerializerMethodField()
    def get_Permitted_use_text(self, obj):
        if obj.Permitted_use == 'other':
            return obj.Permitted_use_other_value
        else:
            return obj.get_Permitted_use_display()
    class Meta:
        model = DataLicense
        exclude = ('Created', 'Modified', 'User','Public_choice')


class SimpleDatasetSerializer(serializers.ModelSerializer):
    Data_license = SimpleDataLicenseSerializer(many=False)
    Data_type_text = fields.CharField(
        source="get_Data_type_display",
        read_only=True
        )
    
    class Meta:
        model = Dataset
        exclude = ('Created', 'Modified', 'User', 'Uploaded_data_file', 'Imported')


class SimpleReferenceSerializer(serializers.ModelSerializer):
    Year = fields.SerializerMethodField()
    class Meta:
        model = Reference
        fields = ('Label', 'Author', 'Year', 'Reference', 'Reference_ID')

    def get_Year(self, obj):
        #Trim 1986b to be 1986
        #Maybe reference should have a Year and Year_string attribute?
        if obj.Year and len(obj.Year) > 4: 
            return obj.Year[0:4]
        else:
            return obj.Year


class SimpleLinkedModelSerializer(serializers.ModelSerializer):
    Species_group = SimpleSpeciesGroupSerializer(many=False)
    Location_group = SimpleLocationGroupSerializer(many=False)
    #Dataset = SimpleDatasetSerializer(many=False)
    Reference = SimpleReferenceSerializer()


class SimpleAllometricEquationSerializer(SimpleLinkedModelSerializer):
    class Meta:
        model = AllometricEquation
        exclude = ('Created', 'Modified')


class SimpleWoodDensitySerializer(SimpleLinkedModelSerializer):
    class Meta:
        model = WoodDensity
        exclude = ('Created', 'Modified', )


