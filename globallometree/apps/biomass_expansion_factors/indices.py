import re
import json

from django.conf import settings

from elasticutils.contrib.django import Indexable, MappingType, get_es

from globallometree.apps.biomass_expansion_factors.models import BiomassExpansionFactor
from globallometree.apps.base.estypes import *
from globallometree.apps.api.serializers import BiomassExpansionFactorSerializer
from globallometree.apps.api.renderers import JSONRenderer

class BiomassExpansionFactorIndex(MappingType, Indexable):

    @classmethod
    def get_index(cls):
        return 'globallometree'

    @classmethod
    def get_mapping_type_name(cls):
        return 'biomassexpansionfactor'

    @classmethod
    def get_model(cls):
        """Returns the Django model this MappingType relates to"""
        return BiomassExpansionFactor

    @classmethod
    def get_indexable(cls):
        #return a queryset of models that should be indexed
        return cls.get_model().objects.all()

    @classmethod
    def get_mapping(cls):
        """Returns an Elasticsearch mapping for this MappingType"""

        mapping = {
            "properties": {
                "ID_BEF": estype_long,
                "Growing_stock": estype_float,
                "Aboveground_biomass": estype_float,
                "Net_annual_increment": estype_float,
                "Stand_density": estype_float,
                "Age": estype_long,
                "BEF": estype_float,
                "Input": estype_string_not_analyzed,
                "Output": estype_string_not_analyzed,
                "Internal_validity": estype_long
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

        obj_serialized = BiomassExpansionFactorSerializer(obj)
        json_string = JSONRenderer().render(obj_serialized.data)
        return json.loads(json_string)




