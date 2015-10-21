import codecs
from django.db import models
from rest_framework.renderers import *
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer, BaseRenderer
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

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
    Renderer which serializes to Unicode UTF-16 txt (excel fotmat for unicode)
    """
    media_type = 'text/tsv'
    format = 'txt'
    charset = 'utf-16-le'

    shared_headers = ["Vegetation_type",
                         "Tree_type",
                       # "ID_Location",
                        "Location",
                        "Region",
                        "Country",
                        "Country_3166_3",
                        "Continent",
                        "Zone_FAO",
                        "Zone_Holdridge",
                        "Ecoregion_Udvardy",
                        "Ecoregion_WWF",
                        "Division_Bailey",
                        #"Geohash",
                        "Latitude",
                        "Longitude",
                        #"LatLonString",
                        #"ID_Zone_FAO",
                        #"ID_Ecoregion_Udvardy",
                        #"ID_Zone_Holdridge",
                        #"id_Ecoregion_WWF",
                        #"ID_Division_Bailey",
                        #"ID_Country",
                        #"ID_Continent",
                        #"ID_Vegetation_type",
                       'Family',
                       'Genus',
                       'Species',
                       'Subspecies',
                       'Species_author', 
                       #'ID_Family', 
                       #'ID_Genus',
                       #'ID_Species', 
                       #'ID_Subspecies',
                       'Species_local_name', 
                       'Species_local_name_iso', 
                       'Species_local_name_latin', 
                       #'ID_Local_name',
                       'Reference_author',
                       'Reference_year',
                       'Reference',
                       #'ID_Reference',
                       'Operator',
                       'Contributor',
                       'Remark',
                       'Contact'
                    ]

    def __init__(self, *args, **kwargs):
        self.headers = []
        return super(CSVRenderer, self).__init__(*args, **kwargs)


    def render(self, data, media_type=None, renderer_context=None, writer_opts=None):
        """
        Renders serialized *data* into CSV. For a dictionary:
        """
        if data is None:
            yield ''

        if writer_opts is None:
            writer_opts = {}

        if isinstance(data, dict) and 'results' in data.keys():
            data = data['results']
        elif isinstance(data, dict):
            data = [data]

        self.add_headers(data[0])
       
        table = self.tablize(data)

        is_first_line = True
        for row in table:
            line = (u'\t'.join([
                unicode(elem) for elem in row
            ]) + u'\r\n').encode('utf-16-le')

            if is_first_line:
                yield codecs.BOM_UTF16_LE + line
                is_first_line = False
            else:
                yield line 


    def tablize(self, data):
        rows = []
        csv_rows = []

        for line in data:
            nested_rows_added = False
            
            line = dict(line)

            # Call to equation, bef, wood density, etc...
            if 'Source' in line.keys():
                reference = line['Source']
                line.update({
                    'Reference_author': reference['Reference_author'],
                    'Reference_year': reference['Reference_year'],
                    'Reference': reference['Reference'],
                   # 'ID_Reference': reference['ID_Reference']
                    })

            # Direct call to the species group api endpoint
            if 'ID_Species_group' in line.keys():
                for item in line['Group']:
                    nested_rows_added = True
                    rows += self.get_species_definition_rows(dict(item), line)

            # Call to equation, bef, wood density, etc...
            if 'Species_group' in line.keys():
                species_group = line['Species_group']
                line.update({'ID_Species_group': species_group['ID_Species_group']})
                for item in species_group['Group']:
                    nested_rows_added = True
                    rows += self.get_species_definition_rows(dict(item), line)

            # Direct call to the location group api endpoint
            if 'ID_Location_group' in line.keys():
                for item in line['Group']:
                    nested_rows_added = True
                    rows += self.get_location_rows(dict(item), line)

            # Call to equation, bef, wood density, etc...
            if 'Location_group' in line.keys():
                location_group = line['Location_group']
                line.update({'ID_Location_group': location_group['ID_Location_group']})
                for item in location_group.pop('Group'):
                    nested_rows_added = True
                    rows += self.get_location_rows(dict(item), line)

            # Call to species, or subspecies
            if 'Species_local_names' in line.keys():
                species_local_names = line['Species_local_names']
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
        if type(species_local_names) == list and len(species_local_names):
            for local_name in species_local_names:
                row = context.copy()
                row.update({
                        'Species_local_name': local_name['Local_name'], 
                        'Species_local_name_iso': local_name['Language_iso_639'], 
                        'Species_local_name_latin': local_name['Local_name_latin']
                    })
                rows.append(row)
        return rows


    def add_headers(self, sample_record):

        # Add the headers in a logical way
        
        component_headers =  ['B','Bd', 'Bg', 'Bt', 'L', 'Rb', 'Rf', 'Rm', 'S', 'T', 'F' ]
        record_keys = sample_record.keys()

        skip_headers = (self.shared_headers + 
                        component_headers +
                       ['Group', 
                        'Species_local_names',
                        'Species_group',
                        'Reference',
                        'Location_group',
                        'Dataset',
                        'LatLonString',
                        'Geohash',
                        'Source',
                        'Created',
                        'Modified',
                        'Elasticsearch_doc_hash',  
                        ])

        if 'ID_AE' in record_keys:
            model = models.get_model('allometric_equations', 'AllometricEquation')
        elif 'ID_WD' in record_keys:
            model = models.get_model('wood_densities', 'WoodDensity')
        elif 'ID_RD' in record_keys:
            model = models.get_model('raw_data', 'RawData')  
        elif 'ID_BME' in record_keys:
            model = models.get_model('biomass_expansion_factors', 'BiomassExpansionFactor')   


        for field in model._meta.fields:
            if field.name not in skip_headers:
                self.headers.append(field.name)

        has_components = True
        for field in component_headers:
            if field not in record_keys:
                has_components = False
        if has_components:
            self.headers += component_headers

        self.headers += self.shared_headers

