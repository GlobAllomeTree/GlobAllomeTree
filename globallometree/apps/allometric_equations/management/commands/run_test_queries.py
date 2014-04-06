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
         #                                       {u'bottom_right': {u'lat': -25.4699,
         #                                                          u'lon': 30.9806},
         #                                        u'center': {u'lat': -25.4699,
         #                                                    u'lon': 30.9806},
         #                                        u'top_left': {u'lat': -25.4699,
         #                                                      u'lon': 30.9806},
         #                                        u'total': 4},
         #                                       {u'bottom_right': {u'lat': 11.427778,
         #                                                          u'lon': 108.648889},
         #                                        u'center': {u'lat': 13.009632638297871,
         #                                                    u'lon': 105.82769434042552},
         #                                        u'top_left': {u'lat': 13.8278,
         #                                                      u'lon': 103.3587},
         #                                        u'total': 47},
         #                                       {u'bottom_right': {u'lat': -15.9,
         #                                                          u'lon': 34.75},
         #                                        u'center': {u'lat': 32.76972698529411,
         #                                                    u'lon': 6.221211029411764},
         #                                        u'top_left': {u'lat': 62.909,
         #                                                      u'lon': -16.0482},
         #                                        u'total': 136},
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
                

                 