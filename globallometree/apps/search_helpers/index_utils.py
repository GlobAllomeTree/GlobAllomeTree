import sys
from django.core.management.base import BaseCommand
from elasticutils.contrib.django import get_es

def rebuild(index_cls, limit):

        #Get an instance of the elasticsearch python wrapper
        es = get_es()
        index = index_cls.get_index()
        model = index_cls.get_model()
        type_name = index_cls.get_mapping_type_name()
        
        #Delete the index if it exists
        if es.indices.exists(index=index):
            try:
                es.indices.delete_mapping(index=index, doc_type=type_name)
            except:
                pass
            
        #Put the mapping
        #Comment this out for letting elasticsearch generate the mapping
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
        n = 0
        for obj in index_cls.get_indexable().iterator():
            if limit and n == limit: break;
            n = n + 1; 
            print n, 'out of', total, '\r',
            sys.stdout.flush()

            document = index_cls.extract_document(obj=obj)
            obj.update_elasticsearch_doc_hash(document)
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


class RebuildIndexCommand(BaseCommand):
    args = '<limit (optional)>'

    def __init__(self, *args, **kwargs):
        self.help = 'Rebuilds the entire index: %s' % self.index_cls.__name__
        return super(RebuildIndexCommand, self).__init__(*args, **kwargs)

    def handle(self,*args, **options):
        if len(args) == 1:
            limit = int(args[0])
        elif len(args) > 1:
            exit('Command only takes one argument <limit>')
        else:
            limit = 0
      
        rebuild(self.index_cls, limit)   