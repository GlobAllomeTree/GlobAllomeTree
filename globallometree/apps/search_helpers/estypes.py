
estype_boolean = {'type': 'boolean'}

estype_integer = {'type': 'integer'}

estype_float = { 'type' : 'float' }

estype_long = { 'type' : 'long'}

estype_double = { 'type' : 'double' }

estype_date = { 'type' : 'date',
                'format' : "YYYY-MM-dd" }

estype_string_analyzed = {'type': 'string',
                          'index': 'analyzed'}

estype_string_not_analyzed = {'type': 'string', 
                             'index': 'not_analyzed'}

estype_geopoint_geohash = {'type': 'geo_point',
                             'geohash_prefix': True,
                             'geohash_precision': 9
                             }

estype_reference = {
                    "properties": {
                        "Author": estype_string_not_analyzed,
                        "Label": estype_string_not_analyzed,
                        "Reference": estype_string_not_analyzed,
                        "Reference_ID": estype_long,
                        "Year": estype_long
                        }
                    }

estype_location_group = {
                            "properties": {
                                "Location_group_ID": estype_long,
                                "Locations": {
                                    "properties": {
                                        "Biome_FAO": estype_string_not_analyzed,
                                        "Biome_FAO_ID": estype_string_not_analyzed,
                                        "Biome_HOLDRIDGE": estype_string_not_analyzed,
                                        "Biome_HOLDRIDGE_ID": estype_string_not_analyzed,
                                        "Biome_UDVARDY": estype_string_not_analyzed,
                                        "Biome_UDVARDY_ID": estype_long,
                                        "Biome_WWF": estype_string_not_analyzed,
                                        "Biome_WWF_ID": estype_long,
                                        "Country": estype_string_not_analyzed,
                                        "Country_3166_3" : estype_string_not_analyzed,
                                        "Country_ID": estype_long,
                                        "Division_BAILEY": estype_string_not_analyzed,
                                        "Division_BAILEY_ID": estype_long,
                                        "Latitude": estype_float,
                                        "Longitude": estype_float,
                                        "LatLonString": estype_string_not_analyzed,
                                        "Location_ID": estype_long,
                                        "Name": estype_string_not_analyzed,
                                        "Geohash": estype_geopoint_geohash
                                    }
                                }
                            }
                        }


estype_species_group = {
                        "properties": {
                            "Species": {
                                "properties": {
                                    "Scientific_name" : estype_string_not_analyzed,
                                    "Family": estype_string_not_analyzed,
                                    "Family_ID": estype_long,
                                    "Genus": estype_string_not_analyzed,
                                    "Genus_ID": estype_long,
                                    "Species": estype_string_not_analyzed,
                                    "Species_ID": estype_long
                                }
                            },
                            "Species_group_ID": estype_long
                        }
                    }
