
from django.conf import settings

from elasticutils import get_es
from elasticutils.contrib.django import Indexable, MappingType

from .models import AllometricEquation

class AllometricEquationIndex(MappingType, Indexable):
    @classmethod
    def get_es(cls):
        return get_es(urls=settings.ELASTICSEARCH_URLS)

    @classmethod
    def get_index(cls):
        return 'globallometree'

    @classmethod
    def get_mapping_type_name(cls):
        return 'allometricequation'

    @classmethod
    def get_model(cls):
        """Returns the Django model this MappingType relates to"""
        return AllometricEquation

    @classmethod
    def get_mapping(cls):
        """Returns an Elasticsearch mapping for this MappingType"""
        return {
            'properties': {
                # The id is an integer, so store it as such. Elasticsearch
                # would have inferred this just fine.
                'ID': {'type': 'integer'},

                'Population' : {'type': 'string', 
                               'index': 'not_analyzed'},

                'Ecosystem' : {'type': 'string', 
                              'index': 'not_analyzed'},

                'Genus' : {'type': 'string',                           
                           'index': 'not_analyzed'},

                # The species is a name---so we shouldn't analyze it
                # (de-stem, tokenize, parse, etc).
                'Species': {'type': 'string', 
                            'index': 'not_analyzed'},
                            
                'Locations' : {'type': 'geo_point',
                               'geohash': True,
                               'geohash_prefix': True,
                               'geohash_precision': 8
                               }
            }
        }

    @classmethod
    def extract_document(cls, obj_id=None, obj=None):
        """Converts this instance into an Elasticsearch document"""
        if not obj_id and not obj:
            raise('Must call extract_document with obj or obj_id')

        if obj is None:
            obj = cls.get_model().objects.get(pk=obj_id)

        return {
            'ID': obj.ID,
            'Population' : cls.prepare_Population(obj),
            'Ecosystem' : cls.prepare_Ecosystem(obj),
            'Genus' : cls.prepare_Genus(obj),
            'Species': cls.prepare_Species(obj),
            'Locations' : cls.prepare_Locations(obj)
            }


    @classmethod
    def get_species(cls, obj):
        species_list = []
        for species in obj.species_group.species.all():
            species_list.append(species.name)
        return species_list

   
    @classmethod
    def get_indexable(cls):
        return cls.get_model().objects.iterator()

    @classmethod
    def prepare_ecosystem_name(cls, obj):
        return None if obj.ecosystem is None else obj.ecosystem.name

    @classmethod
    def prepare_population_name(cls, obj):
        return None if obj.population is None else obj.population.name

    @classmethod
    def prepare_Species(cls, obj):
        return [species.name for species in obj.species_group.species.all()]

    @classmethod
    def prepare_Genus(cls, obj):
        return [
            genus.name for genus in
            [species.genus for species in obj.species_group.species.all()]
            if genus is not None
        ]

    @classmethod
    def prepare_Country(cls, obj):
        return [
            country.common_name for country in [
                location.country for location in
                obj.location_group.locations.all()
            ] if country is not None
        ]

    @classmethod
    def prepare_Biome_FAO(cls, obj):
        return [
            biome_fao.name for biome_fao in [
                location.biome_fao for location in
                obj.location_group.locations.all()
            ] if biome_fao is not None
        ]

    @classmethod
    def prepare_Biome_UDVARDY(cls, obj):
        return [
            biome_udvardy.name for biome_udvardy in [
                location.biome_udvardy for location in
                obj.location_group.locations.all()
            ] if biome_udvardy is not None
        ]
    
    @classmethod
    def prepare_Biome_WWF(cls, obj):
        return [
            biome_wwf.name for biome_wwf in [
                location.biome_wwf for location in
                obj.location_group.locations.all()
            ] if biome_wwf is not None
        ]

    @classmethod
    def prepare_Division_BAILEY(cls, obj):
        return [
            division_bailey.name for division_bailey in [
                    location.division_bailey for location in
                    obj.location_group.locations.all()
            ] if division_bailey is not None
        ]

    @classmethod
    def prepare_Biome_HOLDRIDGE(cls, obj):
        return [
            biome_holdridge.name for biome_holdridge in [
                location.biome_holdridge for location in
                obj.location_group.locations.all()
            ] if biome_holdridge is not None
        ]

    @classmethod
    def get_Locations(cls, obj):
        locations = []
        for location in obj.location_group.locations.all():
            locations.append({
                "lat" : location.Latitude,
                "lon" : location.Longitude
            })
        return locations

