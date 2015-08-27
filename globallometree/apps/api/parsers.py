import csv
import codecs
import io
import six

from django.conf import settings
from rest_framework.parsers import BaseParser
from rest_framework.exceptions import ParseError


def preprocess_stream(stream, charset):
    #if six.PY2:
        # csv.py doesn't do Unicode; encode temporarily:
        return (chunk.encode(charset) for chunk in stream)
    #else:
    #    return stream

def postprocess_row(row, charset):
    #if six.PY2:
        # decode back to Unicode, cell by cell:
        return [cell.decode(charset) for cell in row]
    #else:
    #    return row

def unicode_csv_reader(csv_data, dialect=csv.excel, charset='utf-8', **kwargs):
    csv_data = preprocess_stream(csv_data, charset)
    csv_reader = csv.reader(csv_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield postprocess_row(row, charset)

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

    media_type = 'text/csv'


    def __init__(self, data_type):
        self.data_type = data_type


    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        delimiter = parser_context.get('delimiter', '\t')

        primary_key_fields = {
            'raw_data': 'Raw_data_ID',
            'biomass_expansion': 'Biomass_expansion_factor_ID', 
            'wood_density': 'Wood_density_ID',
            'allometric_equations': 'Allometric_equation_ID' 
        }

        convert_v1_headers = {
            'Label': 'Reference_label',
            'Author': 'Reference_author',               
            'Year': 'Reference_year',      
            'ID_Location': 'Location_ID',
            'Group_Location': 'Location_group_ID',
            'Biome_FAO': 'Zone_FAO',
            'Biome_UDVARDY': 'Ecoregion_Udvardy',
            'Biome_WWF': 'Ecoregion_WWF',
            'Division_BAILEY': 'Division_Bailey',
            'Biome_HOLDRIDGE': 'Zone_Holdridge',
            'ID_Species': 'Species_ID',
            'ID_Group': 'Species_group_ID',
            'Name_operator': 'Operator',
            'ID_Equation': 'Allometric_equation_ID'
        }

        id_field = primary_key_fields[self.data_type]

        # Anything in either location groups or species groups
        # that is required, we set to null so that it isn't required to 
        # guess what fields are present and which aren't
        defaults_to_null = [
            'Plot_name',
            'Plot_size_m2',
            'Zone_Holdridge',
            'Ecoregion_Udvardy',
            'Zone_FAO',
            'Ecoregion_WWF',
            'Division_Bailey',
            'Latitude',
            'Longitude',
            'Country',
            'Region',
            'Forest_type',
            'Location',
            'Contributor',
            'Operator',
            'Location_group_ID',
            'Population',
            'Ecosystem',
            'Continent',
            'Species_group_ID',
            'Genus',
            'Species',
            'Family',
            'Label',
            'Author',
            'Year',
            'Reference',
            'Family',
            'Genus',
            'Species',
            'Subspecies',
            'Tree_type'
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

        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        rows = unicode_csv_reader(universal_newlines(stream), delimiter=delimiter, charset=encoding)
        
        header = next(rows)
        
        for index, item in enumerate(header):
            if item in convert_v1_headers.keys():
                header[index] = convert_v1_headers[item]

        for row in rows:
            row_data = dict(zip(header, row))


            for key in row_data.keys():
                row_data[key] = row_data[key].strip()
                if row_data[key] in ['NA', 'na', 'sp.', "", "None"]:
                    row_data[key] = None
                    
                if row_data[key] in ['TRUE', 'True', 'true', "YES", "Yes", "yes"]:
                    row_data[key] = True
                
                if row_data[key] in ['FALSE', 'False', 'false', "NO", "No", "no"]:
                    row_data[key] = False

            for key in defaults_to_null:
                if not key in row_data.keys():
                    row_data[key] = None;

            if not row_data['Location_group_ID']:
                row_data['Location_group_ID'] = next_location_auto_id
                next_location_auto_id += 1

            if not row_data['Species_group_ID']:
                row_data['Species_group_ID'] = next_species_auto_id
                next_species_auto_id += 1

            if not id_field in row_data.keys() or not row_data[id_field]:
                row_data[id_field] = next_record_auto_id
                next_record_auto_id += 1

            Location_group_ID = row_data['Location_group_ID']
            Species_group_ID = row_data['Species_group_ID']
            Record_ID = row_data[id_field]

            if row_data['Family'] is None: row_data['Family'] = 'Unknown'
            if row_data['Genus'] is None: row_data['Genus'] = 'Unknown'
            if row_data['Species'] is None: row_data['Species'] = 'unknown'

            location_definition =  {
                'Plot_name': row_data.pop("Plot_name"),
                'Plot_size_m2': row_data.pop("Plot_size_m2"),
                'Zone_Holdridge': row_data.pop("Zone_Holdridge"),       
                'Zone_FAO': row_data.pop("Zone_FAO"),
                'Ecoregion_WWF': row_data.pop("Ecoregion_WWF"),
                'Ecoregion_Udvardy': row_data.pop("Ecoregion_Udvardy"),
                'Division_Bailey': row_data.pop('Division_Bailey'),
                'Country': row_data.pop("Country"),
                'Region': row_data.pop("Region"),
                'Forest_type': row_data.pop("Forest_type"),
                'Location_name': row_data.pop("Location"),
                'Latitude': row_data.pop("Latitude"),
                'Longitude': row_data.pop("Longitude")
            }

            if not Location_group_ID in location_groups.keys():
                location_groups[Location_group_ID] = []

            if not location_definition in location_groups[Location_group_ID]:
                location_groups[Location_group_ID].append(location_definition)

            species_definition =    {
                'Family': row_data.pop("Family"),
                'Genus': row_data.pop("Genus"),
                'Species': row_data.pop("Species"),
                'Subspecies': row_data.pop("Subspecies")
            }

            if not Species_group_ID in species_groups.keys():
                species_groups[Species_group_ID] = []

            if not species_definition in species_groups[Species_group_ID]:
                species_groups[Species_group_ID].append(species_definition)

            row_data['Reference'] = {
                "Label": row_data.pop("Label"), 
                "Author": row_data.pop("Author"), 
                "Year": row_data.pop("Year"), 
                "Reference": row_data.pop("Reference")
            }

            #Group repeated records by ID
            records[Record_ID] = row_data

        for record_key in records.keys():

            row_data = records.pop(record_key)

            row_data['Location_group'] = {
                'Group' : location_groups[row_data['Location_group_ID']],
                'Location_group_ID' : row_data['Location_group_ID']
            }
            row_data.pop('Location_group_ID')

            row_data['Species_group'] = {
                'Group' : species_groups[row_data['Species_group_ID']],
                'Species_group_ID' : row_data['Species_group_ID']
            }
            row_data.pop('Species_group_ID')

            data.append(row_data)

        return data

        
