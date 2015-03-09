## api/views.py
import Geohash

from collections import OrderedDict
from django.contrib.auth.models import User

from rest_framework import serializers, fields

from globallometree.apps.data_sharing import models as data_sharing_models 
from globallometree.apps.source import models as source_models
from globallometree.apps.allometric_equations import models as allometric_equation_models
from globallometree.apps.taxonomy import models as taxonomy_models
from globallometree.apps.wood_densities import models as wood_density_models 
from globallometree.apps.raw_data import models as raw_data_models
from globallometree.apps.locations import models as location_models 


class HyperLinkedWithIdSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(HyperLinkedWithIdSerializer, self).__init__(*args, **kwargs)
        self.fields[self.Meta.model._meta.pk.name] = fields.IntegerField()


class ReferenceSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = source_models.Reference
        exclude = ('Created', 'Modified',)


class InstitutionSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = source_models.Institution
        exclude = ('Created', 'Modified',)


class FamilySerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = taxonomy_models.Family
        exclude = ('Created', 'Modified',)


class GenusSerializer(HyperLinkedWithIdSerializer):
    Family = FamilySerializer(many=False)
    class Meta:
        model = taxonomy_models.Genus
        exclude = ('Created', 'Modified',)


class SpeciesLocalNameSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = taxonomy_models.SpeciesLocalName
        exclude = ('Created', 'Modified',)
             

class SpeciesSerializer(HyperLinkedWithIdSerializer):
    Genus = GenusSerializer(many=False)
    Local_names = SpeciesLocalNameSerializer(many=True)
    class Meta:
        model = taxonomy_models.Species
        exclude = ('Created', 'Modified')


class SubspeciesLocalNameSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = taxonomy_models.SubspeciesLocalName
        exclude = ('Created', 'Modified')


class SubspeciesSerializer(HyperLinkedWithIdSerializer):
    Species = SpeciesSerializer(many=False)
    Local_names = SubspeciesLocalNameSerializer(many=True)
    class Meta:
        model = taxonomy_models.Subspecies
        exclude = ('Created', 'Modified',)


class SpeciesGroupSerializer(HyperLinkedWithIdSerializer):
    Subspecies = SubspeciesSerializer(many=True) 
    Species = SpeciesSerializer(many=True)
    class Meta:
        model = taxonomy_models.SpeciesGroup
        exclude = ('Created', 'Modified')


class PopulationSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = allometric_equation_models.Population
        exclude = ('Created', 'Modified',)


class ContinentSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = location_models.Continent
        exclude = ('Created', 'Modified',)


class CountrySerializer(HyperLinkedWithIdSerializer):
    Continent = ContinentSerializer(many=False)
    class Meta:
        model = location_models.Country
        exclude = ('Created', 'Modified',)


class BiomeFAOSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = location_models.BiomeFAO
        exclude = ('Created', 'Modified',)


class BiomeUdvardySerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = location_models.BiomeUdvardy
        exclude = ('Created', 'Modified',)


class BiomeWWFSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = location_models.BiomeWWF
        exclude = ('Created', 'Modified',)


class DivisionBaileySerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = location_models.DivisionBailey
        exclude = ('Created', 'Modified',)


class BiomeHoldridgeSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = location_models.BiomeHoldridge
        exclude = ('Created', 'Modified',)


class ForestTypeSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = location_models.ForestType   
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
        model = location_models.Location
        exclude = ('Created', 'Modified')


class LocationGroupSerializer(HyperLinkedWithIdSerializer):
    Locations = LocationSerializer(many=True)
    class Meta:
        model = location_models.LocationGroup    
        exclude = ('Created', 'Modified')


class TreeTypeSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = allometric_equation_models.TreeType   
        exclude = ('Created', 'Modified')


class LinkedModelSerializer(HyperLinkedWithIdSerializer):
    Species_group = SpeciesGroupSerializer(many=False)
    Location_group = LocationGroupSerializer(many=False)
    Reference = ReferenceSerializer(many=False)


class AllometricEquationSerializer(LinkedModelSerializer):
    Population = PopulationSerializer(many=False) 
    Tree_type = TreeTypeSerializer(many=False)
    
    class Meta:
        model = allometric_equation_models.AllometricEquation
        exclude = ('Created', 'Modified',)


class WoodDensitySerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = wood_density_models.WoodDensity
        exclude = ('Created', 'Modified',)


class RawDataSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = raw_data_models.RawData
        exclude = ('Created', 'Modified',)


class DataLicenseSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = data_sharing_models.DataLicense
        exclude = ('Created', 'Modified',)


class DatasetSerializer(HyperLinkedWithIdSerializer):

    class Meta:
        model = data_sharing_models.Dataset
        exclude = ('Created', 'Modified', 'User', 'Uploaded_data_file', 'Data_as_json')


class DataRequestSerializer(HyperLinkedWithIdSerializer):
    class Meta:
        model = data_sharing_models.DataRequest
        exclude = ('Created', 'Modified',)



########################################################################
#############   SIMPLE SERIALIZERS #####################################
########################################################################


class SimpleInstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = source_models.Institution
        fields = ('Name',)


class SimpleSpeciesLocalNameSerializer(serializers.ModelSerializer):
    Language = fields.CharField(source="Language_iso_639_3")
    class Meta:
        model = taxonomy_models.SpeciesLocalName
        fields = ('Local_name', 'Language')


class SimpleSubspeciesLocalNameSerializer(serializers.ModelSerializer):
    Language = fields.CharField(source="Language_iso_639_3")
    class Meta:
        model = taxonomy_models.SubspeciesLocalName
        fields = ('Local_name', 'Language')


class SimpleFamilySerializer(serializers.ModelSerializer):
    Family = fields.CharField(source="Name")
    Scientific_name = fields.SerializerMethodField()

    def get_Scientific_name(self, obj):
        return obj.get_scientific_name()

    class Meta:
        model = taxonomy_models.Family
        fields = ('Scientific_name', 'Family', 'Family_ID', )


class SimpleGenusSerializer(serializers.ModelSerializer):
    Genus = fields.CharField(source="Name")
    Family = fields.CharField(source="Family.Name")

    Genus_ID = fields.IntegerField()
    Family_ID = fields.IntegerField(source="Family.Family_ID")
    
    Scientific_name = fields.SerializerMethodField()

    def get_Scientific_name(self, obj):
        return obj.get_scientific_name()

    class Meta:
        model = taxonomy_models.Genus
        fields = ('Scientific_name', 'Family', 'Genus', 'Family_ID', 'Genus_ID')


class SimpleSpeciesSerializer(serializers.ModelSerializer):
   
    Family = fields.CharField(source="Genus.Family.Name")
    Genus = fields.CharField(source="Genus.Name")
    Species = fields.CharField(source="Name")
    Species_local_names = SimpleSpeciesLocalNameSerializer(
        many = True,
        source = 'Local_names'
        )
    Genus_ID = fields.IntegerField(source="Genus.Genus_ID")
    Family_ID = fields.IntegerField(source="Genus.Family.Family_ID")
    
    Scientific_name = fields.SerializerMethodField()

    def get_Scientific_name(self, obj):
        return obj.get_scientific_name()

    class Meta:
        model = taxonomy_models.Species
        fields = (
                  'Scientific_name',
                  'Family', 
                  'Genus',
                  'Species',
                  'Species_local_names',
                  'Family_ID',
                  'Genus_ID',
                  'Species_ID',
                  )

class SimpleSubspeciesSerializer(serializers.ModelSerializer):
    
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

    Scientific_name = fields.SerializerMethodField()

    def get_Scientific_name(self, obj):
        return obj.get_scientific_name()

    class Meta:
        model = taxonomy_models.Subspecies
        fields = ('Scientific_name',
                  'Family', 
                  'Genus',
                  'Species',
                  'Subspecies',
                  'Species_local_names',
                  'Subspecies_local_names',
                  'Family_ID',
                  'Genus_ID',
                  'Species_ID',
                  'Subspecies_ID',
                  )


class SimpleSpeciesDefinition(serializers.Serializer):
    """
    This is basically trying to flatten out all of the species, families, local names,
    etc into a simple single record
    """
   
    Family = fields.CharField(required=False, allow_null=True)
    Genus = fields.CharField(required=False,allow_null=True)
    Species = fields.CharField(required=False,allow_null=True)
    Species_local_names = SimpleSpeciesLocalNameSerializer(
        many = True,
        required=False
        )
    Species_ID = fields.IntegerField(required=False,allow_null=True)
    Family_ID = fields.IntegerField(required=False,allow_null=True)
    Genus_ID = fields.IntegerField(required=False,allow_null=True)

    Subspecies = fields.CharField(required=False,allow_null=True)
    Subspecies_local_names = SimpleSubspeciesLocalNameSerializer(
        many=True,
        required=False)

    Scientific_name = fields.CharField(read_only=True,allow_null=True)


