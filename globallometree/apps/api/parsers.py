import os
import re

from django.conf import settings
from rest_framework.parsers import BaseParser
from rest_framework.exceptions import ParseError

tab_re = re.compile('\t')

def universal_newlines(stream):
    for intermediate_line in stream:
        # It's possible that the stream was not opened in universal
        # newline mode. If not, we may have a single "row" that has a
        # bunch of carriage return (\r) characters that should act as
        # newlines. For that case, lets call splitlines on the row. If
        # it doesn't have any newlines, it will return a list of just
        # the row itself.
        for line in intermediate_line.splitlines():
            yield line


class CSVParser(BaseParser):
    """
    Parses CSV serialized data.

    The parser assumes the first line contains the column names.
    """

    media_type = 'text/txt'


    def __init__(self, data_type):
        self.data_type = data_type

        self.conversions =   {
            'Ecoregion_Udvardy': {},
            'Zone_FAO': {},
            'Ecoregion_WWF': {},
            'Division_Bailey': {},
            'Country': {},
            'Zone_Holdridge' : {}
            }

        conversion_files =  {
            'Ecoregion_Udvardy': 'apps/api/resources/conversions_udvardy.csv',
            'Zone_FAO': 'apps/api/resources/conversions_fao.csv' ,
            'Ecoregion_WWF': 'apps/api/resources/conversions_wwf.csv',
            'Division_Bailey': 'apps/api/resources/conversions_bailey.csv',
            'Country': 'apps/api/resources/conversions_country.csv',
            'Zone_Holdridge':'apps/api/resources/conversions_holdridge.csv',
            }

        for conversion_key in conversion_files.keys():

            conversion_file = open(os.path.join(settings.PROJECT_PATH, conversion_files[conversion_key]), "r")
            for line in universal_newlines(conversion_file):
                from_val, to_val = line.split(';')
                self.conversions[conversion_key][from_val] = to_val


    def ensure_local_name_in_list(self,species_local_name, species_groups, definition_index, ID_Species_group):
        found = False
        for local_name in species_groups[ID_Species_group][definition_index]['Species_local_names']:
            if local_name["Local_name"] == species_local_name["Local_name"] and \
               local_name["Language_iso_639"] == species_local_name["Language_iso_639"] and \
               local_name["Local_name_latin"] == species_local_name["Local_name_latin"]:
                found = True
        if not found:
            species_groups[ID_Species_group][definition_index]['Species_local_names'].append(species_local_name)


    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
       
        primary_key_fields = {
            'raw_data': 'ID_RD',
            'biomass_expansion': 'ID_BEF', 
            'wood_density': 'ID_WD',
            'allometric_equations': 'ID_AE' 
        }

        id_field = primary_key_fields[self.data_type]

        # Anything in either location groups or species groups
        # that is required, we set to null so that it isn't required to 
        # guess what fields are present and which aren't
        defaults_to_null = [
            'Zone_Holdridge',
            'Ecoregion_Udvardy',
            'Zone_FAO',
            'Ecoregion_WWF',
            'Division_Bailey',
            'Latitude',
            'Longitude',
            'Country',
            'Region',
            'Vegetation_type',
            'Location',
            'Contributor',
            'Operator',
            'ID_Location_group',
            'Population',
            'Ecosystem',
            'Continent',
            'ID_Species_group',
            'Genus',
            'Species',
            'Family',
            'Species_local_name',
            'Species_local_name_latin',
            'Species_local_name_iso',
            'Species_author',
            'Reference_author',
            'Reference_year',
            'Reference',
            'Family',
            'Genus',
            'Species',
            'Subspecies',
            'Tree_type',
            'Vegetation_type',
        ]

        next_record_auto_id = 10000000
        next_location_auto_id = 1000000000
        next_species_auto_id = 1000000000
        location_groups = {}
        species_groups = {}
        data = []
        records = {}

        # A single record is represented by seeral csv row
        # Each csv row might add a species definition, a new location, or a new species local name

        rows = []

        for line in unicode(stream.read(), 'utf16').splitlines():
            # Fix escaped quotes
            line = line.replace('""', '"')
            # Ignore empty lines
            if not tab_re.match(line):
                row = line.split('\t')
                rows.append(row)

        header = rows.pop(0)
        
        for row in rows:
            row_data = dict(zip(header, row))

            for key in row_data.keys():
                row_data[key] = row_data[key].strip()

                # Unquote text fields
                if row_data[key].startswith('"') and row_data[key].endswith('"'):
                    row_data[key] = row_data[key][1:-1]

                if key in self.conversions.keys() and \
                  row_data[key] in self.conversions[key].keys():
                    row_data[key] = self.conversions[key][row_data[key]]

                if row_data[key] in ['NA', 'na', 'sp.', "", "None"]:
                    row_data[key] = None
                    
                elif row_data[key] in ['TRUE', 'True', 'true', "YES", "Yes", "yes"]:
                    row_data[key] = True
                
                elif row_data[key] in ['FALSE', 'False', 'false', "NO", "No", "no"]:
                    row_data[key] = False

            for key in defaults_to_null:
                if not key in row_data.keys():
                    row_data[key] = None;

            if not row_data['ID_Location_group']:
                row_data['ID_Location_group'] = next_location_auto_id
                next_location_auto_id += 1

            if not row_data['ID_Species_group']:
                row_data['ID_Species_group'] = next_species_auto_id
                next_species_auto_id += 1

            if not id_field in row_data.keys() or not row_data[id_field]:
                row_data[id_field] = next_record_auto_id
                next_record_auto_id += 1

            ID_Location_group = row_data['ID_Location_group']
            ID_Species_group = row_data['ID_Species_group']
            Record_ID = row_data[id_field]

            if row_data['Family'] is None: row_data['Family'] = 'Unknown'
            if row_data['Genus'] is None: row_data['Genus'] = 'Unknown'
            if row_data['Species'] is None: row_data['Species'] = 'unknown'

            location_definition =  {
                'Zone_Holdridge': row_data.pop("Zone_Holdridge"),       
                'Zone_FAO': row_data.pop("Zone_FAO"),
                'Ecoregion_WWF': row_data.pop("Ecoregion_WWF"),
                'Ecoregion_Udvardy': row_data.pop("Ecoregion_Udvardy"),
                'Division_Bailey': row_data.pop('Division_Bailey'),
                'Country': row_data.pop("Country"),
                'Region': row_data.pop("Region"),
                'Location': row_data.pop("Location"),
                'Latitude': row_data.pop("Latitude"),
                'Longitude': row_data.pop("Longitude")
            }

            if not ID_Location_group in location_groups.keys():
                location_groups[ID_Location_group] = []

            if not location_definition in location_groups[ID_Location_group]:
                location_groups[ID_Location_group].append(location_definition)

            species_definition =    {
                'Family': row_data.pop("Family"),
                'Genus': row_data.pop("Genus"),
                'Species': row_data.pop("Species"),
                'Subspecies': row_data.pop("Subspecies"),
                'Species_author': row_data.pop("Species_author"),
                'Species_local_names' : []
            }

            if not ID_Species_group in species_groups.keys():
                species_groups[ID_Species_group] = []

            definition_index = None
            for index, sd in enumerate(species_groups[ID_Species_group]):
                if sd['Family'] == species_definition['Family'] and \
                   sd['Genus'] == species_definition['Genus'] and \
                   sd['Species'] == species_definition['Species'] and \
                   sd['Genus'] == species_definition['Genus'] and \
                   sd['Species_author'] == species_definition['Species_author']:
                    definition_index = index

            if definition_index is None:
                species_groups[ID_Species_group].append(species_definition)
                definition_index = len(species_groups[ID_Species_group]) - 1

            if row_data['Species_local_name']:
                species_local_name = {
                    "Local_name" : row_data.pop('Species_local_name'),
                    "Language_iso_639" : row_data.pop('Species_local_name_iso'),
                    "Local_name_latin": row_data.pop('Species_local_name_latin')
                }

                self.ensure_local_name_in_list(species_local_name = species_local_name,
                                               species_groups = species_groups,
                                               definition_index = definition_index,
                                               ID_Species_group = ID_Species_group)
            
            row_data['Source'] = {
                "Reference_author": row_data.pop("Reference_author"), 
                "Reference_year": row_data.pop("Reference_year"), 
                "Reference": row_data.pop("Reference")
            }

            #Group repeated records by ID
            records[Record_ID] = row_data

        for record_key in records.keys():

            row_data = records.pop(record_key)

            row_data['Location_group'] = {
                'Group' : location_groups[row_data['ID_Location_group']],
                'ID_Location_group' : row_data['ID_Location_group']
            }
            row_data.pop('ID_Location_group')

            row_data['Species_group'] = {
                'Group' : species_groups[row_data['ID_Species_group']],
                'ID_Species_group' : row_data['ID_Species_group']
            }
            row_data.pop('ID_Species_group')

            data.append(row_data)

        return data

        
