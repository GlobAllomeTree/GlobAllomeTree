from django.contrib.auth.decorators import login_required

from .models import RawData
from .forms import RawDataSearchForm

from apps.api.serializers import RawDataSerializer
from apps.search_helpers.views import LinkedModelSearchView
from apps.search_helpers.views import (
    record_by_id_view, 
    record_by_id_pdf_view,
    export_view
    )

class RawDataSearchView(LinkedModelSearchView):
    form_class = RawDataSearchForm
    form_template = 'raw_data/template.search.form.html'
    search_title = "Raw Data Search"
    configuration_js_file = 'raw_data/js/raw_data_search.js'


@login_required(login_url='/accounts/login/')
def record_id(request, id):
    return record_by_id_view(
        request, 
        id, 
        api_path="raw_data",
        model_class=RawData,
        record_content_template='raw_data/record_content.html',
        record_title='Raw Data %s' %  id
        )


@login_required(login_url='/accounts/login/')
def record_id_pdf(request, id):
    return record_by_id_pdf_view(
        request, 
        id, 
        api_path="raw-data",  
        model_class=RawData,
        record_content_template='raw_data/record_content.html',
        record_title='Raw Data %s' %  id,
        record_url= 'http://globallometree.org/data/raw-data/%s/' % id)
   

@login_required(login_url='/accounts/login/')
def export(request):
    return export_view(request, 
                       doc_type="rawdata",
                       filename='raw_data',
                       serializer=RawDataSerializer)
    
