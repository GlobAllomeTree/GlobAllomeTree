import re

from django.conf import settings

from elasticutils.contrib.django import Indexable, MappingType, get_es

from ..models import AllometricEquation
from .estypes import *

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
        return cls.get_model().objects.all()

    @classmethod
    def get_mapping(cls):
        """Returns an Elasticsearch mapping for this MappingType"""
        mapping = {
            'properties': {
                'ID':               estype_integer,
                'Population' :      estype_string_not_analyzed,
                'Ecosystem' :       estype_string_not_analyzed,
                'Genus' :           estype_string_not_analyzed,
                'Species':          estype_string_not_analyzed,
                'Genus_Species':    estype_string_not_analyzed,
                'Locations' :       estype_geopoint_geohashed,
                'Country' :         estype_string_not_analyzed,
                'Country_3166_3' :  estype_string_not_analyzed,
                'Biome_FAO' :       estype_string_not_analyzed,
                'Biome_UDVARDY' :   estype_string_not_analyzed,
                'Biome_WWF' :       estype_string_not_analyzed,
                'Division_BAILEY' : estype_string_not_analyzed,
                'Biome_HOLDRIDGE' : estype_string_not_analyzed,
                'X' :               estype_string_not_analyzed, 
                'Unit_X' :          estype_string_not_analyzed, 
                'Z' :               estype_string_not_analyzed, 
                'Unit_Z' :          estype_string_not_analyzed, 
                'W' :               estype_string_not_analyzed, 
                'Unit_W' :          estype_string_not_analyzed, 
                'U' :               estype_string_not_analyzed, 
                'Unit_U' :          estype_string_not_analyzed, 
                'V' :               estype_string_not_analyzed, 
                'Unit_V' :          estype_string_not_analyzed, 
                'Min_X' :           estype_float, 
                'Max_X' :           estype_float,
                'Min_Z' :           estype_float, 
                'Max_Z' :           estype_float, 
                'Output' :          estype_string_not_analyzed, 
                'Unit_Y' :          estype_string_not_analyzed,
                'B' :               estype_boolean, 
                'Bd' :              estype_boolean,
                'Bg' :              estype_boolean, 
                'Bt' :              estype_boolean,
                'L' :               estype_boolean,
                'Rb' :              estype_boolean, 
                'Rf' :              estype_boolean, 
                'Rm' :              estype_boolean, 
                'S' :               estype_boolean, 
                'T' :               estype_boolean, 
                'F' :               estype_boolean, 
                'Equation' :        estype_string_not_analyzed, 
                'Author' :          estype_string_not_analyzed,
                'Year' :            estype_integer,
                'Reference' :       estype_string_not_analyzed,

                #utility
                'has_precise_location' :        estype_boolean,

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
    def prepare_Ecosystem(cls, obj):
        return None if obj.ecosystem is None else obj.ecosystem.name

    @classmethod
    def prepare_Population(cls, obj):
        return None if obj.population is None else obj.population.name

    @classmethod
    def prepare_Species(cls, obj):

        return list(set([species.name for species in obj.species_group.species.all()]))

    @classmethod
    def prepare_Genus(cls, obj):
        return list(set([
            genus.name for genus in
            [species.genus for species in obj.species_group.species.all()]
            if genus is not None
        ]))

    @classmethod
    def prepare_Genus_Species(cls, obj):
        #Combined list of Genus and Species
        species_genus = [];

        for species in obj.species_group.species.all():
            if species.genus:
                name = u"%s %s" % (species.genus.name, species.name)
            else:
                name = species.name
            species_genus.append(name)
        return list(set(species_genus))


    @classmethod
    def prepare_Country(cls, obj):
        return list(set([
            country.common_name for country in [
                location.country for location in
                obj.location_group.locations.all()
            ] if country is not None
        ]))

    @classmethod
    def prepare_Country_3166_3(cls, obj):
        return list(set([
            country.iso3166a3 for country in [
                location.country for location in
                obj.location_group.locations.all()
            ] if country is not None
        ]))

    @classmethod
    def prepare_Biome_FAO(cls, obj):
        return list(set([
            biome_fao.name for biome_fao in [
                location.biome_fao for location in
                obj.location_group.locations.all()
            ] if biome_fao is not None
        ]))

    @classmethod
    def prepare_Biome_UDVARDY(cls, obj):
        return list(set([
            biome_udvardy.name for biome_udvardy in [
                location.biome_udvardy for location in
                obj.location_group.locations.all()
            ] if biome_udvardy is not None
        ]))
    
    @classmethod
    def prepare_Biome_WWF(cls, obj):
        return list(set([
            biome_wwf.name for biome_wwf in [
                location.biome_wwf for location in
                obj.location_group.locations.all()
            ] if biome_wwf is not None
        ]))

    @classmethod
    def prepare_Division_BAILEY(cls, obj):
        return list(set([
            division_bailey.name for division_bailey in [
                    location.division_bailey for location in
                    obj.location_group.locations.all()
            ] if division_bailey is not None
        ]))

    @classmethod
    def prepare_Biome_HOLDRIDGE(cls, obj):
        return list(set([
            biome_holdridge.name for biome_holdridge in [
                location.biome_holdridge for location in
                obj.location_group.locations.all()
            ] if biome_holdridge is not None
        ]))

    @classmethod
    def prepare_Locations(cls, obj):
        if hasattr(obj, '_locations_cache'):
            return obj._locations_cache

        locations = []
        for location in obj.location_group.locations.all():

            if not location.Latitude or not location.Longitude:
                #locations can just be countries or biomes
                #so in that case we just skip over the object
                continue

            #dicts do not work with unique sets
            if not any(l == {'lat' : location.Latitude,  'lon' : location.Longitude} for l in locations):
                locations.append({
                    "lat" : location.Latitude,
                    "lon" : location.Longitude
                })
        obj._locations_cache = locations
        return locations

    @classmethod
    def prepare_Author(cls, obj):
        return obj.reference.author

    @classmethod
    def prepare_Reference(cls, obj):
        return obj.reference.reference

    @classmethod
    def prepare_Year(cls, obj):
        if obj.reference.year:
            return list(set(re.findall(r'\d{4}', obj.reference.year)))
        return None
    
    @classmethod
    def prepare_has_precise_location(cls, obj):
        if len(cls.prepare_Locations(obj)):
            return True
        else:
            return False

       