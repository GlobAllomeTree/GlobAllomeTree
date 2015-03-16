from django.contrib.auth.decorators import login_required

from .models import AllometricEquation
from .forms import AllometricEquationSearchForm

from globallometree.apps.search_helpers.views import LinkedModelSearchView
from globallometree.apps.search_helpers.views import (
    record_by_id_view, 
    record_by_id_pdf_view,
    export_view
    )

class AllometricEquationSearchView(LinkedModelSearchView):
    form_class = AllometricEquationSearchForm
    form_template = 'allometric_equations/template.search.form.html'
    search_title = "Allometric Equation Search"
    configuration_js_file = 'allometric_equations/js/allometricequation_search.js'


@login_required(login_url='/accounts/login/')
def record_id(request, id):
    return record_by_id_view(
        request, id, model_class=AllometricEquation, template_path='allometric_equations')
   

@login_required(login_url='/accounts/login/')
def record_id_pdf(request, id):
    return record_by_id_pdf_view(
        request, id, model_class=AllometricEquation, template_path='allometric_equations')
   

@login_required(login_url='/accounts/login/')
def export(request):
    return export_view(request, filename='allometric_equations')
    
