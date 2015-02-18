import os
import json

from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q

from rest_framework.parsers import JSONParser, XMLParser

from apps.api.serializers import SimpleDatasetSerializer # needed?
from apps.api.serializers import (
    SimpleAllometricEquationSerializer,
    SimpleWoodDensitySerializer,
    SimpleRawDataSerializer
)

from apps.accounts.mixins import RestrictedPageMixin

from .models import Dataset
from .forms import ( 
    DataLicenseForm, 
    LicenseChoiceForm, 
    ExistingForm,
    CreativeForm,
    DatasetUploadForm 
    )


class DataSharingOverview(RestrictedPageMixin, TemplateView):
    template_name = "data_sharing/overview.html"


    def get_context_data(self, **kwargs):
        context = super(DataSharingOverview, self).get_context_data(**kwargs)
        context['hello'] = "Hello World"
        return context


@login_required(login_url='/accounts/login/')
def choose_license(request, data_agreement=None):

    choose_license_form = LicenseChoiceForm()
    creative_form = CreativeForm()
    agreement_form = DataLicenseForm(user=request.user)
    existing_form = ExistingForm(user=request.user)
    submitted = None

    if request.method == 'POST':
        submitted = request.POST.get('submitted')
        choose_license_form = LicenseChoiceForm(data={'choose_license' : submitted})
        license_id = None
        if submitted == "existing":
            existing_form = ExistingForm(request.POST, user=request.user)
            if existing_form.is_valid():
                license_id = existing_form.cleaned_data['license'].pk
        elif submitted == "creative":
            creative_form = CreativeForm(request.POST)
            if creative_form.is_valid():
                license_id = creative_form.cleaned_data['license'].pk
        elif submitted == "new" :
            agreement_form = DataLicenseForm(request.POST, user=request.user)
            if agreement_form.is_valid():
                license = agreement_form.save()
                license_id = license.pk 
        elif submitted == "open":
            pass

        if license_id:
            url = "%s?license_id=%s" % (reverse('data-sharing-upload'), license_id) 
            return HttpResponseRedirect(url)
      

    return render_to_response(
        "data_sharing/choose_license.html",
        {
         'agreement_form': agreement_form,
         'existing_form' : existing_form,
         'creative_form' : creative_form,
         'choose_license_form' : choose_license_form,
         'submitted' : submitted
         },
        context_instance=RequestContext(request)
    )

@login_required(login_url='/accounts/login/')
def upload_data(request):

    data_errors = []

    if request.method == 'POST':
        form = DatasetUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            # Form is valid, now we actually try to parse and serialize the 
            # real data 
            # sumitted_file is the in memory copy of the file
            submitted_file = form.cleaned_data['Uploaded_data_file']
            
            parsers = {
                '.json': JSONParser,
                '.xml': XMLParser,
                '.csv': None
            }

            serializers = {
                'raw_data': SimpleRawDataSerializer,
                'biomass_expansion': None,
                'wood_density': SimpleWoodDensitySerializer,
                'allometric_equations': SimpleAllometricEquationSerializer
            }

            extension = os.path.splitext(submitted_file._name.lower())[1]
            ParserClass = parsers[extension]
            SerializerClass = serializers[form.cleaned_data['Data_type']]

            parser = ParserClass()
            data = parser.parse(submitted_file)

            def get_sub_errors(sub_error_list):
                for sub_error_dict in sub_error_list:
                    sub_errors = []
                    for sub_key in sub_error_dict:
                        val = {
                            'field' : sub_key,
                            'error' : ', '.join(sub_error_dict[sub_key])
                            }
                        if val not in sub_errors:
                            sub_errors.append(val)
                return sub_errors

            for en in enumerate(data):
                record_number = en[0] + 1
                record_serializer = SerializerClass(data=en[1])
                record_errors = []
                if not record_serializer.is_valid():
                    
                    error_dict = dict(record_serializer.errors)

                    for key in error_dict.keys():

                        if key == 'Location_group':
                            record_errors.append({
                                'field' : key,
                                'sub_errors' : get_sub_errors(error_dict['Location_group']['Locations'])
                            })

                        elif key == 'Species_group':
                            record_errors.append({
                                'field' : key,
                                'sub_errors' : get_sub_errors(error_dict['Species_group']['Species'])
                            })
                        else:    
                            record_errors.append({
                                'field' : key,
                                'error' : ', '.join(error_dict[key])
                                })

                    data_errors.append({
                        'record_number': record_number,
                        'errors' : record_errors,
                        'source' : json.dumps(data, indent=4)
                        })

            if not(data_errors):
                dataset = form.save()
                return HttpResponseRedirect(
                    reverse("data-sharing-upload-confirm", kwargs={'Dataset_ID':dataset.pk}) 
                )
    else:
        license_id = request.GET.get('license_id', None)
        form = DatasetUploadForm(initial={'Data_license':license_id}, user=request.user)


    return render_to_response(
        "data_sharing/upload_data.html",
        {
         'form': form,
         'data_errors': data_errors
         },
        context_instance=RequestContext(request)
    )

@login_required(login_url='/accounts/login/')
def dataset_detail(request, Dataset_ID):
    dataset = get_object_or_404(Dataset, Dataset_ID=Dataset_ID)
    assert (dataset.User.pk == request.user.pk) \
        or dataset.Imported \
        or request.user.is_staff
    dataset_serialized = SimpleDatasetSerializer(dataset).data
    return render_to_response(
        "data_sharing/dataset_detail.html",
        {
          'dataset': dataset_serialized,
        },
        context_instance=RequestContext(request)
    )

@login_required(login_url='/accounts/login/')
def upload_confirm(request, Dataset_ID):
    dataset = get_object_or_404(Dataset, Dataset_ID=Dataset_ID)
    assert dataset.User.pk == request.user.pk
    dataset_serialized = SimpleDatasetSerializer(dataset).data
    return render_to_response(
        "data_sharing/upload_confirm.html",
        {
          'dataset': dataset_serialized,
          'dataset_url': reverse("data-sharing-dataset-detail", 
                            kwargs={'Dataset_ID':dataset.pk}) 

        },
        context_instance=RequestContext(request)
    )


class DatasetListView(RestrictedPageMixin, ListView):
    model = Dataset
    template = 'data_sharing/dataset_list.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(DatasetListView, self).get_context_data(**kwargs)
        context['datasets'] = []
        for dataset in self.object_list:
            obj_serialized = SimpleDatasetSerializer(dataset).data
            context['datasets'].append(obj_serialized)
        return context

    def get_queryset(self, *args, **kwargs):
       return Dataset.objects.filter(Imported=1)





