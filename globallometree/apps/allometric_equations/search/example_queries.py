from django.conf import settings

#Get the elasticutils objects configured from settings.py
from elasticutils.contrib.django import S, get_es

from pprint import pprint


from elasticsearch import Elasticsearch

es = get_es(urls=settings.ES_URLS)

#Sample facet accross all indices by Species

# s = S().facet('Species')

# for result in s.facet_counts()['Species']['terms'][0:10]:
#     print "%s: %s" % (result['term'],result['count'])





############ ouput #################
# spp.: 56
# All: 21
# sylvestris: 10
# uaucu: 9
# sp.: 9
# sericea: 9
# guianensis: 9
# glabrum: 9
# copaia: 9
# tulipifera: 8


# query works... but then fails in elasticutils parser
# s = global_search.facet_raw( places = {
#                 "geo_cluster" : {
#                     "field" : "Locations",
#                     "factor" : 0.5
#                 }
#         })

# for result in s:
#     pprint(result)
#


#Direct query to elasticsearch
#http://stackoverflow.com/questions/10715812/elasticsearch-facet-results-without-document
# 
# pprint(es.search(search_type='count', #since we just want the facet counts returned
#                  body = { 
#                 "facets" : {
#                     "places" : {
#                         "geo_cluster" : {
#                             "field" : "Locations",
#                             "factor" : 0.4
#                             }
#                         }
#                     }
#                 }))

#Returns something like:
#   {u'_shards': {u'failed': 0, u'successful': 5, u'total': 5},
# u'facets': {u'places': {u'_type': u'geo_cluster',
#                         u'clusters': [{u'bottom_right': {u'lat': 19.4412,
#                                                          u'lon': -155.0916},
#                                        u'center': {u'lat': 20.425166666666666,
#                                                    u'lon': -156.55726666666666},
#                                        u'top_left': {u'lat': 22.001,
#                                                      u'lon': -159.4302},
#                                        u'total': 6},
#          
#     ...
#
#                                       {u'bottom_right': {u'lat': -23.093885,
#                                                          u'lon': -56.036147},
#                                        u'center': {u'lat': 33.077651745364896,
#                                                    u'lon': -81.33346079166667},
#                                        u'top_left': {u'lat': 49.2333,
#                                                      u'lon': -124.6667},
#                                        u'total': 792}],
#                         u'factor': 0.4}},
# u'hits': {u'hits': [], u'max_score': 0.0, u'total': 421},
# u'timed_out': False,
# u'took': 10}
#
#
# Which is pretty close, but the total per cluster seems to be more than the overall possible total
#
#     
    
# pprint(es.search(search_type='count', #since we just want the facet counts returned
#                  body = { 
#                  "aggregations" : {
#                     "Locations-Grid" : {
#                         "geohash_grid" : {
#                             "field" : "Locations",
#                             "precision" : 2
#                             }
#                         }
#                     }
#                 }))


#############################################################################
# {u'_shards': {u'failed': 0, u'successful': 5, u'total': 5},
#  u'aggregations': {u'Locations-Grid': {u'buckets': [{u'doc_count': 102,
#                                                      u'key': u'dn'},
#                                                     {u'doc_count': 68,
#                                                      u'key': u'dj'},
#                                                     {u'doc_count': 67,
#                                                      u'key': u'dq'},
#                                                     {u'doc_count': 22,
#                                                      u'key': u'ed'},
#                                                     {u'doc_count': 15,
#                                                      u'key': u'w6'},
#                                                     {u'doc_count': 13,
#                                                      u'key': u'd8'},
#                                                     {u'doc_count': 12,
#                                                      u'key': u'u4'},
#                                                     {u'doc_count': 11,
#                                                      u'key': u'ec'},
                                            



# pprint(es.search(search_type='count', #since we just want the facet counts returned
#                  body = { 
#                  "aggregations" : {
#                     "species" : {
#                         "terms" : { 
#                             "field" : "Species" 
#                             }
#                         }
#                     }
#                 }))


#############################################################################
# {u'_shards': {u'failed': 0, u'successful': 5, u'total': 5},
#  u'aggregations': {u'species': {u'buckets': [{u'doc_count': 56,
#                                               u'key': u'spp.'},
#                                              {u'doc_count': 21,
#                                               u'key': u'All'},
#                                              {u'doc_count': 9,
#                                               u'key': u'copaia'},
#                                              {u'doc_count': 9,
#                                               u'key': u'glabrum'},
#                                              {u'doc_count': 9,


