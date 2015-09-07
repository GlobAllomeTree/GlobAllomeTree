from __future__ import unicode_literals

import csv
from six import StringIO, text_type

from rest_framework.renderers import *
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer, BaseRenderer
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

# six versions 1.3.0 and previous don't have PY2
try:
    from six import PY2
except ImportError:
    import sys
    PY2 = sys.version_info[0] == 2


class JSONRenderer(JSONRenderer):
    format='json'

    def get_indent(self, accepted_media_type, renderer_context):
        return 4


class XMLRenderer(XMLRenderer):
    format='xml'


class BrowsableAPIRenderer(BrowsableAPIRenderer):
    format='api'
    
    def get_context(self, *args, **kwargs):
        context = super(BrowsableAPIRenderer, self).get_context(*args, **kwargs)
        context["display_edit_forms"] = False  
        return context


class OrderedRows(list):
    """
    Maintains original header/field ordering.
    """
    def __init__(self, header):
        self.header = [c.strip() for c in header] if (header is not None) else None


class CSVRenderer(BaseRenderer):
    """
    Renderer which serializes to CSV
    """
    media_type = 'text/csv'
    format = 'csv'
   
    def __init__(self, *args, **kwargs):
        self.headers = []
        return super(CSVRenderer, self).__init__(*args, **kwargs)

    def render(self, data, media_type=None, renderer_context=None, writer_opts=None):
        """
        Renders serialized *data* into CSV. For a dictionary:
        """
        if data is None:
            return ''

        if writer_opts is None:
            writer_opts = {}

        table = self.tablize(data)

        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer, delimiter=str('\t'), **writer_opts)
        for row in table:
            # Assume that strings should be encoded as UTF-8
            csv_writer.writerow([
                elem.encode('utf-8') if isinstance(elem, text_type) and PY2 else elem
                for elem in row
            ])

        return csv_buffer.getvalue()

    def tablize(self, data):
        rows = []
        csv_rows = []

        skip_headers = ['Group', 
                        'Species_local_names',
                        'Species_group',
                        'Reference',
                        'Location_group',
                        'Dataset',
                        'LatLonString',
                        'Geohash',
                        ]

        if isinstance(data, dict) and 'results' in data.keys():
            data = data['results']
        elif isinstance(data, dict):
            data = [data]

        for line in data:
            nested_rows_added = False
            for key in line.keys():
                if key not in self.headers and key not in skip_headers:
                    self.headers.append(key)
            line = dict(line)

            # Call to equation, bef, wood density, etc...
            if 'Reference' in line.keys():
                reference = line.pop('Reference')
                self.add_reference_headers()
                line.update({
                    'Reference_author': reference['Author'],
                    'Reference_year': reference['Year'],
                    'Reference': reference['Reference'],
                   # 'ID_Reference': reference['ID_Reference']
                    })

            # Direct call to the species group api endpoint
            if 'ID_Species_group' in line.keys():
                self.add_species_definition_headers()
                for item in line.pop('Group'):
                    nested_rows_added = True
                    rows += self.get_species_definition_rows(dict(item), line)

            # Call to equation, bef, wood density, etc...
            if 'Species_group' in line.keys():
                self.add_species_definition_headers()
                species_group = line.pop('Species_group')
                line.update({'ID_Species_group': species_group.pop('ID_Species_group')})
                for item in species_group.pop('Group'):
                    nested_rows_added = True
                    rows += self.get_species_definition_rows(dict(item), line)

            # Direct call to the location group api endpoint
            if 'ID_Location_group' in line.keys():
                self.add_location_headers()
                for item in line.pop('Group'):
                    nested_rows_added = True
                    rows += self.get_location_rows(dict(item), line)

            # Call to equation, bef, wood density, etc...
            if 'Location_group' in line.keys():
                self.add_location_headers()
                location_group = line.pop('Location_group')
                line.update({'ID_Location_group': location_group.pop('ID_Location_group')})
                for item in location_group.pop('Group'):
                    nested_rows_added = True
                    rows += self.get_location_rows(dict(item), line)

            # Call to species, or subspecies
            if 'Species_local_names' in line.keys():
                species_local_names = line.pop('Species_local_names')
                nested_rows = self.get_species_local_name_rows(species_local_names, line)
                if len(nested_rows):
                    nested_rows_added = True
                rows += nested_rows
            
            if not nested_rows_added:    
                rows.append(line)


        csv_rows.append(self.headers)

        for row in rows:
            csv_row = []
            for header in self.headers:
                if header in row.keys() and row[header] is not None:
                    csv_row.append(row[header])
                else:
                    csv_row.append('NA')
            csv_rows.append(csv_row)

        # Need to zip up headers and rows here
        return csv_rows

    def get_species_definition_rows(self, species_definition, context):
        rows = []
        species_local_names = species_definition.pop('Species_local_names')
        context.update(species_definition)
        rows = rows + self.get_species_local_name_rows(species_local_names, context)
        return rows

    def get_location_rows(self, location, context):
        row = context.copy()
        row.update(location)
        return [row]


    def get_species_local_name_rows(self, species_local_names, context):
        rows = []
        self.add_species_local_name_headers()
        if type(species_local_names) == list and len(species_local_names):
            for local_name in species_local_names:
                row = context.copy()
                row.update({
                        'Species_local_name': local_name['Local_name'], 
                        'Species_local_name_iso': local_name['Language_iso_639'], 
                        'Species_local_name_latin': local_name['Local_name_latin'], 
                        'ID_Local_name': local_name['Local_name_ID'], 
                    })
                rows.append(row)

        return rows

    def add_location_headers(self):
        if 'ID_Location' not in self.headers:
            self.headers += [
                               # "ID_Location",
                                "Location_name",
                                "Plot_name",
                                "Plot_size_m2",
                                "Commune",
                                "Province",
                                "Region",
                                "Country",
                                "Country_3166_3",
                                "Continent",
                                "Zone_FAO",
                                "Zone_Holdridge",
                                "Ecoregion_Udvardy",
                                "Ecoregion_WWF",
                                "Division_Bailey",
                                "Vegetation_type",
                                #"Geohash",
                                "Latitude",
                                "Longitude",
                                #"LatLonString",
                                #"ID_Zone_FAO",
                                #"ID_Ecoregion_Udvardy",
                                #"ID_Zone_Holdridge",
                                #"id_ecoregion_wwf",
                                #"ID_Division_Bailey",
                                #"ID_Country",
                                #"ID_Continent",
                                #"ID_Vegetation_type"
                               ]

    def add_species_definition_headers(self):
        if 'Family' not in self.headers:
            self.headers += [
                           'Family',
                           'Genus',
                           'Species',
                           'Subspecies',
                           'Species_author', 
                           #'ID_Family', 
                           #'ID_Genus',
                           #'ID_Species', 
                           #'ID_Subspecies'
                           ]
        self.add_species_local_name_headers()

    def add_species_local_name_headers(self):
        if 'Species_local_name' not in self.headers:
            self.headers += [
                           'Species_local_name', 
                           'Species_local_name_iso', 
                           'Species_local_name_latin', 
                           #'ID_Local_name',
                           ]

    def add_reference_headers(self):
        if 'Reference' not in self.headers:
            self.headers += [
                'Reference_author',
                'Reference_year',
                'Reference',
                #'ID_Reference',
                ]

