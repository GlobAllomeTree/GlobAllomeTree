from django.contrib.auth.decorators import login_required

from .models import WoodDensity
from .forms import WoodDensitySearchForm

from globallometree.apps.api.serializers import SimpleWoodDensitySerializer
from globallometree.apps.search_helpers.views import LinkedModelSearchView
from globallometree.apps.search_helpers.views import (
    record_by_id_view, 
    record_by_id_pdf_view,
    export_view
    )

class WoodDensitySearchView(LinkedModelSearchView):
    form_class = WoodDensitySearchForm
    form_template = 'wood_densities/template.search.form.html'
    search_title = "Wood Density Search"
    configuration_js_file = 'wood_densities/js/wood_densities_search.js'


@login_required(login_url='/accounts/login/')
def record_id(request, id):
    return record_by_id_view(
        request, 
        id, 
        model_class=WoodDensity, 
        record_content_template='wood_densities/record_content.html',
        record_title='Wood Density %s' %  id
        )


@login_required(login_url='/accounts/login/')
def record_id_pdf(request, id):
    return record_by_id_pdf_view(
        request, 
        id, 
        model_class=WoodDensity, 
        record_content_template='wood_densities/record_content.html',
        record_title='Wood Density %s' %  id,
        record_url= 'http://globallometree.org/data/wood-densities/%s/' % id)
   

@login_required(login_url='/accounts/login/')
def export(request):
    return export_view(request, 
                       doc_type="wooddensity", 
                       filename='wood_densities',
                       serializer=SimpleWoodDensitySerializer)
    
