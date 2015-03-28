
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_csv.renderers import CSVRenderer
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


class CSVRenderer(CSVRenderer):
    format='csv'
    # expand_lists = 'vertical'
    # sort_headers = False

    # def get_data(self, data):
    #     if type(data) == ReturnDict:
    #         data = dict(data)
    #         return data['results']
    #     if type(data) == ReturnList:
    #         data = [data]
    #     return data
