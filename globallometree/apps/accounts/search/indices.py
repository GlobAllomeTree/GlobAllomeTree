import re

from django.conf import settings

from elasticutils.contrib.django import Indexable, MappingType, get_es

from globallometree.apps.common.estypes import *

from ..models import UserProfile

class UserProfileIndex(MappingType, Indexable):

    @classmethod
    def get_index(cls):
        return 'globallometree'

    @classmethod
    def get_mapping_type_name(cls):
        return 'userprofile'

    @classmethod
    def get_model(cls):
        """Returns the Django model this MappingType relates to"""
        return UserProfile

    @classmethod
    def get_indexable(cls):
        #return a queryset of models that should be indexed
        return cls.get_model().objects.exclude(location_privacy='none')

    @classmethod
    def get_mapping(cls):
        """Returns an Elasticsearch mapping for this MappingType"""
        mapping = {
            'properties': {
                'ID':  estype_integer,
                'Name' :  estype_string_not_analyzed,
                'Institution_name' : estype_string_not_analyzed,
                'Country' : estype_string_not_analyzed,

                #utility
                'anonymous' : estype_boolean,

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

        document = {}
        #Create the document dynamically using the mapping, obj, and prepare methods
        for field in cls.get_mapping()['properties'].keys():
            document[field] = cls.get_field_value(obj, field)
            
        return document

    @classmethod
    def freeze(cls, d):
        if isinstance(d, dict):
            return frozenset((key, cls.freeze(value)) for key, value in d.items())
        elif isinstance(d, list):
            return tuple(cls.freeze(value) for value in d)
        return d

    @classmethod
    def get_field_value(cls, obj, field):
        prepare_method_name = 'prepare_%s' % field
            
        #If this class has a prepare_FOO method for field FOO, use that method
        if hasattr(cls, prepare_method_name):
            method = getattr(cls, prepare_method_name)
            return method(obj)
        #If the object has a FOO property, use the object's FOO
        elif hasattr(obj, field):
            return getattr(obj, field)
        else:
            raise Exception("No model field or prepare method found for field %s" % field)

    @classmethod
    def prepare_Name(cls, obj):
        return obj.user.get_full_name()

    @classmethod
    def prepare_Institution_name(cls, obj):
        return obj.user.get_full_name()

    @classmethod
    def prepare_Country(cls, obj):
        return obj.location_country.common_name

    @classmethod
    def prepare_anonymous(cls, obj):
        return obj.location_privacy == 'anonymous'

 