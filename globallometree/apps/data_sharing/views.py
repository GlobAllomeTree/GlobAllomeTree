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

from apps.api.serializers import DatasetSerializer

from apps.accounts.mixins import RestrictedPageMixin

from .data_tools import validate_records, validate_data_file
from .models import (
    Dataset, 
    DataSharingAgreement, 
    DataLicense
    )

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
    data_errors = None
    if request.method == 'POST':
        form = DatasetUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():

            submission_method = request.POST.get('Submission_method')

            if(submission_method == 'dataset'):

                # Form is valid, now we actually try to parse and serialize the 
                # data, give errors as feedback if needed
                data, data_errors = validate_data_file(
                    form.cleaned_data['Uploaded_dataset_file'],
                    form.cleaned_data['Data_type'] 
                )

                if not(data_errors):
                    dataset = form.save()
                    # Keep the json for each dataset so it doesn't have to be
                    # parsed out every single time
                    dataset.Data_as_json = json.dumps(data)
                    dataset.Record_count = len(data)
                    dataset.save()

                    return HttpResponseRedirect(
                        reverse("data-sharing-upload-confirm", kwargs={'Dataset_ID':dataset.pk}) 
                    )

            elif(submission_method == 'document'):
                dataset = form.save()
                return HttpResponseRedirect(
                    reverse("data-sharing-upload-confirm", kwargs={'Dataset_ID':dataset.pk}) 
                )

            elif(submission_method == 'editor'):
                dataset = form.save()
                return HttpResponseRedirect(
                    reverse("dataset-edit", kwargs={'Dataset_ID':dataset.pk}) 
                )

    else:
        license_id = request.GET.get('license_id', None)
        form = DatasetUploadForm(initial={'Data_license':license_id}, user=request.user)


    return render_to_response(
        "data_sharing/upload_data.html",
        {
         'form': form,
         'data_errors': data_errors,
         'extend_template': "base.html"
         },
        context_instance=RequestContext(request)
    )

@login_required(login_url='/accounts/login/')
def dataset_detail(request, Dataset_ID):
    dataset = get_object_or_404(Dataset, Dataset_ID=Dataset_ID)
    notify = None

    try:
        data_sharing_agreement = DataSharingAgreement.objects.get(
            User=request.user,
            Dataset=dataset
            )
    except DataSharingAgreement.DoesNotExist:
        data_sharing_agreement = None

    if request.method == 'POST' and \
       dataset.Imported and \
       data_sharing_agreement is None:        
        data_sharing_agreement = DataSharingAgreement.objects.create(
            User=request.user,
            Dataset=dataset
            )
        license = dataset.Data_license

        if license.Requires_provider_approval:
            data_sharing_agreement.Agreement_status = 'pending'   
            # send email
        else:
            data_sharing_agreement.Agreement_status = 'granted'
        data_sharing_agreement.save()

    return render_to_response(
        "data_sharing/dataset_detail.html",
        {
          'data_sharing_agreement' : data_sharing_agreement,
          'dataset': dataset
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/accounts/login/')
def dataset_edit(request, Dataset_ID):
    dataset = get_object_or_404(Dataset, Dataset_ID=Dataset_ID)
    assert (dataset.User.pk == request.user.pk) \
        or request.user.is_staff
    return render_to_response(
        "data_sharing/dataset_edit.html",
        {
          'Dataset_ID': Dataset_ID,
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/accounts/login/')
def upload_confirm(request, Dataset_ID):
    dataset = get_object_or_404(Dataset, Dataset_ID=Dataset_ID)
    assert dataset.User.pk == request.user.pk
    dataset_serialized = DatasetSerializer(dataset).data
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
        context['datasets'] = self.get_queryset()
        return context

    def get_queryset(self, *args, **kwargs):
        return Dataset.objects.filter(Imported=1)


@login_required(login_url='/accounts/login/')
def my_data(request):
    datasets = Dataset.objects.filter(User=request.user)
    
    requests_made_to_user = DataSharingAgreement.objects.filter(
        Dataset__User=request.user
        )
    
    requests_made_by_user = DataSharingAgreement.objects.filter(
        User=request.user
        )

    return render_to_response(
        "data_sharing/my_data.html",
        {
          'requests_made_to_user': requests_made_to_user,
          'requests_made_by_user': requests_made_by_user,
          'datasets': datasets,
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/accounts/login/')
def agreement(request, Data_sharing_agreement_ID):
    data_sharing_agreement = get_object_or_404(DataSharingAgreement,
         Data_sharing_agreement_ID=Data_sharing_agreement_ID)

    show_response_form = False
    if request.user == data_sharing_agreement.Dataset.User \
       and data_sharing_agreement.Agreement_status == 'pending':
        if request.method == 'POST':
            response = request.POST.get('response')
            if response in ['granted', 'denied']:
                data_sharing_agreement.Agreement_status = response
                data_sharing_agreement.save()
        else:
            show_response_form = True
        

    return render_to_response(
        "data_sharing/agreement.html",
        {
          'data_sharing_agreement': data_sharing_agreement,
          'show_response_form': show_response_form
        },
        context_instance=RequestContext(request)
    )

