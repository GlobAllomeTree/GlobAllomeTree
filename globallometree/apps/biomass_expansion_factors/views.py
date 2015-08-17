from django.contrib.auth.decorators import login_required

from .models import BiomassExpansionFactor
from .forms import BiomassExpansionFactorSearchForm

from apps.api.serializers import BiomassExpansionFactorSerializer
from apps.search_helpers.views import LinkedModelSearchView
from apps.search_helpers.views import (
    record_by_id_view, 
    record_by_id_pdf_view,
    export_view
    )


class BiomassExpansionFactorSearchView(LinkedModelSearchView):
    form_class = BiomassExpansionFactorSearchForm
    form_template = 'biomass_expansion_factors/template.search.form.html'
    search_title = "Biomass Expansion Factor Search"
    configuration_js_file = 'biomass_expansion_factors/js/biomass_expansion_factors_search.js'


@login_required(login_url='/accounts/login/')
def record_id(request, id):
    return record_by_id_view(
        request, 
        id, 
        api_path="biomass-expansion-factors",  
        model_class=BiomassExpansionFactor,
        record_content_template='biomass_expansion_factors/record_content.html',
        record_title='Biomass Expansion Factor %s' %  id
        )


@login_required(login_url='/accounts/login/')
def record_id_pdf(request, id):
    return record_by_id_pdf_view(
        request, 
        id, 
        model_class=BiomassExpansionFactor,
        record_content_template='biomass_expansion_factors/record_content.html',
        record_title='Biomass Expansion Factor %s' %  id,
        record_url= 'http://globallometree.org/data/biomass-expansion-factor/%s/' % id)
   

@login_required(login_url='/accounts/login/')
def export(request):
    return export_view(request, 
                       doc_type="biomassexpansionfactor",
                       filename='biomass_expansion_factors',
                       serializer=BiomassExpansionFactorSerializer)
    
