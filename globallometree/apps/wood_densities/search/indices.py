import re
import json

from django.conf import settings

from elasticutils.contrib.django import Indexable, MappingType, get_es

from ..models import WoodDensity
from globallometree.apps.search_helpers.estypes import *
from globallometree.apps.api.serializers import SimpleWoodDensitySerializer
from globallometree.apps.api.renderers import SimpleJSONRenderer

class WoodDensityIndex(MappingType, Indexable):

    @classmethod
    def get_index(cls):
        return 'globallometree'

    @classmethod
    def get_mapping_type_name(cls):
        return 'wooddensity'

    @classmethod
    def get_model(cls):
        """Returns the Django model this MappingType relates to"""
        return WoodDensity

    @classmethod
    def get_indexable(cls):
        #return a queryset of models that should be indexed
        return cls.get_model().objects.all()

    @classmethod
    def get_mapping(cls):
        """Returns an Elasticsearch mapping for this MappingType"""

        mapping = {
            "properties": {
                    "Wood_density_ID": estype_long,
                    "H_tree_avg": estype_float,
                    "H_tree_min": estype_float,
                    "H_tree_max": estype_float,
                    "DBH_tree_avg": estype_float,
                    "DBH_tree_min": estype_float,
                    "DBH_tree_max": estype_float,
                    "m_WD": estype_float,
                    "MC_m": estype_float,
                    "V_WD": estype_float,
                    "MC_V": estype_float,
                    "CR": estype_float,
                    "FSP": estype_float,
                    "Methodology": estype_string_not_analyzed,
                    "Bark": estype_boolean,
                    "Density_g_cm3": estype_float,
                    "MC_Density": estype_string_not_analyzed,
                    "Data_origin": estype_string_not_analyzed,
                    "Data_type": estype_string_not_analyzed,
                    "Samples_per_tree": estype_long,
                    "Number_of_trees": estype_long,
                    "SD": estype_float,
                    "Min": estype_float,
                    "Max": estype_float,
                    "H_measure": estype_float,
                    "Bark_distance": estype_float
                }
            }

        return mapping


    @classmethod
    def extract_document(cls, obj_id=None, obj=None):
        """Converts this instance into an Elasticsearch document"""
        if not obj_id and not obj:
            raise('Must call extract_document with obj or obj_id')

        if obj is None:
            obj = cls.get_model().objects.get(pk=obj_id)

        obj_serialized = SimpleWoodDensitySerializer(obj)
        json_string = SimpleJSONRenderer().render(obj_serialized.data)
        return json.loads(json_string)




