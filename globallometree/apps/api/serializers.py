## api/views.py

from collections import OrderedDict
from django.contrib.auth.models import User
from django.db import transaction

from rest_framework import serializers, fields

from globallometree.apps.source import models as source_models
from globallometree.apps.allometric_equations import models as allometric_equation_models
from globallometree.apps.wood_densities import models as wood_density_models 
from globallometree.apps.raw_data import models as raw_data_models
from globallometree.apps.biomass_expansion_factors import models as biomass_expansion_factors_models
from globallometree.apps.locations import models as location_models
from globallometree.apps.taxonomy import models as taxonomy_models
from globallometree.apps.base import models as base_models

from globallometree.apps.api.serializers_location import (
    ZoneFAOSerializer, 
    EcoregionUdvardySerializer, 
    EcoregionWWFSerializer, 
    DivisionBaileySerializer, 
    ZoneHoldridgeSerializer,
    VegetationTypeSerializer,
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

from globallometree.apps.api.validators import ValidRelatedField

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
        fields = ('Author', 'Year', 'Reference', 'ID_Reference')

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
    Dataset = DatasetSerializer(many=False, read_only=True)
    Reference = ReferenceSerializer(many=False, required=False)
    Contributor = fields.CharField(source='Contributor.Name', allow_null=True, required=False)
    Operator = fields.CharField(source='Operator.Name', allow_null=True, required=False)

    Tree_type = fields.CharField(
        source='Tree_type.Name', 
        allow_null=True,
        validators=[ValidRelatedField(model=base_models.TreeType, 
                                      field_name="Name")]
        )

    def __init__(self, *args, **kwargs):
        super(LinkedModelSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        with transaction.atomic():
            species_data = validated_data.pop('Species_group')
            location_data = validated_data.pop('Location_group')
            reference_data = validated_data.pop('Reference')
            contributor_data = validated_data.pop('Contributor')
            operator_data = validated_data.pop('Operator')

            ModelClass = self.Meta.model

            if validated_data['Tree_type']['Name']:
                validated_data['Tree_type'] = base_models.TreeType.objects.get(Name=validated_data['Tree_type']['Name'])
            else:
                validated_data['Tree_type'] = None

            instance = ModelClass.objects.create(**validated_data)

            species_data['ID_Species_group'] = species_data['ID_Species_group'] + 13

            if contributor_data and contributor_data['Name']:
                instance.Contributor = source_models.Institution.objects.get_or_create(Name=contributor_data['Name'])[0]
            
                if operator_data and operator_data['Name']:
                    instance.Operator = source_models.Operator.objects.get_or_create(Name=operator_data['Name'],
                                                                                     Institution=instance.Contributor)[0]
            if species_data:
                species_group, created = taxonomy_models.SpeciesGroup.objects.get_or_create(
                    Dataset=self.context['dataset'],
                    ID_Dataset_Species_group=species_data['ID_Species_group']
                    )

                instance.Species_group = species_group
                # First time we have seen this species group so we save all the details
                # otherwise we assume that it's repeated data of the same group
                if created:

                    # Since the species group is m2m, we need to save a copy of it
                    # before adding any species
                    species_group.save()
                    for species_def in species_data['Species_definitions']:

                        family = None
                        genus = None
                        species = None
                        subspecies = None

                        # create any needed taxonomy models
                        # when there is not an id, but there is a name,
                        # it indicates we need to create the model
                        if species_def['Family']['Name']:
                            family = taxonomy_models.Family.objects.get_or_create(
                                Name=species_def['Family']['Name'])[0]
                        
                            if species_def['Genus']['Name']:
                                genus = taxonomy_models.Genus.objects.get_or_create(
                                    Name=species_def['Genus']['Name'], 
                                    Family=family)[0]

                                if species_def['Species']['Name']:
                                    
                                    if species_def['Species_author']:
                                        if species_def['Subspecies']['Name']:
                                            subspecies_author = species_def['Species_author']
                                            species_author = None
                                        elif species_def['Species']['Name']:
                                            subspecies_author = None
                                            species_author = species_def['Species_author']
                                    else:
                                        species_author = None
                                        subspecies_author = None

                                    species = taxonomy_models.Species.objects.get_or_create(
                                                Name=species_def['Species']['Name'], 
                                                Genus=genus,
                                                Author=species_author
                                                )[0]
                        
                                    for sln in species_def['Species']['Local_names']:
                                        species_local_name = taxonomy_models.SpeciesLocalName.objects.get_or_create(
                                            Species = species,
                                            Local_name=sln['Local_name'],
                                            Local_name_latin=sln['Local_name_latin'],
                                            Language_iso_639_3=sln['Language_iso_639_3']
                                            )

                                    if species_def['Subspecies']['Name']:
                                        subspecies = taxonomy_models.Subspecies.objects.get_or_create(
                                            Name=species_def['Subspecies']['Name'], 
                                            Species=species,
                                            Author=subspecies_author)[0]


                        species_def_model = taxonomy_models.SpeciesDefinition(
                            Family=family,
                            Genus=genus,
                            Species=species,
                            Subspecies=subspecies
                            )

                        species_def_model.save()
                        species_group.Species_definitions.add(species_def_model)      


            if location_data:
                location_group, created = location_models.LocationGroup.objects.get_or_create(
                    Dataset=self.context['dataset'],
                    Dataset_ID_Location_group=location_data['ID_Location_group']
                    )
                instance.Location_group = location_group
                # First time we have seen this location group so we save all the details
                # otherwise we assume that it's repeated data of the same group
                if created:
                    # Since the location group is m2m, we need to save a copy of it
                    # before adding any biomes, country, etc...
                    location_group.save()
                    
                    for location_def in location_data['Locations']:

                        relational_kwargs = ['Vegetation_type', 'Country', 'Country_3166_3', 
                                             'Division_Bailey', 'Ecoregion_Udvardy', 'Ecoregion_WWF', 'Zone_FAO', 'Zone_Holdridge']
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

                        if 'Division_Bailey' in location_def.keys() and location_def['Division_Bailey']['Name']:
                            location.Division_Bailey = location_models.DivisionBailey.objects.get(Name=location_def['Division_Bailey']['Name'])
                        
                        if 'Country_3166_3' in location_def.keys() and location_def['Country_3166_3']:
                            location.Country = location_models.Country.objects.get(Iso3166a3=location_def['Country_3166_3'])
                        elif 'Country' in location_def.keys() and location_def['Country']['Formal_name']:
                            location.Country = location_models.Country.objects.get(Formal_name=location_def['Country']['Formal_name'])

                        if 'Vegetation_type' in location_def.keys() and location_def['Vegetation_type']['Name']:
                            location.Vegetation_type = location_models.VegetationType.objects.get(Name=location_def['Vegetation_type']['Name'])
                           
                        location.save()
                        location_group.Locations.add(location)
               
            instance.Reference = source_models.Reference.objects.get_or_create(**reference_data)[0]

            if 'dataset' in self.context.keys():
                instance.Dataset = self.context['dataset']
                self.context['dataset'].Records_imported += 1
                self.context['dataset'].save()
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


        return super(AllometricEquationSerializer, self).create(validated_data)

    Population = fields.CharField(
        source='Population.Name', 
        allow_null=True,
        validators=[ValidRelatedField(model=allometric_equation_models.Population, 
                                      field_name="Name")]
        )

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


