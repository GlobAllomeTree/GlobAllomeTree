from django.contrib.auth.decorators import login_required

from .models import AllometricEquation
from .forms import AllometricEquationSearchForm

from globallometree.apps.api.serializers import SimpleAllometricEquationSerializer
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
    configuration_js_file = 'allometric_equations/js/allometric_equation_search.js'


@login_required(login_url='/accounts/login/')
def record_id(request, id):
    return record_by_id_view(
        request, 
        id, 
        model_class=AllometricEquation, 
        record_content_template='allometric_equations/record_content.html',
        record_title='Allometric Equation %s' %  id
        )
   
@login_required(login_url='/accounts/login/')
def record_id_pdf(request, id):
    return record_by_id_pdf_view(
        request, 
        id, 
        model_class=AllometricEquation, 
        record_content_template='allometric_equations/record_content.html',
        record_title='Allometric Equation %s' %  id,
        record_url= 'http://globallometree.org/data/allometric-equations/%s/' % id)
   

@login_required(login_url='/accounts/login/')
def export(request):
    return export_view(request, 
                       doc_type="allometricequation", 
                       filename='allometric_equations',
                       serializer=SimpleAllometricEquationSerializer)
    
