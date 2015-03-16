from django.conf.urls import patterns, url, include
from .views import AllometricEquationSearchView

urlpatterns = patterns('apps.allometric_equations.views',

    url(r'^export/$', 'export', name='equations_export'),
            
    #Single equation
    (r'^(\d+)/$', 'allometric_equation_id'),
    #Single equation PDF
    (r'^(\d+)/pdf$', 'allometric_equation_id_pdf'),
    
    url(r'^$', AllometricEquationSearchView.as_view(), name='equation_search'),  
)