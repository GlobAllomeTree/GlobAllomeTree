
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

estype_object =  {"type" : "object"}

estype_reference = {
                    "properties": {
                        "Author": estype_string_not_analyzed,
                        "Reference": estype_string_not_analyzed,
                        "ID_Reference": estype_long,
                        "Year": estype_long
                        }
                    }

estype_location_group = {
                            "properties": {
                                "ID_Location_group": estype_long,
                                "Group": {
                                    "properties": {
                                        "Zone_FAO": estype_string_not_analyzed,
                                        "ID_Zone_FAO": estype_string_not_analyzed,
                                        "Zone_Holdridge": estype_string_not_analyzed,
                                        "ID_Zone_Holdridge": estype_string_not_analyzed,
                                        "Ecoregion_Udvardy": estype_string_not_analyzed,
                                        "ID_Ecoregion_Udvardy": estype_long,
                                        "Ecoregion_WWF": estype_string_not_analyzed,
                                        "id_ecoregion_wwf": estype_long,
                                        "Biome_local": estype_string_not_analyzed,
                                        "Biome_local_reference": estype_string_not_analyzed,
                                        "ID_Biome_local": estype_long,
                                        "Country": estype_string_not_analyzed,
                                        "Country_3166_3" : estype_string_not_analyzed,
                                        "ID_Country": estype_long,
                                        "Division_Bailey": estype_string_not_analyzed,
                                        "ID_Division_Bailey": estype_long,
                                        "Latitude": estype_float,
                                        "Longitude": estype_float,
                                        "LatLonString": estype_string_not_analyzed,
                                        "ID_Location": estype_long,
                                        "Name": estype_string_not_analyzed,
                                        "Geohash": estype_geopoint_geohash,
                                        "Plot_name": estype_string_not_analyzed,
                                        "Plot_size_m2": estype_long,
                                    }
                                }
                            }
                        }


estype_species_group = {
                        "properties": {
                            "Group": {
                                "properties": {
                                    "Scientific_name" : estype_string_not_analyzed,
                                    "Family": estype_string_not_analyzed,
                                    "ID_Family": estype_long,
                                    "Genus": estype_string_not_analyzed,
                                    "ID_Genus": estype_long,
                                    "Species": estype_string_not_analyzed,
                                    "ID_Species": estype_long,
                                    "Subspecies": estype_string_not_analyzed,
                                    "Species_author": estype_string_not_analyzed,
                                    "Species_local_names": { 
                                        "properties": {
                                             "Local_name": estype_string_not_analyzed,
                                             "Language_iso_639": estype_string_not_analyzed,
                                             "Local_name_latin": estype_string_not_analyzed,
                                             "Local_name_ID": estype_long
                                         }
                                    },
                                }
                            },
                            "ID_Species_group": estype_long
                        }
                    }


estype_linked_model = {
            "Reference": estype_reference,
            "Dataset": estype_object,
            "Remark": estype_string_analyzed,
            "Contact": estype_string_analyzed,
            "Tree_type": estype_string_not_analyzed,
            "Species_group" : estype_species_group,
            "Location_group" : estype_location_group,
            "Contributor": estype_string_not_analyzed,
            "Operator": estype_string_not_analyzed
            }
