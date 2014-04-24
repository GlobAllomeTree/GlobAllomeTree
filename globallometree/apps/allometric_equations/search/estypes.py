
estype_boolean = {'type': 'boolean'}

estype_integer = {'type': 'integer'}

estype_float = { 'type' : 'float' }

estype_long = { 'type' : 'long'}

estype_double = { 'type' : 'double' }

estype_string_analyzed = {'type': 'string',
						  'index': 'analyzed'}

estype_string_not_analyzed = {'type': 'string', 
                         	 'index': 'not_analyzed'}

estype_geopoint_geohashed = {'type': 'geo_point',
	                         'geohash': True,
	                         'geohash_prefix': True,
	                         'geohash_precision': 8
	                         }
