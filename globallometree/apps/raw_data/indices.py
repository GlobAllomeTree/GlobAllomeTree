import re
import json

from django.conf import settings

from elasticutils.contrib.django import Indexable, MappingType, get_es

from globallometree.apps.raw_data.models import RawData
from globallometree.apps.search_helpers.estypes import *
from globallometree.apps.api.serializers import RawDataSerializer
from globallometree.apps.api.renderers import JSONRenderer

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
                "D_Bole_kg": estype_float,
                "D_Branch_kg": estype_float,
                "D_Foliage_kg": estype_float,
                "D_Stump_kg": estype_float,
                "D_Buttress_kg": estype_float,
                "D_Roots_kg": estype_float,
                "ABG_kg": estype_float,
                "BGB_kg": estype_float,
                "Tot_Biomass_kg": estype_float,
                }
            }

        mapping['properties'].update(estype_linked_model)

        return mapping


    @classmethod
    def extract_document(cls, obj_id=None, obj=None):
        """Converts this instance into an Elasticsearch document"""
        if not obj_id and not obj:
            raise('Must call extract_document with obj or obj_id')

        if obj is None:
            obj = cls.get_model().objects.get(pk=obj_id)

        obj_serialized = RawDataSerializer(obj)
        json_string = JSONRenderer().render(obj_serialized.data)
        return json.loads(json_string)




