import os
import json

from django import forms
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext

from globallometree.apps.api.serializers import (
    AllometricEquationSerializer,
    WoodDensitySerializer,
    RawDataSerializer
)

from . import models
from .data_tools import(
    match_data_to_database, 
    summarize_data,
    Parsers,
    validate_data_file
)

class DatasetForm(forms.ModelForm):
   
   def clean_Uploaded_dataset_file(self):
        if self.cleaned_data['Uploaded_dataset_file']:
            extension = os.path.splitext(self.cleaned_data['Uploaded_dataset_file'].name.lower())[1]
            if extension not in Parsers.keys():
                valid_extensions = ", ".join(Parsers.keys())
                raise forms.ValidationError("The uploaded file must end with one of the extensions:%s" % valid_extensions)

        return self.cleaned_data['Uploaded_dataset_file']


   def clean(self):
        if 'Uploaded_dataset_file' in self.cleaned_data.keys() and \
        self.cleaned_data['Uploaded_dataset_file'] is not None and \
        not hasattr(self.cleaned_data['Uploaded_dataset_file'], '_committed'):
                data, data_errors = validate_data_file(
                    self.cleaned_data['Uploaded_dataset_file'], 
                    self.cleaned_data['Data_type']
                    )
              
                if data_errors:
                    self.request._data_errors = data_errors
                    raise forms.ValidationError("The uploaded file has errors in the data")
                else:
                    self.request._record_count = len(data)
                    self.request._data_as_json = json.dumps(data)

        return self.cleaned_data


class DatasetAdmin(admin.ModelAdmin):
    actions = ['run_import']
    list_display = ('Title',  'Imported', 'Marked_for_import', 'Import_error', 'Record_count', 'Records_imported', 'User', 'Data_type',  'Data_license', 'Created')
    search_fields  = ['Title', 'Description']
    raw_id_fields = ('User',)
    exclude = ('Data_as_json',)
    form = DatasetForm
        
    def get_form(self, request, obj=None, **kwargs):
        form = super(DatasetAdmin, self).get_form(request, obj, **kwargs)
        # Keep a reference to the form so that we can use it later
        form.request = request
        #self.form = form
        return form

    def change_view(self, request, object_id, form_url='', extra_context=None):
        change_response = super(DatasetAdmin, self).change_view(request, object_id, form_url, extra_context)
        
        # File was uploaded without valid data - so we just output the template with the errors
        if hasattr(request, '_data_errors'):
            return self.error_view(request)
        else:
            return change_response
    
    def add_view(self, request, form_url='', extra_context=None):
        add_response = super(DatasetAdmin, self).add_view(request, form_url, extra_context)
        
        # File was uploaded without valid data - so we just output the template with the errors
        if hasattr(request, '_data_errors'):
            return self.error_view(request)
        else:
            return add_response

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        # New valid json, so we store it (Since Data_as_json is an exluded field from the admin
        # the form doesn't manage to save it automatically)
        if hasattr(request, '_data_as_json'):
            obj.Data_as_json = request._data_as_json
            obj.Record_count = request._record_count
        obj.save()

    def error_view(self, request):

        return render_to_response(
                "data_sharing/upload_data.html",
                {
                 'form': self.form,
                 'data_errors': request._data_errors,
                 'extend_template': "admin/base_site.html",
                 'include_jquery' : True
                },
                context_instance=RequestContext(request)
            )

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

     
        if not dataset.Data_as_json or len(dataset.Data_as_json) == 0:
            messages.error(request, "There is not any structured data in this dataset. Please upload a structured dataset file in order to import this dataset into the database.")
            return None

        if dataset.Marked_for_import:
            messages.error(request, "The dataset '%s' has already been marked for import and will be imported by a scheduled task." % dataset.Title)
            return None

        if dataset.Imported:
            messages.error(request, "The dataset '%s' has already been imported." % dataset.Title)
            return None

        try:
            data = json.loads(dataset.Data_as_json)
        except:
            messages.error(request, "There was an error trying to parse the structured data, and the dataset could not be imported.")
            return None

        if import_confirmed:
            dataset.Marked_for_import = True
            dataset.save()
            messages.info(request, "The dataset '%s' was marked for import and the import process has started" % dataset.Title)
   
        else:

            data = match_data_to_database(data)
            data_summary = summarize_data(data)
            context = {
                'summary' : data_summary,
                'dataset' : dataset 
            }

            return render_to_response('data_sharing/admin_confirm_import.html', context,
                                            context_instance=RequestContext(request))
            
    run_import.short_description = "Mark dataset to start import"

class DataLicenseAdmin(admin.ModelAdmin):
    list_display = ('Title', 'User', 'Public_choice',)
    search_fields  = ['Title',]
    raw_id_fields = ('User',)


class DataSharingAgreementAdmin(admin.ModelAdmin):
    list_display = ('Dataset', 'User', 'Agreement_status',)
    raw_id_fields = ('User',)

admin.site.register(models.Dataset, DatasetAdmin)
admin.site.register(models.DataLicense, DataLicenseAdmin)
admin.site.register(models.DataSharingAgreement, DataSharingAgreementAdmin)

