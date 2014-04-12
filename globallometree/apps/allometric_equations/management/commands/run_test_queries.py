from django.core.management.base import BaseCommand

from globallometree.apps.allometric_equations.es_index import AllometricEquationIndex

from django.conf import settings

#Try out the S search object from elasticutils
from elasticutils import S

#Get the raw elasticsearch connection
from elasticutils import get_es

from pprint import pprint

class Command(BaseCommand):

    def handle(self,*args, **options):

        from elasticsearch import Elasticsearch

        #Sample facet accross all indexes by Species
        global_search = S().es(urls=settings.ELASTICSEARCH_URLS) 
        s = global_search.facet('Species')
        for result in s.facet_counts()['Species']['terms'][0:10]:
            print "%s: %s" % (result['term'],result['count'])


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
        es = get_es(urls=settings.ELASTICSEARCH_URLS)
        pprint(es.search(search_type='count', #since we just want the facet counts returned
                         body = { 
                        "facets" : {
                            "places" : {
                                "geo_cluster" : {
                                    "field" : "Locations",
                                    "factor" : 0.4
                                    }
                                }
                            }
                        }))

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
            
        pprint(es.search(search_type='count', #since we just want the facet counts returned
                         body = { 
                         "aggregations" : {
                            "Locations-Grid" : {
                                "geohash_grid" : {
                                    "field" : "Locations",
                                    "precision" : 2
                                    }
                                }
                            }
                        }))


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
                                                    
        


        pprint(es.search(search_type='count', #since we just want the facet counts returned
                         body = { 
                         "aggregations" : {
                            "species" : {
                                "terms" : { 
                                    "field" : "Species" 
                                    }
                                }
                            }
                        }))


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


        #Combining!
        pprint(es.search(search_type='count', #since we just want the facet counts returned
                         body = { 
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
                                        }
                                    }
                                },         
                            }       
                        }))

        #Here we get a list of geohashes by key with the species that are at that geohash
        ##############################################################################
        # {u'doc_count': 2,
        # u'key': u'6q',
        # u'species': {u'buckets': [{u'doc_count': 2,
        #                            u'key': u'unknown'},
        #                           {u'doc_count': 1,
        #                            u'key': u'flexuosa'},
        #                           {u'doc_count': 1,
        #                            u'key': u'laevis'},
        #                           {u'doc_count': 1,
        #                            u'key': u'officinalis'},
        #                           {u'doc_count': 1,
        #                            u'key': u'pavonis'}]}},
        #  {u'doc_count': 1,
        #  u'key': u'ud',
        #  u'species': {u'buckets': [{u'doc_count': 1,
        #                             u'key': u'sylvestris'}]}},
        # {u'doc_count': 1,
        #  u'key': u'u7',
        #  u'species': {u'buckets': [{u'doc_count': 1,
        #                             u'key': u'sylvestris'}]}},


        #Example showing both query, aggregations, and geo_bounding_box
        
        pprint(es.search(search_type='count', 
                         body = { 

                             "query" : {
                                 "constant_score" : {
                                    "filter" : {
                                        "term" : { "Species" : "sylvestris"},
                                    }
                                 },
                                 "filtered" : {
                                    "query" : {
                                        "match_all" : {}
                                    },
                                    "filter" : {
                                        "geo_bounding_box" : {
                                            "Locations" : {
                                                "top_left" : {
                                                    "lat" : 180,
                                                    "lon" : 0
                                                },
                                                "bottom_right" : {
                                                    "lat" : 0,
                                                    "lon" : 180
                                                }
                                            }
                                        }
                                    }
                                }
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
                                            }
                                        }
                                    },         
                                }       
                            }))
       

                 