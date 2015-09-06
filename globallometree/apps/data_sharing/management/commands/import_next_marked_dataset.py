import json
import traceback

from django.conf import settings
from django.core.management.base import BaseCommand

from globallometree.apps.data_sharing.models import Dataset

from globallometree.apps.api import Serializers


class Command(BaseCommand):
    args = '<limit>'
    help = 'Imports a set of records from the next dataset that has been marked for import'

 
    def handle(self,*args, **options):

        if len(args) == 1:
            limit = int(args[0])
        elif len(args) > 1:
            exit('Command only takes one argument <limit>')
        else:
            limit = 0

        # Is there a currently running import task? If so skip
        try: 
            locked_set = Dataset.objects.get(Locked=1)
            print "There is a locked dataset, exiting and not starting new import"
            exit(0)
        except Dataset.DoesNotExist:
            pass

        dataset = None
        
        # Is there a dataset that is currently being imported
        try:
            dataset = Dataset.objects.get(Marked_for_import=1, Records_imported__gt=0, Imported=False)
        except Dataset.DoesNotExist:
            datasets_to_import = Dataset.objects.filter(Marked_for_import=1, Imported=False)
            if len(datasets_to_import) > 0:
                dataset = datasets_to_import[0]

        if dataset is not None:   

            if dataset.Records_imported > 0:
                print "Continuing import for dataset '%s' from record %s" % (dataset,dataset.Records_imported + 1)
            else:
                print "Beginning import for dataset '%s'" % dataset
            dataset.Locked = True
            dataset.save()
            try:
                data = json.loads(dataset.Data_as_json)

                if limit:
                    data = data[dataset.Records_imported:dataset.Records_imported + limit]
                else:
                    data = data[dataset.Records_imported:]

                SerializerClass = Serializers[dataset.Data_type] 
                serializer = SerializerClass(data=data, many=True, context={'dataset': dataset})
                if serializer.is_valid(): # Must call is valid before calling save

                    serializer.save()                  
                    # records imported gets augmented inside the serializer 
                    if dataset.Records_imported == dataset.Record_count:
                        dataset.Marked_for_import = False
                        dataset.Imported = True
                    dataset.Locked = False
                    dataset.save()
                  
                else:
                    raise Exception("The dataset could not be validated and was not imported.") 
            except:
                import pdb; pdb.set_trace()
                dataset.Import_error = True
                dataset.Import_error_details = traceback.format_exc()
                dataset.Marked_for_import = False
                dataset.Locked = False
                dataset.save()
                raise 

        else:
            print "No datasets marked for import, or any marked datasets have import errors"
        


