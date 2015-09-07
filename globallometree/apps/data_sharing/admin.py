import os
import json

from django import forms
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import models, router, transaction
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.admin.utils import unquote 
from django.utils.encoding import force_text

# (
#     NestedObjects, flatten_fieldsets, get_deleted_objects,
#     lookup_needs_distinct, model_format_dict, quote, 
# )

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


csrf_protect_m = method_decorator(csrf_protect)
TO_FIELD_VAR = '_to_field'
IS_POPUP_VAR = '_popup'

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
    list_display = ('ID_Dataset', 'Title',  'Imported', 'Marked_for_import', 'Import_error', 'Record_count', 'Records_imported', 'User', 'Data_type',  'Data_license', 'Created')
    search_fields  = ['Title', 'Description']
    raw_id_fields = ('User',)
    exclude = ('Data_as_json',)
    form = DatasetForm
    delete_confirmation_template = 'data_sharing/admin_confirm_delete.html'
        
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


    @csrf_protect_m
    @transaction.atomic
    def delete_view(self, request, object_id, extra_context=None):
        "The 'delete' admin view for this model."
        opts = self.model._meta
        app_label = opts.app_label

        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)

        obj = self.get_object(request, unquote(object_id), to_field)

        if not self.has_delete_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(
                '%(name)s object with primary key %(key)r does not exist.' %
                {'name': force_text(opts.verbose_name), 'key': escape(object_id)}
            )

        using = router.db_for_write(self.model)

        if request.POST:  # The user has already confirmed the deletion.

            obj_display = force_text(obj)
            attr = str(to_field) if to_field else opts.pk.attname
            obj_id = obj.serializable_value(attr)
            self.log_deletion(request, obj, obj_display)
            self.delete_model(request, obj)

            return self.response_delete(request, obj_display, obj_id)

        object_name = force_text(opts.verbose_name)

        
        title = "Are you sure?"

        context = dict(
            self.admin_site.each_context(request),
            title=title,
            object_name=object_name,
            object=obj,
            opts=opts,
            app_label=app_label,
            preserved_filters=self.get_preserved_filters(request),
            is_popup=(IS_POPUP_VAR in request.POST or
                      IS_POPUP_VAR in request.GET),
            to_field=to_field,
        )
        context.update(extra_context or {})

        return self.render_delete_form(request, context)


    def run_import(self, request, queryset):
        import_confirmed = request.POST.get('run', False)
        if import_confirmed:
            dataset = models.Dataset.objects.get(pk=request.POST.get('id_dataset'))
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
    list_display = ('Title', 'User', 'Public_choice','Available_to_registered_users', 'Requires_provider_approval')
    search_fields  = ['Title',]
    raw_id_fields = ('User',)


class DataSharingAgreementAdmin(admin.ModelAdmin):
    list_display = ('Dataset', 'User', 'Agreement_status',)
    raw_id_fields = ('User',)

admin.site.register(models.Dataset, DatasetAdmin)
admin.site.register(models.DataLicense, DataLicenseAdmin)
admin.site.register(models.DataSharingAgreement, DataSharingAgreementAdmin)

