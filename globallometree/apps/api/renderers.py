
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework.renderers import XMLRenderer
from rest_framework_csv.renderers import CSVRenderer


class SimpleJSONRenderer(JSONRenderer):
	format='simple-json'


class SimpleXMLRenderer(XMLRenderer):
	format='simple-xml'


class SimpleBrowsableAPIRenderer(BrowsableAPIRenderer):
	format='simple-api'


class SimpleCSVRenderer(CSVRenderer):
	format='simple-csv'

