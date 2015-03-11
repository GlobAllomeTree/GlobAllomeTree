import re
import json

from django.conf import settings

from elasticutils.contrib.django import Indexable, MappingType, get_es

from ..models import RawData
from globallometree.apps.search_helpers.estypes import *
from globallometree.apps.api.serializers import SimpleRawDataSerializer
from globallometree.apps.api.renderers import SimpleJSONRenderer

class RawDataIndex(MappingType, Indexable):

    @classmethod
    def get_index(cls):
        return 'globallometree'

    @classmethod
    def get_mapping_type_name(cls):
        return 'rawdata'

    @classmethod
    def get_model(cls):
        """Returns the Django model this MappingType relates to"""
        return RawData

    @classmethod
    def get_indexable(cls):
        #return a queryset of models that should be indexed
        return cls.get_model().objects.all()

    @classmethod
    def get_mapping(cls):
        """Returns an Elasticsearch mapping for this MappingType"""

        mapping = {
            "properties": {
                "Raw_data_ID": estype_long,
                "H_tree_avg": estype_float,
                "Plot_ID": estype_long,
                "Forest_type": estype_string_not_analyzed,
                "Tree_ID": estype_long,
                "Date_collection": estype_date,
                "DBH_cm": estype_float,
                "H_m": estype_float,
                "CD_m": estype_float,
                "F_Bole_kg": estype_float,
                "F_Branch_kg": estype_float,
                "F_Foliage_kg": estype_float,
                "F_Stump_kg": estype_float,
                "F_Buttress_kg": estype_float,
                "F_Roots_kg": estype_float,
                "Volume_m3": estype_float,
                "Volume_bole_m3": estype_float,
                "WD_AVG_gcm3": estype_float,
                "DF_Bole_AVG": estype_float,
                "DF_Branch_AVG": estype_float,
                "DF_Foliage_AVG": estype_float,
                "DF_Stump_AVG": estype_float,
                "DF_Buttress_AVG": estype_float,
                "DF_Roots_AVG": estype_float,
                "D_Bole_kg": estype_float,
                "D_Branch_kg": estype_float,
                "D_Foliage_kg": estype_float,
                "D_Stump_kg": estype_float,
                "D_Buttress_kg": estype_float,
                "D_Roots_kg": estype_float,
                "ABG_kg": estype_float,
                "BGB_kg": estype_float,
                "Tot_Biomass_kg": estype_float,
                "BEF": estype_float
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

        obj_serialized = SimpleRawDataSerializer(obj)
        json_string = SimpleJSONRenderer().render(obj_serialized.data)
        return json.loads(json_string)




