
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


class CSVRenderer(BaseRenderer):
    format='csv'
    media_type='text/csv'

    def render(self, data, media_type=None, renderer_context=None):
        return data.encode(self.charset)
