import sys
from django.core.management.base import BaseCommand
from elasticutils.contrib.django import get_es

def remap(index_cls):

        #Get an instance of the elasticsearch python wrapper
        es = get_es()
        index = index_cls.get_index()
        model = index_cls.get_model()
        type_name = index_cls.get_mapping_type_name()
        
        #Delete the mapping if it exists
        if es.indices.exists(index=index):
            try:
                es.indices.delete_mapping(index=index, doc_type=type_name)
            except:
                pass
            
        #Put the mapping
        #Comment this out for letting elasticsearch generate the mapping
        result = es.indices.put_mapping(
            index=index,
            doc_type=type_name,
            body={
                type_name : index_cls.get_mapping()
            }
        )

        if not result['acknowledged']:
            print "Mapping was not acknowledged by elasticsearch"
        else:
            print "Mapping acknowledged by elasticsearch"


class RemapIndexCommand(BaseCommand):
    args = '<no arguments>'

    def __init__(self, *args, **kwargs):
        self.help = 'Remaps an index: %s' % self.index_cls.__name__
        return super(RemapIndexCommand, self).__init__(*args, **kwargs)

    def handle(self,*args, **options):
        if len(args) != 0:
            exit('Command takes no arguments')

      
        remap(self.index_cls)   