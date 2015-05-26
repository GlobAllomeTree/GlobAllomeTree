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
from globallometree.apps.biomass_expansion_factors import models as biomass_expansion_factors_models


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = source_models.Institution
        fields = ('Name',)


class SpeciesLocalNameSerializer(serializers.ModelSerializer):
    Language = fields.CharField(source="Language_iso_639_3")
    class Meta:
        model = taxonomy_models.SpeciesLocalName
        fields = ('Local_name', 'Language')


class FamilySerializer(serializers.ModelSerializer):
    Family = fields.CharField(source="Name")
    Scientific_name = fields.SerializerMethodField()

    def get_Scientific_name(self, obj):
        return obj.get_scientific_name()

    class Meta:
        model = taxonomy_models.Family
        fields = ('Scientific_name', 'Family', 'Family_ID', )


class GenusSerializer(serializers.ModelSerializer):
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


class SpeciesSerializer(serializers.ModelSerializer):
   
    Family = fields.CharField(source="Genus.Family.Name")
    Genus = fields.CharField(source="Genus.Name")
    Species = fields.CharField(source="Name")
    Species_local_names = SpeciesLocalNameSerializer(
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

class SubspeciesSerializer(serializers.ModelSerializer):
    
    Family = fields.CharField(source="Species.Genus.Family.Name")
    Genus = fields.CharField(source="Species.Genus.Name")
    Species = fields.CharField(source="Species.Name")
    Species_local_names = SpeciesLocalNameSerializer(
        many = True,
        source = 'Species.Local_names'
        )
    Species_ID = fields.IntegerField(source="Species.Species_ID")
    Family_ID = fields.IntegerField(source="Species.Genus.Family.Family_ID")
    Genus_ID = fields.IntegerField(source="Species.Genus.Genus_ID")

    Subspecies = fields.CharField(source="Name")
  
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
                  'Family_ID',
                  'Genus_ID',
                  'Species_ID',
                  'Subspecies_ID',
                  )


class SpeciesDefinitionSerializer(serializers.Serializer):
    """
    This is basically trying to flatten out all of the species, families, local names,
    etc into a  single record
    """
   
    Family = fields.CharField(required=False, allow_null=True)
    Genus = fields.CharField(required=False,allow_null=True)
    Species = fields.CharField(required=False,allow_null=True)
    Species_local_names = SpeciesLocalNameSerializer(
        many = True,
        required=False
        )
    Species_ID = fields.IntegerField(required=False,allow_null=True)
    Family_ID = fields.IntegerField(required=False,allow_null=True)
    Genus_ID = fields.IntegerField(required=False,allow_null=True)

    Subspecies = fields.CharField(required=False,allow_null=True)
   
    Scientific_name = fields.CharField(read_only=True,allow_null=True)

    def to_representation(self, obj):
        # Standardize the keys
        if 'Family' not in obj.keys():
            obj['Family'] = None
            obj['Family_ID'] = None

        if 'Genus' not in obj.keys():
            obj['Genus'] = None
            obj['Genus_ID'] = None

        if 'Species' not in obj.keys():
            obj['Species'] = None
            obj['Species_ID'] = None

        if 'Species_local_names' not in obj.keys():
            obj['Species_local_names'] = []

        if 'Subspecies' not in obj.keys():
            obj['Subspecies'] = None
            obj['Subspecies_ID'] = None

        return obj


class SpeciesGroupSerializer(serializers.ModelSerializer):
    # Note that the Group is returned from a method on 
    # the SpeciesGroup model
    Group = SpeciesDefinitionSerializer(many=True)
    
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
            species_def_matched = SpeciesGroupSerializer.match_species_def_to_db(species_def)

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
                species_def['db_subspecies'] = taxonomy_models.Subspecies.objects.get(
                    Species=species_def['db_species'], 
                    Name=species_def['Subspecies']
                    )
                species_def['Subpsecies_ID'] = species_def['db_subspecies'].pk
            except taxonomy_models.Subspecies.DoesNotExist:
                pass

        return species_def


class ForestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = location_models.ForestType
        fields = ('Forest_type_ID', 'Name',)


