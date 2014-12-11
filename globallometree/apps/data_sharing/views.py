
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import ( 
    DataLicenseForm, 
    LicenseChoiceForm, 
    ExistingForm,
    DatasetUploadForm 
    )


class DataSharingOverview(TemplateView):
    template_name = "data_sharing/overview.html"
    def get_context_data(self, **kwargs):
        context = super(DataSharingOverview, self).get_context_data(**kwargs)
        context['hello'] = "Hello World"
        return context


def choose_license(request, data_agreement=None):
    if request.method == 'POST':
        submitted = request.POST.get('submitted')
        if submitted == "existing":
            choose_license_form = ExistingForm(request.POST, user=request.user)
            if choose_license_form.is_valid():
                license_id = choose_license_form.cleaned_data['license'].pk
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

    else:
        agreement_form = DataLicenseForm()

    choose_license_form = LicenseChoiceForm()
    existing_form = ExistingForm(user=request.user)

    return render_to_response(
        "data_sharing/choose_license.html",
        {
         'agreement_form': agreement_form,
         'existing_form' : existing_form,
         'choose_license_form' : choose_license_form
         },
        context_instance=RequestContext(request)
    )


def upload_data(request, dataset=None):

    if request.method == 'POST':
        form = DatasetUploadForm(request.POST, request.FILES, user=request.user)
    else:
        form = DatasetUploadForm(user=request.user)

    return render_to_response(
        "data_sharing/upload_data.html",
        {
         'form': form,
         },
        context_instance=RequestContext(request)
    )


