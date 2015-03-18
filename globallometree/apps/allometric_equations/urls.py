from django.conf.urls import patterns, url, include
from .views import AllometricEquationSearchView

urlpatterns = patterns('apps.allometric_equations.views',

    url(r'^export/$', 'export', name='equations_export'),
            
    #Single equation
    url(r'^(\d+)/$', 'record_id', name='equations_record'),
    
    #Single equation PDF
    url(r'^(\d+)/pdf/$', 'record_id_pdf', name='equations_record_pdf'),
    
    url(r'^$', AllometricEquationSearchView.as_view(), name='equation_search'),  
)