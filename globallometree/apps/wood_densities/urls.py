from django.conf.urls import patterns, url, include
from .views import WoodDensitySearchView

urlpatterns = patterns('globallometree.apps.wood_densities.views',

    url(r'^export/$', 'export', name='wood_densities_export'),
            
    #Single equation
    url(r'^(\d+)/$', 'record_id', name='wood_densities_record'),
    #Single equation PDF
    url(r'^(\d+)/pdf/$', 'record_id_pdf', name='wood_densities_record_pdf'),
    
    url(r'^$', WoodDensitySearchView.as_view(), name='wood_densities_search'),
)
