
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
            'Species': cls.get_species(obj),
            'Locations' : cls.get_locations(obj)
            }


    @classmethod
    def get_species(cls, obj):
        species_list = []
        for species in obj.species_group.species.all():
            species_list.append(species.name)
        return species_list

    @classmethod
    def get_locations(cls, obj):
        locations = []
        for location in obj.location_group.locations.all():
            locations.append({
                "lat" : location.Latitude,
                "lon" : location.Longitude
            })
        return locations


    @classmethod
    def get_indexable(cls):
        return cls.get_model().objects.iterator()

