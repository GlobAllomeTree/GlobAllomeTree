import json
import hashlib

import elasticsearch
from django.conf import settings
from django.core.management.base import BaseCommand
from globallometree.apps.allometric_equations.models import AllometricEquation
from elasticutils.contrib.django import get_es
from globallometree.apps.allometric_equations.indices import AllometricEquationIndex
from globallometree.apps.wood_densities.indices import WoodDensityIndex
from globallometree.apps.raw_data.indices import RawDataIndex
from globallometree.apps.biomass_expansion_factors.indices import BiomassExpansionFactorIndex

class Command(BaseCommand):
    help = 'Fully synchronizes the elasticsearch indices from the postgresql database\n (optional arg: allometricequation, biomassexpansionfactor, rawdata, or wooddensity)'
    args = '<type name (optional allometricequation, biomassexpansionfactor, rawdata, or wooddensity)>'

    def handle(self,*args, **options):

        if len(args) == 1:
            limit_type_name = args[0]
        else:
            limit_type_name = None

        index_classes = (
            AllometricEquationIndex,
            WoodDensityIndex,
            RawDataIndex,
            BiomassExpansionFactorIndex
        )

        #Get an instance of the elasticsearch python wrapper
        es = get_es()

        limit_reached = False
        for index_cls in index_classes:

            if limit_reached:
                break

            updated = 0
            skipped = 0
            created = 0
            deleted = 0
            index_name = index_cls.get_index()
            model = index_cls.get_model()
            type_name = index_cls.get_mapping_type_name()

            if limit_type_name is not None and type_name != limit_type_name:
                continue

            searcher = index_cls.search()
            valid_id_list = []

            # Handle additions and updates
            for obj in index_cls.get_indexable().iterator():
                try:
                    valid_id_list.append(obj.pk)
                    current_document = index_cls.extract_document(obj=obj)
                    current_doc_hash = hashlib.md5(json.dumps(current_document)).hexdigest()
                    old_doc_hash = obj.Elasticsearch_doc_hash
                    search_results = searcher.filter(_id=obj.pk)
                    obj_updated = False

                    if len(search_results) == 0:
                        obj.update_index(add=True, document=current_document)
                        created += 1
                    elif current_doc_hash != old_doc_hash:
                        obj.update_index(add=False, document=current_document)
                        updated += 1
                    else:
                        skipped += 1
                except:
                    print "Error indexing document %s ID %s" % (type_name, obj.pk)
                    raise

                if updated + created >= 1000:
                    print "Created or updated batch of 1000 records. Please run again to continue the sync"
                    limit_reached = True
                    break
                    
            
            # Handle deletions
            # Looks at all the records in elasticsearch, if there are any that should not be there, delete them
            searcher = index_cls.search()

            result_iterator = elasticsearch.helpers.scan(client=es,
                                             query= {"query": 
                                                        {
                                                            "match_all": {}
                                                        },
                                                     "fields": ['_id',]
                                                    }, 
                                             doc_type=type_name, 
                                             index='globallometree')

            for result in result_iterator:
                # If the model is no longer present in the database, then delete it from the elasticsearch index
                if not int(result['_id']) in valid_id_list:
                    es.delete(doc_type=type_name, index='globallometree', id=result['_id'])
                    deleted += 1
                    # print 'obj %s, Deleted %s' % (result['_id'], deleted)

            # Force a lucene, elasticsearch commit of all of the previous queries
            index_client = elasticsearch.client.IndicesClient(es)
            index_client.flush(index=index_name)

            print '%s: Updated %s, Skipped %s, Created %s, Deleted %s' % (type_name, updated, skipped, created, deleted)

