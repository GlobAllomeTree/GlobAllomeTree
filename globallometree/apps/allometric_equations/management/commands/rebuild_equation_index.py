import sys
from pprint import pprint

from django.core.management.base import BaseCommand

from globallometree.apps.allometric_equations.search.indices import AllometricEquationIndex
from globallometree.apps.allometric_equations.models import AllometricEquation
from elasticutils.contrib.django import get_es


class Command(BaseCommand):
    args = '<limit (optional)>'
    help = 'Rebuilds the entire equation index'

    def handle(self,*args, **options):
        if len(args) == 1:
            limit = int(args[0])
        elif len(args) > 1:
            exit('Command only takes one argument <limit>')
        else:
            limit = 0
        n = 0

        index_cls = AllometricEquationIndex

        #Get an instance of the elasticsearch python wrapper
        es = get_es()
        index = index_cls.get_index()
        model = index_cls.get_model()
        type_name = index_cls.get_mapping_type_name()
        #Delete the index if it exists
        es.indices.delete(index, ignore=404)
        es.indices.create(index)
        #Put the mapping
        es.indices.put_mapping(
            index=index,
            doc_type=type_name,
            body={
                type_name : index_cls.get_mapping()
            }
        )


        if limit:
            total = limit
        else:
            total = index_cls.get_indexable().count()

        def send_to_index(documents):
            #Using the bulk command - put all the documents
            index_cls.bulk_index(documents, id_field=model._meta.pk.name, es=es, index=index)

        documents=[]
        for obj in index_cls.get_indexable().iterator():
            if limit and n > limit: break;
            n = n + 1; 
            print n, 'out of', total, '\r',
            sys.stdout.flush()

            document = index_cls.extract_document(obj=obj)
            #pprint(document)
            documents.append(document)

           
            #Send in batches of 50
            if len(documents) == 50:
                send_to_index(documents)
                documents = []

        #Send any remaining documents (for example if loop ended with 29 docs) 
        if len(documents):
            send_to_index(documents)

        print
        print total, ' documents indexed'
       