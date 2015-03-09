import os
import json

from django import forms
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
    Parsers,
    validate_data_file,
    import_dataset_to_db
)

class DatasetForm(forms.ModelForm):
   
   def clean_Uploaded_data_file(self):
        extension = os.path.splitext(self.cleaned_data['Uploaded_data_file'].name.lower())[1]
        if extension not in Parsers.keys():
            valid_extensions = ", ".join(Parsers.keys())
            raise forms.ValidationError("The uploaded file must end with one of the extensions:%s" % valid_extensions)

        return self.cleaned_data['Uploaded_data_file']

   def clean(self):
        print "Clean"
        if 'Uploaded_data_file' in self.cleaned_data.keys() and \
        not hasattr(self.cleaned_data['Uploaded_data_file'], '_committed'):
                data, data_errors = validate_data_file(
                    self.cleaned_data['Uploaded_data_file'], 
                    self.cleaned_data['Data_type']
                    )
                # Since the file is ok, we keep a copy as json
                self.cleaned_data['Data_as_json'] = json.dumps(data)
                if data_errors:
                    self.request._data_errors = data_errors
                    raise forms.ValidationError("The uploaded file has errors in the data")
 
        return self.cleaned_data


class DatasetAdmin(admin.ModelAdmin):
    actions = ['run_import']
    list_display = ('Title',  'Imported', 'User', 'Data_type',  'Data_license', 'Created')
    search_fields  = ['Title', 'Description']
    raw_id_fields = ('User',)
    readonly_fields = ('Imported',)
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
        else:
            return change_response

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
            try:
                import_dataset_to_db(dataset, data)
                messages.info(request, "The dataset '%s' was import correctly" % dataset.Title)
            except:
                messages.error(request, "There was an error validating the data from dataset %s" % dataset.Title)
   
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
