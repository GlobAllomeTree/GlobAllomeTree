
from django.conf import settings

from elasticutils.contrib.django import Indexable, MappingType, get_es

from ..models import AllometricEquation

estypes = {
    'boolean' : {'type': 'boolean'},

    'integer' : {'type': 'integer'},

    'float' : { 'type' : 'float' },

    'long' : { 'type' : 'long'},

    'double' : { 'type' : 'double' },

    'string_not_analyzed' : {'type': 'string', 
                             'index': 'not_analyzed'},

    'geopoint_geohashed' : {'type': 'geo_point',
                            'geohash': True,
                            'geohash_prefix': True,
                            'geohash_precision': 8
                            },
}

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
    def get_mapping(cls):
        """Returns an Elasticsearch mapping for this MappingType"""
        return {
            'properties': {
                'ID':               estypes.integer,
                'Population' :      estypes.string_not_analyzed,
                'Ecosystem' :       estypes.string_not_analyzed,
                'Genus' :           estypes.string_not_analyzed,
                'Species':          estypes.string_not_analyzed,
                'Locations' :       estypes.geopoint_geohashed,
                'Country' :         estypes.string_not_analyzed,
                'Biome_FAO' :       estypes.string_not_analyzed,
                'Biome_UDVARDY' :   estypes.string_not_analyzed,
                'Biome_WWF' :       estypes.string_not_analyzed,
                'Division_BAILEY' : estypes.string_not_analyzed,
                'Biome_HOLDRIDGE' : estypes.string_not_analyzed,
                'X' :               estypes.string_not_analyzed, 
                'Unit_X' :          estypes.string_not_analyzed, 
                'Z' :               estypes.string_not_analyzed, 
                'Unit_Z' :          estypes.string_not_analyzed, 
                'W' :               estypes.string_not_analyzed, 
                'Unit_W' :          estypes.string_not_analyzed, 
                'U' :               estypes.string_not_analyzed, 
                'Unit_U' :          estypes.string_not_analyzed, 
                'V' :               estypes.string_not_analyzed, 
                'Unit_V' :          estypes.string_not_analyzed, 
                'Min_X' :           estypes.float, 
                'Max_X' :           estypes.float,
                'Min_Z' :           estypes.float, 
                'Max_Z' :           estypes.float, 
                'Output' :          estypes.string_not_analyzed, 
                'Unit_Y' :          estypes.string_not_analyzed,
                'B' :               estypes.boolean, 
                'Bd' :              estypes.boolean,
                'Bg' :              estypes.boolean, 
                'Bt' :              estypes.boolean,
                'L' :               estypes.boolean,
                'Rb' :              estypes.boolean, 
                'Rf' :              estypes.boolean, 
                'Rm' :              estypes.boolean, 
                'S' :               estypes.boolean, 
                'T' :               estypes.boolean, 
                'F' :               estypes.boolean, 
                'Equation' :        estypes.string_not_analyzed, 
                'Author' :          estypes.string_not_analyzed,
                'Year' :            estypes.string_not_analyzed,
                'Reference' :       estypes.string_not_analyzed
            }
        }
   

    @classmethod
    def extract_document(cls, obj_id=None, obj=None):
        """Converts this instance into an Elasticsearch document"""
        if not obj_id and not obj:
            raise('Must call extract_document with obj or obj_id')

        if obj is None:
            obj = cls.get_model().objects.get(pk=obj_id)

        for field in cls.get_mapping()['properties'].keys():
            print field

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
        return cls.get_model().objects.all()

    @classmethod
    def prepare_Ecosystem(cls, obj):
        return None if obj.ecosystem is None else obj.ecosystem.name

    @classmethod
    def prepare_Population(cls, obj):
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
    def prepare_Locations(cls, obj):
        locations = []
        for location in obj.location_group.locations.all():
            locations.append({
                "lat" : location.Latitude,
                "lon" : location.Longitude
            })
        return locations

