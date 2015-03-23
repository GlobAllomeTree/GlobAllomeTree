from django.conf.urls import patterns, url, include
from .views import BiomassExpansionFactorSearchView

urlpatterns = patterns('apps.biomass_expansion_factors.views',

    url(r'^export/$', 'export', name='biomass_expansion_factors_export'),
            
    #Single equation
    url(r'^(\d+)/$', 'record_id', name='biomass_expansion_factors_record'),
    #Single equation PDF
    url(r'^(\d+)/pdf/$', 'record_id_pdf', name='biomass_expansion_factors_record_pdf'),
    
    url(r'^$', BiomassExpansionFactorSearchView.as_view(), name='biomass_expansion_factors_search'),
)
