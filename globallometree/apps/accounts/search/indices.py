import re

from django.conf import settings

from elasticutils.contrib.django import Indexable, MappingType, get_es

from globallometree.apps.search_helpers.estypes import *

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
        return cls.get_model().objects.exclude(privacy='none')

    @classmethod
    def get_mapping(cls):
        """Returns an Elasticsearch mapping for this MappingType"""
        mapping = {
            'properties': {
                'id':  estype_integer,
                'Name' :  estype_string_not_analyzed,
                'Institution_name' : estype_string_not_analyzed,
                'Country' : estype_string_not_analyzed,
                "ID_Country": estype_long,
                'Country_3166_3' :  estype_string_not_analyzed,
                "Latitude": estype_float,
                "Longitude": estype_float,
                "LatLonString": estype_string_not_analyzed,
                "Geohash": estype_geopoint_geohash,

                #utility
                'anonymous' : estype_boolean,
                'has_precise_location' : estype_boolean
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

        if obj.privacy == 'anonymous':
            #Use a more limited set of fields for the anonymous index
            for field in ['id', 
                          'Institution_name', 
                          'Country', 
                          'Country_3166_3',
                          "Latitude",
                          "Longitude",
                          "LatLonString",
                          "Geohash"
                          ]:
                document[field] = cls.get_field_value(obj, field)
        else:
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
    def prepare_ID(cls, obj):
        return obj.user.pk

    @classmethod
    def prepare_Name(cls, obj):
        return obj.user.get_full_name()

    @classmethod
    def prepare_Institution_name(cls, obj):
        return obj.institution_name

    @classmethod
    def prepare_Country(cls, obj):
        if obj.location_country:
            return obj.location_country.Common_name
        else:
            return None

    @classmethod
    def prepare_Country_3166_3(cls, obj):
        if obj.location_country:
            return obj.location_country.Iso3166a3
        else:
            return None


    @classmethod
    def prepare_Geohash(cls, obj):
        if obj.location_latitude:
            return {
                        "lat" : obj.location_latitude,
                        "lon" : obj.location_longitude
                    }

    @classmethod
    def prepare_Latitude(cls, obj):
        return obj.location_latitude
    
    @classmethod
    def prepare_Longitude(cls, obj):
        return obj.location_longitude

    @classmethod
    def prepare_LatLonString(cls, obj):
        if obj.location_latitude:
            lat_lon_string = "%s,%s" % (obj.location_latitude,obj.location_longitude)
        else:
            lat_lon_string = None  
        return lat_lon_string

    @classmethod
    def prepare_anonymous(cls, obj):
        return obj.privacy == 'anonymous'


 