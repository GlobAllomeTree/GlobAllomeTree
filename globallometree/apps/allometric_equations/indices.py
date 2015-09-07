import re
import json

from django.conf import settings

from elasticutils.contrib.django import Indexable, MappingType, get_es

from globallometree.apps.allometric_equations.models import AllometricEquation
from globallometree.apps.base.estypes import *
from globallometree.apps.api.serializers import AllometricEquationSerializer
from globallometree.apps.api.renderers import JSONRenderer

class AllometricEquationIndex(MappingType, Indexable):

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
    def get_indexable(cls):
        #return a queryset of models that should be indexed
        return cls.get_model().objects.all().order_by('pk')

    @classmethod
    def get_mapping(cls):
        """Returns an Elasticsearch mapping for this MappingType"""

        mapping = {
            "properties": {
                    "ID_AE": estype_long,
                    "ID_AE_original": estype_long,
                    "B": estype_boolean,
                    "Bd": estype_boolean,
                    "Bg": estype_boolean,
                    "Bias_correction": estype_float,
                    "Bt": estype_boolean,
                    "Contributor": estype_string_not_analyzed,
                    "Corrected_for_bias": estype_boolean,
                    "Equation": estype_string_not_analyzed,
                    "F": estype_boolean,
                    "L": estype_boolean,
                    "Max_X": estype_float,
                    "Min_X": estype_float,
                    "Max_Z": estype_float,
                    "Min_Z": estype_float,
                    "Output": estype_string_not_analyzed,
                    "Output_TR": estype_string_not_analyzed,
                    "Population": estype_string_not_analyzed,
                    "R2": estype_float,
                    "R2_Adjusted": estype_float,
                    "RMSE": estype_float,
                    "SEE": estype_float,
                    "Rb": estype_boolean,
                    "Rf": estype_boolean,
                    "Rm": estype_boolean,
                    "S": estype_boolean,
                    "Sample_size": estype_string_not_analyzed,
                    "Segmented_equation": estype_boolean,
                    "Stump_height": estype_float,
                    "Top_dob" : estype_float,
                    "Substitute_equation": estype_string_not_analyzed,
                    "T": estype_boolean,
                    "Unit_W": estype_string_not_analyzed,
                    "Unit_X": estype_string_not_analyzed,
                    "Unit_Y": estype_string_not_analyzed,
                    "Veg_Component": estype_string_not_analyzed,
                    "X": estype_string_not_analyzed,
                    
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

        obj_serialized = AllometricEquationSerializer(obj).data
        return obj_serialized

    

       