class SimpleSpeciesGroupSerializer(serializers.ModelSerializer):
    Group = SimpleSpeciesDefinition(many=True)
    
    class Meta: 
        model = taxonomy_models.SpeciesGroup
        fields = ('Species_group_ID', 'Group')

    def create(self, data):
        ModelClass = self.Meta.model
        species_group = ModelClass()
        # Since the species group is m2m, we need to save a copy of it
        # before adding any species
        species_group.save()
        for species_def in data['Group']:

            # match the species def to our database
            species_def_matched = SimpleSpeciesGroupSerializer.match_species_def_to_db(species_def)

            # create any needed taxonomy models
            # when there is not an id, but there is a name,
            # it indicates we need to create the model
            if species_def_matched['Family'] and not species_def_matched['Family_ID']:
                family = taxonomy_models.Family.objects.get_or_create(
                    Name=species_def_matched['Family'])[0]
            else:
                family = species_def_matched['db_family']

            if species_def_matched['Genus'] and not species_def_matched['Genus_ID']:
                genus = taxonomy_models.Genus.objects.get_or_create(
                    Name=species_def_matched['Genus'], 
                    Family=family)[0]
            else:
                genus = species_def_matched['db_genus']

            if species_def_matched['Species'] and not species_def_matched['Species_ID']:
                species = taxonomy_models.Species.objects.get_or_create(
                    Name=species_def_matched['Species'], 
                    Genus=genus)[0]
            else:
                species = species_def_matched['db_species']

            if species_def_matched['Subspecies'] and not species_def_matched['Subspecies_ID']:
                subspecies = taxonomy_models.Subspecies.objects.get_or_create(
                    Name=species_def_matched['Subspecies'], 
                    Species=species)[0]
            else:
                subspecies = species_def_matched['db_subspecies']

            # link by the most specific record only
            if subspecies:
                species_group.Subspecies.add(subspecies)
            elif species:
                species_group.Species.add(species)
            elif genus:
                species_group.Genera.add(genus)
            elif family:
                species_group.Families.add(family)            

        return species_group

  
    @staticmethod       
    def match_species_def_to_db(species_def):
     
        # Don't trust the ids we were given
        species_def['Family_ID'] = None
        species_def['Species_ID'] = None
        species_def['Genus_ID'] = None
        species_def['Subspecies_ID'] = None

        species_def['db_family'] = None
        species_def['db_genus'] = None
        species_def['db_species'] = None
        species_def['db_subspecies'] = None

        # Family and Genus are required by the parser
        try:
            species_def['db_family'] = taxonomy_models.Family.objects.get(Name=species_def['Family'])
            species_def['Family_ID'] = species_def['db_family'].pk
        except taxonomy_models.Family.DoesNotExist:
            pass
            
        # If we have the family in our db, we try to find the genus id
        if species_def['db_family']:
            try:
                species_def['db_genus'] = taxonomy_models.Genus.objects.get(
                    Family=species_def['db_family'],
                    Name=species_def['Genus']
                    )
                species_def['Genus_ID'] = species_def['db_genus'].pk
            except taxonomy_models.Genus.DoesNotExist:
                pass
                
        # If we have the genus in our db, we try to find the species id
        if species_def['db_genus'] and 'Species' in species_def.keys():
            try:
                species_def['db_species'] = taxonomy_models.Species.objects.get(
                    Genus=species_def['db_genus'],
                    Name=species_def['Species'])
                species_def['Species_ID'] = species_def['db_species'].pk
            except taxonomy_models.Species.DoesNotExist:
                pass

        # If we have the species in our db, we try to find the subspecies id
        if species_def['db_species'] and 'Subspecies' in species_def.keys():
            try:
                specied_def['db_subspecies'] = taxonomy_models.Subspecies.objects.get(
                    Species=species_def['db_species'], 
                    Name=species_def['Subspecies']
                    )
                species_def['Subpsecies_ID'] = specied_def['db_subspecies'].pk
            except taxonomy_models.Subspecies.DoesNotExist:
                pass

        return species_def



class SimpleForestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = location_models.BiomeFAO
        fields = ('Forest_type_ID', 'Name',)


class SimpleBiomeFAOSerializer(serializers.ModelSerializer):
    class Meta:
        model = location_models.BiomeFAO
        fields = ('Biome_FAO_ID', 'Name',)


class SimpleBiomeUdvardySerializer(serializers.ModelSerializer):
    class Meta:
        model = location_models.BiomeUdvardy
        fields = ('Biome_UDVARDY_ID', 'Name',)


class SimpleBiomeWWFSerializer(serializers.ModelSerializer):
    class Meta:
        model = location_models.BiomeWWF
        fields = ('Biome_WWF_ID', 'Name',)


class SimpleBiomeHoldridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = location_models.BiomeHoldridge
        fields = ('Biome_HOLDRIDGE_ID','Name',)


class SimpleDivisionBaileySerializer(serializers.ModelSerializer):
    class Meta:
        model = location_models.DivisionBailey
        fields = ('Division_BAILEY_ID', 'Name',)


class SimpleLocationSerializer(serializers.ModelSerializer):
   
    Country = fields.ChoiceField(
        source="Country.Formal_name", 
        allow_null=True,
        required=False,
        choices = [(country.Formal_name, country.Formal_name) for country in location_models.Country.objects.all()]
        )

    Biome_FAO = fields.ChoiceField(
        source="Biome_FAO.Name", 
        allow_null=True,
        required=False,
        choices = [(biome.Name, biome.Name) for biome in location_models.BiomeFAO.objects.all()]
        )

    Biome_UDVARDY = fields.ChoiceField(
        source="Biome_UDVARDY.Name", 
        allow_null=True,
        required=False,
        choices = [(biome.Name, biome.Name) for biome in location_models.BiomeUdvardy.objects.all()]
        )

    Biome_WWF = fields.ChoiceField(
        source="Biome_WWF.Name", 
        allow_null=True,
        required=False,
        choices= [(biome.Name, biome.Name) for biome in location_models.BiomeWWF.objects.all()]
        )

    Biome_HOLDRIDGE = fields.ChoiceField(
        source="Biome_HOLDRIDGE.Name", 
        allow_null=True,
        required=False,
        choices=[(biome.Name, biome.Name) for biome in location_models.BiomeHoldridge.objects.all()]
        )

    Division_BAILEY = fields.ChoiceField(
        source="Division_BAILEY.Name", 
        allow_null=True,
        required=False,
        choices=[(division.Name, division.Name) for division in location_models.DivisionBailey.objects.all()]
        )

    Forest_type = fields.ChoiceField(
        source="Forest_type.Name", 
        allow_null=True,
        required=False,
        choices=[(forest.Name, forest.Name) for forest in location_models.ForestType.objects.all()]
        )

    Country_3166_3 = fields.ChoiceField(
        source="Country.Iso3166a3", 
        allow_null=True,
        required=False,
        choices = [(country.Iso3166a3, country.Iso3166a3) for country in location_models.Country.objects.all()]
        )

    # IDs are read only since we are not trusting them at the moment
    # They could be ids internal to a single dataset or study
    Country_ID = fields.IntegerField(
        source="Country.Country_ID", 
        read_only=True
        )
    Biome_FAO_ID = fields.IntegerField(
        source="Biome_FAO.Biome_FAO_ID", 
        read_only=True
        )
    Biome_UDVARDY_ID = fields.IntegerField(
        source="Biome_UDVARDY.Biome_UDVARDY_ID", 
        read_only=True)

    Biome_WWF_ID = fields.IntegerField(
        source="Biome_WWF.Biome_WWF_ID",
        read_only=True
        )    
    Division_BAILEY_ID = fields.IntegerField(
        source="Division_BAILEY.Division_BAILEY_ID", 
        read_only=True
        ) 
    Biome_HOLDRIDGE_ID = fields.IntegerField(
        source="Biome_HOLDRIDGE.Biome_HOLDRIDGE_ID",
        read_only=True) 
    Forest_type_ID = fields.IntegerField(
        source="Forest_type.Forest_type_ID", 
        read_only=True) 

    # Serializer fields are always read only
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


    def create(self, data):
        ModelClass = self.Meta.model
        location_group = ModelClass()
        # Since the species group is m2m, we need to save a copy of it
        # before adding any species
        location_group.save()
        for location in data['Group']:

            # match the location def to our database
            location_matched = SimpleLocationGroupSerializer.match_location_to_db(location)

                       

        return location_group

  
   

    class Meta: 
        model = location_models.Location
        
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
    Group = SimpleLocationSerializer(many=True)

    class Meta:
        model = location_models.LocationGroup
        fields = ('Location_group_ID', 'Group',)


class SimplePopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = allometric_equation_models.Population
        fields = ('Name',)


class SimpleContinentSerializer(serializers.ModelSerializer):
    class Meta:
        model = location_models.Continent
        fields = ('Name',)


class SimpleCountrySerializer(serializers.ModelSerializer):
    Name = fields.CharField(source='Formal_name')
    Code = fields.CharField(source='Iso3166a3')
    Continent = fields.CharField(source="Continent.Name")
    class Meta:
        model = location_models.Country
        fields = ('Country_ID', 'Name', 'Code', 'Continent')   


class SimpleDataLicenseSerializer(serializers.ModelSerializer):
    Permitted_use_text = fields.SerializerMethodField()
    def get_Permitted_use_text(self, obj):
        if obj.Permitted_use == 'other':
            return obj.Permitted_use_other_value
        else:
            return obj.get_Permitted_use_display()
    class Meta:
        model = data_sharing_models.DataLicense
        exclude = ('Created', 'Modified', 'User','Public_choice')


class SimpleDatasetSerializer(serializers.ModelSerializer):
    Data_license = SimpleDataLicenseSerializer(many=False)
    Data_type_text = fields.CharField(
        source="get_Data_type_display",
        read_only=True
        )
    
    class Meta:
        model = data_sharing_models.Dataset
        exclude = ('Created', 'Modified', 'User', 'Uploaded_data_file', 'Imported', 'Data_as_json')


class SimpleReferenceSerializer(serializers.ModelSerializer):
    Year = fields.SerializerMethodField()
    class Meta:
        model = source_models.Reference
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
    Dataset = SimpleDatasetSerializer(many=False, read_only=True)
    Reference = SimpleReferenceSerializer(many=False)
    Contributor = fields.CharField(source='Contributor.Name', allow_null=True)
    Operator = fields.CharField(source='Operator.Name', allow_null=True)

    def create(self, validated_data):
        species_data = validated_data.pop('Species_group')
        location_data = validated_data.pop('Location_group')
        reference_data = validated_data.pop('Reference')
        contributor_data = validated_data.pop('Contributor')
        operator_data = validated_data.pop('Operator')

        ModelClass = self.Meta.model
        instance = ModelClass.objects.create(**validated_data)

        if contributor_data and contributor_data['Name']:
            instance.Contributor = source_models.Institution.objects.get_or_create(Name=contributor_data['Name'])[0]
        
            if operator_data and operator_data['Name']:
                instance.Operator = source_models.Operator.objects.get_or_create(Name=operator_data['Name'],
                                                                            Institution=instance.Contributor)[0]
        if species_data:
            species_group_serializer = SimpleSpeciesGroupSerializer(data=species_data)
            if species_group_serializer.is_valid():
                instance.Species_group = species_group_serializer.save()

        if location_data:
            location_group_serializer = SimpleLocationGroupSerializer(data=location_data)
            if location_group_serializer.is_valid():
                instance.Location_group = location_group_serializer.save()

        instance.Reference = source_models.Reference.objects.get_or_create(**reference_data)[0]

        instance.save()

        return instance


class SimpleAllometricEquationSerializer(SimpleLinkedModelSerializer):
    class Meta:
        model = allometric_equation_models.AllometricEquation
        exclude = ('Created', 'Modified')


class SimpleWoodDensitySerializer(SimpleLinkedModelSerializer):
    class Meta:
        model = wood_density_models.WoodDensity
        exclude = ('Created', 'Modified', )


class SimpleRawDataSerializer(SimpleLinkedModelSerializer):
    class Meta:
        model = raw_data_models.RawData
        exclude = ('Created', 'Modified', )


