
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework.renderers import XMLRenderer
from rest_framework_csv.renderers import CSVRenderer


class SimpleJSONRenderer(JSONRenderer):
	format='json'


class SimpleXMLRenderer(XMLRenderer):
	format='xml'


class SimpleBrowsableAPIRenderer(BrowsableAPIRenderer):
	format='api'


class SimpleCSVRenderer(CSVRenderer):
	format='csv'


class FullJSONRenderer(JSONRenderer):
	format='json-full'


class FullXMLRenderer(XMLRenderer):
	format='xml-full'


class FullBrowsableAPIRenderer(BrowsableAPIRenderer):
	format='api-full'


