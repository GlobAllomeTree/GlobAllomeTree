
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_csv.renderers import CSVRenderer
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

class SimpleJSONRenderer(JSONRenderer):
    format='json'

    def get_indent(self, accepted_media_type, renderer_context):
        return 4


class SimpleXMLRenderer(XMLRenderer):
    format='xml'


class SimpleBrowsableAPIRenderer(BrowsableAPIRenderer):
    format='api'
    
    def get_context(self, *args, **kwargs):
        context = super(SimpleBrowsableAPIRenderer, self).get_context(*args, **kwargs)
        context["display_edit_forms"] = False  
        return context



class SimpleCSVRenderer(CSVRenderer):
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


class FullJSONRenderer(JSONRenderer):
    format='json-full'


class FullXMLRenderer(XMLRenderer):
    format='xml-full'


class FullBrowsableAPIRenderer(BrowsableAPIRenderer):
    format='api-full'
    display_edit_forms=False

    def get_context(self, *args, **kwargs):
        context = super(FullBrowsableAPIRenderer, self).get_context(*args, **kwargs)
        context["display_edit_forms"] = False  
        return context

