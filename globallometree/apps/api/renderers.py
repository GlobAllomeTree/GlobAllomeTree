
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework.renderers import XMLRenderer
from rest_framework_csv.renderers import CSVRenderer
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

class SimpleJSONRenderer(JSONRenderer):
    format='json'


class SimpleXMLRenderer(XMLRenderer):
    format='xml'


class SimpleBrowsableAPIRenderer(BrowsableAPIRenderer):
    format='api'


class SimpleCSVRenderer(CSVRenderer):
    expand_lists = 'vertical'
    sort_headers = False

    def get_data(self, data):
        if type(data) == ReturnDict:
            data = dict(data)
            return data['results']
        if type(data) == ReturnList:
            data = [data]
        return data


class FullJSONRenderer(JSONRenderer):
    format='json-full'


class FullXMLRenderer(XMLRenderer):
    format='xml-full'


class FullBrowsableAPIRenderer(BrowsableAPIRenderer):
    format='api-full'


