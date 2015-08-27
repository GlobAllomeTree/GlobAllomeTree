
from .serializers import (
    AllometricEquationSerializer,
    WoodDensitySerializer,
    RawDataSerializer,
    BiomassExpansionFactorSerializer
)

from .renderers import (
    JSONRenderer,
    XMLRenderer,
    CSVRenderer
)

from .parsers import CSVParser

from rest_framework.parsers import JSONParser
from rest_framework_xml.parsers import XMLParser


Serializers = {
                'raw_data': RawDataSerializer,
                'biomass_expansion': BiomassExpansionFactorSerializer,
                'wood_density': WoodDensitySerializer,
                'allometric_equations': AllometricEquationSerializer
            }

Parsers = {
                '.json': JSONParser,
                '.xml': XMLParser,
                '.csv': CSVParser
            }

Renderers = {
				 '.json': JSONRenderer,
			     '.xml': XMLRenderer,
			     '.csv': CSVRenderer
			}

