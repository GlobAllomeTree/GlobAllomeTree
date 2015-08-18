## api/views.py

from collections import OrderedDict
from django.contrib.auth.models import User

from rest_framework import serializers, fields

from globallometree.apps.source import models as source_models
from globallometree.apps.allometric_equations import models as allometric_equation_models
from globallometree.apps.wood_densities import models as wood_density_models 
from globallometree.apps.raw_data import models as raw_data_models
from globallometree.apps.biomass_expansion_factors import models as biomass_expansion_factors_models
from globallometree.apps.locations import models as location_models
from globallometree.apps.taxonomy import models as taxonomy_models


from globallometree.apps.api.serializers_location import (
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

from globallometree.apps.api.serializers_taxonomy import (
    GenusSerializer,
    FamilySerializer,
    SpeciesSerializer,
    SubspeciesSerializer,
    SpeciesLocalNameSerializer,
    SpeciesGroupSerializer
    )

from globallometree.apps.api.serializers_data_sharing import (
    DataLicenseSerializer,
    DatasetSerializer,
    )

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = source_models.Institution
        fields = ('Name',)


class PopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = allometric_equation_models.Population
        fields = ('Name',)


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
            species_group, created = taxonomy_models.SpeciesGroup.objects.get_or_create(
                Dataset=self.context['dataset'],
                Dataset_Species_group_ID=species_data['Species_group_ID']
                )

            instance.Species_group = species_group
            # First time we have seen this species group so we save all the details
            # otherwise we assume that it's repeated data of the same group
            if created:

                # Since the species group is m2m, we need to save a copy of it
                # before adding any species
                species_group.save()
                for species_def in species_data['Species_definitions']:

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

                    species_def = taxonomy_models.SpeciesDefinition(
                        Family=family,
                        Genus=genus,
                        Species=species,
                        Subspecies=subspecies
                        )

                    species_def.save()
                    species_group.Species_definitions.add(species_def)      


        if location_data:
            location_group, created = location_models.LocationGroup.objects.get_or_create(
                Dataset=self.context['dataset'],
                Dataset_Location_group_ID=location_data['Location_group_ID']
                )
            instance.Location_group = location_group
            # First time we have seen this location group so we save all the details
            # otherwise we assume that it's repeated data of the same group
            if created:
                # Since the location group is m2m, we need to save a copy of it
                # before adding any biomes, country, etc...
                location_group.save()
                
                for location_def in location_data['Locations']:

                    relational_kwargs = ['Forest_type', 'Country', 'Country_3166_3', 
                                         'Division_BAILEY', 'Ecoregion_Udvardy', 'Ecoregion_WWF', 'Zone_FAO']
                    location_kwargs = {}
                    for key in location_def.keys():
                        if key not in relational_kwargs:
                            location_kwargs[key] = location_def[key]

                    location = location_models.Location.objects.create(**location_kwargs)


                    if 'Zone_FAO' in location_def.keys() and location_def['Zone_FAO']['Name']:
                        location.Zone_FAO = location_models.ZoneFAO.objects.get(Name=location_def['Zone_FAO']['Name'])
                  
                    if 'Ecoregion_WWF' in location_def.keys() and location_def['Ecoregion_WWF']['Name']:
                        location.Ecoregion_WWF = location_models.EcoregionWWF.objects.get(Name=location_def['Ecoregion_WWF']['Name'])
                   
                    if 'Ecoregion_Udvardy' in location_def.keys() and location_def['Ecoregion_Udvardy']['Name']:
                        location.Ecoregion_Udvardy = location_models.EcoregionUdvardy.objects.get(Name=location_def['Ecoregion_Udvardy']['Name'])
                   
                    if 'Zone_Holdridge' in location_def.keys() and location_def['Zone_Holdridge']['Name']:
                        location.Zone_Holdridge = location_models.ZoneHoldridge.objects.get(Name=location_def['Zone_Holdridge']['Name'])

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
        choices= []
        )

    Tree_type = fields.ChoiceField(
        source='Tree_type.Name', 
        allow_null=True,
        choices=[]
        )

    def get_fields(self, *args, **kwargs):
        fields = super(AllometricEquationSerializer, self).get_fields(*args, **kwargs)
        fields['Population'].choices = [pop.Name for pop in allometric_equation_models.Population.objects.all()]
        fields['Tree_type'].choices = [tt.Name for tt in allometric_equation_models.TreeType.objects.all()]
        return fields

    class Meta:
        model = allometric_equation_models.AllometricEquation
        exclude = ('Created', 'Modified', 'Elasticsearch_doc_hash')


class WoodDensitySerializer(LinkedModelSerializer):
    elasticsearch_index_name = 'wooddensity'
    class Meta:
        model = wood_density_models.WoodDensity
        exclude = ('Created', 'Modified', 'Elasticsearch_doc_hash')


class RawDataSerializer(LinkedModelSerializer):
    elasticsearch_index_name = 'rawdata'
    class Meta:
        model = raw_data_models.RawData
        exclude = ('Created', 'Modified', 'Elasticsearch_doc_hash')


class BiomassExpansionFactorSerializer(LinkedModelSerializer):
    elasticsearch_index_name = 'biomassexpansionfactor'
    class Meta:
        model = biomass_expansion_factors_models.BiomassExpansionFactor
        exclude = ('Created', 'Modified', 'Elasticsearch_doc_hash')


