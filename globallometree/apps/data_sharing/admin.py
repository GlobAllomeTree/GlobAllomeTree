import json

from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.api.serializers import (
    SimpleAllometricEquationSerializer,
    SimpleWoodDensitySerializer,
    SimpleRawDataSerializer
)

from . import models
from .data_tools import(
    match_data_to_database, 
    summarize_data,
    serializers
)

class DatasetAdmin(admin.ModelAdmin):
    actions = ['run_import']
    list_display = ('Title',  'Imported', 'User', 'Data_type',  'Data_license', 'Created')
    search_fields  = ['Title', 'Description']
    raw_id_fields = ('User',)
    readonly_fields = ('Imported',)
    exclude = ('Data_as_json',)

    def has_add_permission(self, request):
        return False

    def run_import(self, request, queryset):
        import_confirmed = request.POST.get('run', False)
        if import_confirmed:
            dataset = models.Dataset.objects.get(pk=request.POST.get('dataset_id'))
        else:
            #Make sure that there are some selected rows 
            n = queryset.count()
            if not n:
                messages.error(request, "Please select a file to import")
                return None
      
            #Make sure multiple objects were not selected
            if n > 1:
                messages.error(request, "Please select only ONE file to import at a time")
                return None

            #Now that we have one row, we get the data submission from the query set
            dataset = queryset[0]

        # if dataset.Imported:
        #     messages.error(request, "That dataset selected has already been imported")
        #     return None
     
        
        data = json.loads(dataset.Data_as_json)

        if import_confirmed:
            SerializerClass = serializers[dataset.Data_type] 
            serializer = SerializerClass(data=data, many=True)
            if serializer.is_valid(): # Must call id valid
                serializer.save()
            else:
                messages.error(request, "There was an error validating the data")
            dataset.Imported = True
            dataset.save()
        else:

            data = match_data_to_database(data)
            data_summary = summarize_data(data)
            context = {
                'summary' : data_summary,
                'dataset' : dataset 
            }

            return render_to_response('data_sharing/admin_confirm_import.html', context,
                                            context_instance=RequestContext(request))


class DataLicenseAdmin(admin.ModelAdmin):
    list_display = ('Title', 'User', 'Public_choice',)
    search_fields  = ['Title',]
    raw_id_fields = ('User',)

admin.site.register(models.Dataset, DatasetAdmin)
admin.site.register(models.DataLicense, DataLicenseAdmin)
