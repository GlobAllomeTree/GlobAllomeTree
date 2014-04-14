from django.core.management.base import BaseCommand

from globallometree.apps.allometric_equations.indexes import AllometricEquationIndex
from globallometree.apps.allometric_equations.models import AllometricEquation

from pprint import pprint

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
        es = index_cls.get_es()
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

        documents=[]
        for obj in index_cls.get_indexable():
            if limit and n > limit: break;
            n = n + 1; 
            document = index_cls.extract_document(obj=obj)
            #pprint(document)
            documents.append(document)

        #Using the bulk command - put all the documents
        index_cls.bulk_index(documents, id_field=model._meta.pk.name, es=es, index=index)

        #Refresh the index
        #index_cls.get_es().indices.refresh(index=index)
        #wait for the index to be ready
        #index_cls.get_es().cluster.health(wait_for_status='yellow')