# #Combining!
# pprint(es.search(search_type='count', #since we just want the facet counts returned
#                  body = {
#                     "query" : {
#                     	"filtered" :  {
#                  			"query" : {
#                 				"match" : { "Keywords" : 'Forest'}			
#                  			},
# 		                    "filter": {
# 		                     	"and" : [
# 		                     		{
# 		                 	 			#Restrict these to limit the bounding box
# 			                     	 	"geo_bounding_box" : {
# 				                            "Locations" : {
# 				                                "top_left" : {
# 				                                    "lat" : -90,
# 				                                    "lon" : -180
# 				                                },
# 				                                "bottom_right" : {
# 				                                    "lat" : 90,
# 				                                    "lon" : 180
# 				                                }
# 				                            }
# 				                        }
# 				                    },
		                 	 	 	
# 			                 	]
# 		                    }
# 		                }
# 		             },
# 	                 "aggregations" : {
# 	                    "Locations-Grid" : {
# 	                        "geohash_grid" : {
# 	                            "field" : "Locations",
# 	                            "precision" : 2
# 	                        },
# 	                        "aggregations" : {
# 	                            "species" : {
# 	                                "terms" : { 
# 	                                    "field" : "Species" 
# 	                                 }
# 	                            },
# 	                            "avg_lat": {
# 							        "avg": {
# 							            "script": "doc['Locations'].value.lat"
# 							        }
# 							    },
# 							    "avg_lon": {
# 							        "avg": {
# 							            "script": "doc['Locations'].value.lon"
# 							        }
# 							    },
# 	                        },
# 	                    },
# 	                    "Locations-Bounds"  : {
# 	                    	"filter" : { 
# 	                    		"exists" : {
# 	                    			"field" : "Locations"
# 	                    		},
# 	                    	},
# 	                    	"aggregations": {
# 		                    	"min_lat": {
# 								        "min": {
# 								            "script": "doc['Locations'].value.lat"
# 								        }
# 							    },
# 							    "max_lat": {
# 								        "max": {
# 								            "script": "doc['Locations'].value.lat"
# 								        }
# 							    },
# 							    "min_lon": {
# 								        "min": {
# 								            "script": "doc['Locations'].value.lon"
# 								        }
# 							    },
# 							    "max_lon": {
# 								        "max": {
# 								            "script": "doc['Locations'].value.lon"
# 								        }
# 							    },
# 						   }
# 						}  
# 	                }       
#                 }))




#Combining!
pprint(es.search(body = {
                    "query" : {
                        "filtered" :  {
                            "query" : {
                                #search in keywords for matches based on simple query string
                                "simple_query_string" : {
                                    "query" : "dendrometrique",
                                    "fields": ["Keywords"],
                                    "default_operator": "and"
                                }
                            },
                            "filter": {
                                "and" : [
                                    {
                                        #Restrict these to limit the bounding box
                                        "geo_bounding_box" : {
                                            "Locations" : {
                                                "top_left" : {
                                                    "lat" : 10,
                                                    "lon" : 0
                                                },
                                                "bottom_right" : {
                                                    "lat" : 0,
                                                    "lon" : 10
                                                }
                                            }
                                        }
                                    },
                                    {
                                        "term": {
                                            "Population": "TREE"
                                        },
                                    }
                                ]
                            }, 
                        },
                    },  
                     "aggregations" : {
                        "Locations-Grid" : {
                            "geohash_grid" : {
                                "field" : "Locations",
                                "precision" : 2
                            },
                            "aggregations" : {
                                "species" : {
                                    "terms" : { 
                                        "field" : "Species" 
                                     }
                                },
                                "avg_lat": {
                                    "avg": {
                                        "script": "doc['Locations'].value.lat"
                                    }
                                },
                                "avg_lon": {
                                    "avg": {
                                        "script": "doc['Locations'].value.lon"
                                    }
                                },
                            },
                        },
                        "Locations-Bounds"  : {
                            "filter" : { 
                                "exists" : {
                                    "field" : "Locations"
                                },
                            },
                            "aggregations": {
                                "min_lat": {
                                        "min": {
                                            "script": "doc['Locations'].value.lat"
                                        }
                                },
                                "max_lat": {
                                        "max": {
                                            "script": "doc['Locations'].value.lat"
                                        }
                                },
                                "min_lon": {
                                        "min": {
                                            "script": "doc['Locations'].value.lon"
                                        }
                                },
                                "max_lon": {
                                        "max": {
                                            "script": "doc['Locations'].value.lon"
                                        }
                                },
                           }
                        }  
                    }       
                }))


