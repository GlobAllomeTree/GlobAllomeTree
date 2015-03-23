
from .serializers import (
    SimpleAllometricEquationSerializer,
    SimpleWoodDensitySerializer,
    SimpleRawDataSerializer,
    SimpleBiomassExpansionFactorSerializer
)

from .renderers import (
    SimpleJSONRenderer,
    SimpleXMLRenderer
)

from rest_framework.parsers import JSONParser
from rest_framework_xml.parsers import XMLParser


Serializers = {
                'raw_data': SimpleRawDataSerializer,
                'biomass_expansion': SimpleBiomassExpansionFactorSerializer,
                'wood_density': SimpleWoodDensitySerializer,
                'allometric_equations': SimpleAllometricEquationSerializer
            }

Parsers = {
                '.json': JSONParser,
                '.xml': XMLParser,
                '.csv': None
            }

Renderers = {
				 '.json': SimpleJSONRenderer,
			     '.xml': SimpleXMLRenderer,
			     '.csv': None
			}