class BiomeFAOSerializer(serializers.ModelSerializer):
    class Meta:
        model = location_models.BiomeFAO
        fields = ('Biome_FAO_ID', 'Name',)


class BiomeUdvardySerializer(serializers.ModelSerializer):
    class Meta:
        model = location_models.BiomeUdvardy
        fields = ('Biome_UDVARDY_ID', 'Name',)


class BiomeWWFSerializer(serializers.ModelSerializer):
    class Meta:
        model = location_models.BiomeWWF
        fields = ('Biome_WWF_ID', 'Name',)


class BiomeHoldridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = location_models.BiomeHoldridge
        fields = ('Biome_HOLDRIDGE_ID','Name',)


class DivisionBaileySerializer(serializers.ModelSerializer):
    class Meta:
        model = location_models.DivisionBailey
        fields = ('Division_BAILEY_ID', 'Name',)


class LocationSerializer(serializers.ModelSerializer):
 
    Location_name = fields.CharField(
        source="Name", 
        allow_null=True,
        required=False
        )

    Country = fields.ChoiceField(
        source="Country.Formal_name", 
        allow_null=True,
        required=False,
        choices = [country.Formal_name for country in location_models.Country.objects.all()]
        )

    Continent = fields.CharField(
        source="Country.Continent.Name", 
        read_only=True
        ) 

    Biome_FAO = fields.ChoiceField(
        source="Biome_FAO.Name", 
        allow_null=True,
        required=False,
        choices = [biome.Name for biome in location_models.BiomeFAO.objects.all()]
        )

    Biome_UDVARDY = fields.ChoiceField(
        source="Biome_UDVARDY.Name", 
        allow_null=True,
        required=False,
        choices = [biome.Name for biome in location_models.BiomeUdvardy.objects.all()]
        )

    Biome_WWF = fields.ChoiceField(
        source="Biome_WWF.Name", 
        allow_null=True,
        required=False,
        choices= [biome.Name for biome in location_models.BiomeWWF.objects.all()]
        )

    Biome_HOLDRIDGE = fields.ChoiceField(
        source="Biome_HOLDRIDGE.Name", 
        allow_null=True,
        required=False,
        choices=[biome.Name for biome in location_models.BiomeHoldridge.objects.all()]
        )

    Division_BAILEY = fields.ChoiceField(
        source="Division_BAILEY.Name", 
        allow_null=True,
        required=False,
        choices=[division.Name for division in location_models.DivisionBailey.objects.all()]
        )

    Forest_type = fields.ChoiceField(
        source="Forest_type.Name", 
        allow_null=True,
        required=False,
        choices=[forest.Name for forest in location_models.ForestType.objects.all()]
        )

    Country_3166_3 = fields.ChoiceField(
        source="Country.Iso3166a3", 
        allow_null=True,
        required=False,
        choices = [country.Iso3166a3 for country in location_models.Country.objects.all()]
        )

    # IDs are read only since we are not trusting them at the moment
    # They could be ids internal to a single dataset or study
    Country_ID = fields.IntegerField(
        source="Country.Country_ID", 
        read_only=True
        )

    Continent_ID = fields.IntegerField(
        source="Country.Continent.Continent_ID", 
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
            return Geohash.encode(float(obj.Latitude), float(obj.Longitude))
        else:
            return None

    def get_LatLonString(self, obj):
        if obj.Latitude:
            lat_lon_string = "%s,%s" % (obj.Latitude, obj.Longitude)
        else:
            lat_lon_string = None  
        return lat_lon_string

    class Meta: 
        model = location_models.Location
        
        fields = (
            "Location_ID",
            "Location_name",
            "Plot_name",
            "Plot_size_m2",
            "Commune",
            "Province",
            "Region",
            "Country",
            "Country_3166_3",
            "Continent", 
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
            "Continent_ID",
            "Forest_type_ID",
            )

class LocationGroupSerializer(serializers.ModelSerializer):

    Group = LocationSerializer(many=True, source="Locations")
    Location_group_ID = fields.IntegerField()

    class Meta:
        model = location_models.LocationGroup
        fields = ('Location_group_ID', 'Group',)

     

class PopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = allometric_equation_models.Population
        fields = ('Name',)


class ContinentSerializer(serializers.ModelSerializer):
    class Meta:
        model = location_models.Continent
        fields = ('Name',)


class CountrySerializer(serializers.ModelSerializer):
    Name = fields.CharField(source='Formal_name')
    Code = fields.CharField(source='Iso3166a3')
    Continent = fields.CharField(source="Continent.Name")
    class Meta:
        model = location_models.Country
        fields = ('Country_ID', 'Name', 'Code', 'Continent')   


class DataLicenseSerializer(serializers.ModelSerializer):
    Permitted_use_text = fields.SerializerMethodField()
    def get_Permitted_use_text(self, obj):
        return obj.get_Permitted_use_text()
        
    class Meta:
        model = data_sharing_models.DataLicense        
        exclude = ('Created', 'Modified', 'User', 'Public_choice')


class DatasetSerializer(serializers.ModelSerializer):
    Data_license = DataLicenseSerializer(many=False, read_only=True)
    Dataset_url = fields.SerializerMethodField()
    Data_type_text = fields.CharField(
        source="get_Data_type_display",
        read_only=True
        )

    def __init__(self, *args, **kwargs):
        if 'exclude_json' in kwargs.keys():
            self.exclude_json = kwargs.pop('exclude_json')
        else:
            self.exclude_json = False
        return super(DatasetSerializer, self).__init__(*args, **kwargs)

    def get_Dataset_url(self, obj):
        return obj.get_absolute_url()

    def update(self, instance, validated_data):
        instance.Data_as_json = validated_data.get('Data_as_json', instance.Data_as_json)
        instance.Title = validated_data.get('Title', instance.Title)
        instance.Description = validated_data.get('Description', instance.Description)
        instance.save()
        return instance

    def to_representation(self, obj):
        try:
            if (not self.context['request'].user.is_superuser) and (self.context['request'].user != obj.User):
                obj.Data_as_json = None
        except:
            obj.Data_as_json = None

        if self.exclude_json:
            obj.Data_as_json = None

        return super(DatasetSerializer, self).to_representation(obj)
    
    class Meta:
        model = data_sharing_models.Dataset
        exclude = ('Created', 'Modified', 'User', 'Uploaded_dataset_file', 'Imported')
        read_only_fields = ('Data_license', 'Data_type_text', 'Record_count', 'Imported')


class ReferenceSerializer(serializers.ModelSerializer):
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


class LinkedModelSerializer(serializers.ModelSerializer):
    Species_group = SpeciesGroupSerializer(many=False, required=False)
    Location_group = LocationGroupSerializer(many=False, required=False)
    Dataset = DatasetSerializer(many=False, read_only=True, exclude_json=True)
    Reference = ReferenceSerializer(many=False, required=False)
    Contributor = fields.CharField(source='Contributor.Name', allow_null=True, required=False)
    Operator = fields.CharField(source='Operator.Name', allow_null=True, required=False)

    def __init__(self, *args, **kwargs):
        super(LinkedModelSerializer, self).__init__(*args, **kwargs)

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
            species_group_serializer = SpeciesGroupSerializer(data=species_data)
            if species_group_serializer.is_valid():
                instance.Species_group = species_group_serializer.save()

        if location_data:
            location_group, created = location_models.LocationGroup.objects.get_or_create(
                Dataset=self.context['dataset'],
                Dataset_Location_group_ID=location_data['Location_group_ID']
                )
            instance.Location_group = location_group
            # First time we have seen this location group so we save it
            if created:
                # Since the species group is m2m, we need to save a copy of it
                # before adding any biomes, country, etc...
                location_group.save()
                
                for location_def in location_data['Locations']:

                    relational_kwargs = ['Forest_type', 'Country', 'Country_3166_3', 
                                         'Division_BAILEY', 'Biome_UDVARDY', 'Biome_WWF', 'Biome_FAO']
                    location_kwargs = {}
                    for key in location_def.keys():
                        if key not in relational_kwargs:
                            location_kwargs[key] = location_def[key]

                    location = location_models.Location.objects.create(**location_kwargs)


                    if 'Biome_FAO' in location_def.keys() and location_def['Biome_FAO']['Name']:
                        location.Biome_FAO = location_models.BiomeFAO.objects.get(Name=location_def['Biome_FAO']['Name'])
                  
                    if 'Biome_WWF' in location_def.keys() and location_def['Biome_WWF']['Name']:
                        location.Biome_WWF = location_models.BiomeWWF.objects.get(Name=location_def['Biome_WWF']['Name'])
                   
                    if 'Biome_UDVARDY' in location_def.keys() and location_def['Biome_UDVARDY']['Name']:
                        location.Biome_UDVARDY = location_models.BiomeUdvardy.objects.get(Name=location_def['Biome_UDVARDY']['Name'])
                   
                    if 'Biome_HOLDRIDGE' in location_def.keys() and location_def['Biome_HOLDRIDGE']['Name']:
                        location.Biome_HOLDRIDGE = location_models.BiomeHoldridge.objects.get(Name=location_def['Biome_HOLDRIDGE']['Name'])

                    if 'Division_BAILEY' in location_def.keys() and location_def['Division_BAILEY']['Name']:
                        location.Division_BAILEY = location_models.DivisionBailey.objects.get(Name=location_def['Division_BAILEY']['Name'])
                    
                    if 'Country_3166_3' in location_def.keys() and location_def['Country_3166_3']:
                        location.Country = location_models.Country.objects.get(Iso3166a3=location_def['Country_3166_3'])
                    elif 'Country' in location_def.keys() and location_def['Country']['Formal_name']:
                        location.Country = location_models.Country.objects.get(Formal_name=location_def['Country']['Formal_name'])

                    if 'Forest_type' in location_def.keys() and location_def['Forest_type']['Name']:
                        location.Forest_type = location_models.ForestType.objects.get(Name=location_def['Forest_type']['Name'])
                       
                    location.save()
                    location_group.Locations.add(location)
           
        instance.Reference = source_models.Reference.objects.get_or_create(**reference_data)[0]

        if 'dataset' in self.context.keys():
            instance.Dataset = self.context['dataset']

        instance.save()

        return instance


    def to_representation(self, obj):
        # Here we figure out if the user has access to this data object
        # through a data sharing agreement or since the object is permitted
        # to all users
        from globallometree.apps.data_sharing.data_tools import restrict_access
        record = super(LinkedModelSerializer, self).to_representation(obj)
        
        if 'request' in self.context.keys():
            return restrict_access(record, self.elasticsearch_index_name, self.context['request'].user)
        else:
            return record

class AllometricEquationSerializer(LinkedModelSerializer):
    elasticsearch_index_name = 'allometricequation'

    def __init__(self, *args, **kwargs):
        super(AllometricEquationSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        
        if validated_data['Population']['Name']:
            validated_data['Population'] = allometric_equation_models.Population.objects.get(Name=validated_data['Population']['Name'])
        else:
            validated_data['Population'] = None

        if validated_data['Tree_type']['Name']:
            validated_data['Tree_type'] = allometric_equation_models.TreeType.objects.get(Name=validated_data['Tree_type']['Name'])
        else:
            validated_data['Tree_type'] = None

        return super(AllometricEquationSerializer, self).create(validated_data)

    Population = fields.ChoiceField(
        source='Population.Name', 
        allow_null=True,
        choices= [pop.Name for pop in allometric_equation_models.Population.objects.all()]
        )

    Tree_type = fields.ChoiceField(
        source='Tree_type.Name', 
        allow_null=True,
        choices=[tt.Name for tt in allometric_equation_models.TreeType.objects.all()]
        )

    class Meta:
        model = allometric_equation_models.AllometricEquation
        exclude = ('Created', 'Modified')


class WoodDensitySerializer(LinkedModelSerializer):
    elasticsearch_index_name = 'wooddensity'
    class Meta:
        model = wood_density_models.WoodDensity
        exclude = ('Created', 'Modified', )


class RawDataSerializer(LinkedModelSerializer):
    elasticsearch_index_name = 'rawdata'
    class Meta:
        model = raw_data_models.RawData
        exclude = ('Created', 'Modified', )


class BiomassExpansionFactorSerializer(LinkedModelSerializer):
    elasticsearch_index_name = 'biomassexpansionfactor'
    class Meta:
        model = biomass_expansion_factors_models.BiomassExpansionFactor
        exclude = ('Created', 'Modified', )