#Here we get a list of geohashes by key with the species that are at that geohash
#Also the Locations-Bounds aggregation shows the max and min lons for all results
##############################################################################
# {u'_shards': {u'failed': 0, u'successful': 5, u'total': 5},
#  u'aggregations': {u'Locations-Bounds': {u'doc_count': 4786,
#                                          u'max_lat': {u'value': 69.7333},
#                                          u'max_lon': {u'value': 116.9927},
#                                          u'min_lat': {u'value': -54.60127},
#                                          u'min_lon': {u'value': -155.15}},
#                    u'Locations-Grid': {u'buckets': [{u'avg_lat': {u'value': 33.56548754646842},
#                                                      u'avg_lon': {u'value': -84.37593382899628},
#                                                      u'doc_count': 538,
#                                                      u'key': u'dn',
#                                                      u'species': {u'buckets': [{u'doc_count': 60,
#                                                                                 u'key': u'spp.'},
#                                                                                {u'doc_count': 52,
#                                                                                 u'key': u'tesota'},
#                                                                                {u'doc_count': 45,
#                                                                                 u'key': u'alba'},
#                                                                                {u'doc_count': 44,
#                                                                                 u'key': u'tulipifera'},
#                                                                                {u'doc_count': 32,
#                                                                                 u'key': u'coccinea'},
#                                                                                {u'doc_count': 29,
#                                                                                 u'key': u'rubrum'},
#                                                                                {u'doc_count': 27,
#                                                                                 u'key': u'styraciflua'},
#                                                                                {u'doc_count': 14,
#                                                                                 u'key': u'prinus'},
#                                                                                {u'doc_count': 13,
#                                                                                 u'key': u'falcata var. falcata'},
#                                                                                {u'doc_count': 13,
#                                                                                 u'key': u'sylvatica'}]}},
#                                                     {u'avg_lat': {u'value': 43.993877848101256},
#                                                      u'avg_lon': {u'value': -70.39159715189872},
#                                                      u'doc_count': 316,
#                                                      u'key': u'dr',
#                                                      u'species': {u'buckets': [{u'doc_count': 39,
#                                                                                 u'key': u'spp.'},
#                                                                                {u'doc_count': 34,
#                                                                                 u'key': u'saccharum'},
#                                                                                {u'doc_count': 22,
#                                                                                 u'key': u'grandifolia'},
#                                                                                {u'doc_count': 19,
#                                                                                 u'key': u'rubrum'},
#                                                                                {u'doc_count': 14,
#                                                                                 u'key': u'alleghaniensis'},
#                                                                                {u'doc_count': 12,
#                                                                                 u'key': u'canadensis'},
#                                                                                {u'doc_count': 12,
#                                                                                 u'key': u'papyrifera'},
#                                                                                {u'doc_count': 9,
#                                                                                 u'key': u'virginiana'},
#                                                                                {u'doc_count': 8,
#                                                                                 u'key': u'populifolia'},
#                                                                                {u'doc_count': 8,
#                                                                                 u'key': u'strobus'}]}},
#                                                     {u'avg_lat': {u'value': 47.02884925373134},
#                                                      u'avg_lon': {u'value': -118.69945970149253},
#                                                      u'doc_count': 268,
#                                                      u'key': u'c2',
#                                                      u'species': {u'buckets': [{u'doc_count': 89,
#                                                                                 u'key': u'menziesii'},
#                                                                                {u'doc_count': 24,
#                                                                                 u'key': u'mertensiana'},
#                                                                                {u'doc_count': 24,
#                                                                                 u'key': u'ponderosa'},
#                                                                                {u'doc_count': 20,
#                                                                                 u'key': u'amabilis'},
#                                                                                {u'doc_count': 20,
#                                                                                 u'key': u'plicata'},
#                                                                                {u'doc_count': 17,
#                                                                                 u'key': u'heterophylla'},
#                                                                                {u'doc_count': 12,
#                                                                                 u'key': u'occidentalis'},
#                                                                                {u'doc_count': 10,
#                                                                                 u'key': u'spp.'},
#                                                                                {u'doc_count': 9,
#                                                                                 u'key': u'contorta'},
#                                                                                {u'doc_count': 8,
#                                                                                 u'key': u'resinosa'}]}},


#Example showing both query, aggregations, and geo_bounding_box

# pprint(es.search(search_type='count', 
#                  body = { 

#                      "query" : {
#                          "constant_score" : {
#                             "filter" : {
#                                 "term" : { "Species" : "sylvestris"},
#                             }
#                          },
#                          "filtered" : {
#                             "query" : {
#                                 "match_all" : {}
#                             },
#                             "filter" : {
#                                 "geo_bounding_box" : {
#                                     "Locations" : {
#                                         "top_left" : {
#                                             "lat" : 0,
#                                             "lon" : -30
#                                         },
#                                         "bottom_right" : {
#                                             "lat" : -90,
#                                             "lon" : 50
#                                         }
#                                     }
#                                 }
#                             }
#                         }
#                      },
#                      "aggregations" : {
#                         "Locations-Grid" : {
#                             "geohash_grid" : {
#                                 "field" : "Locations",
#                                 "precision" : 2
#                             },
#                             "aggregations" : {
#                                 "species" : {
#                                         "terms" : { 
#                                             "field" : "Species" 
#                                          }
#                                     }
#                                 }
#                             },         
#                         }       
#                     }))
