
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q

from apps.api.serializers import SimpleDatasetSerializer

from .models import Dataset
from .forms import ( 
    DataLicenseForm, 
    LicenseChoiceForm, 
    ExistingForm,
    CreativeForm,
    DatasetUploadForm 
    )


class DataSharingOverview(TemplateView):
    template_name = "data_sharing/overview.html"
    def get_context_data(self, **kwargs):
        context = super(DataSharingOverview, self).get_context_data(**kwargs)
        context['hello'] = "Hello World"
        return context


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


def upload_data(request):

    if request.method == 'POST':
        form = DatasetUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
    else:
        license_id = request.GET.get('license_id', None)
        form = DatasetUploadForm(initial={'Data_license':license_id}, user=request.user)

    return render_to_response(
        "data_sharing/upload_data.html",
        {
         'form': form,
         },
        context_instance=RequestContext(request)
    )


def dataset_detail(request, Dataset_ID):
    dataset = get_object_or_404(Dataset, Dataset_ID=Dataset_ID)
    dataset_serialized = SimpleDatasetSerializer(dataset).data
    return render_to_response(
        "data_sharing/dataset_detail.html",
        {
          'dataset': dataset_serialized,
        },
        context_instance=RequestContext(request)
    )


class DatasetListView(ListView):
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





