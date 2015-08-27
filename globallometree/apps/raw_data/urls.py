from django.conf.urls import patterns, url, include
from .views import RawDataSearchView

urlpatterns = patterns('globallometree.apps.raw_data.views',

    url(r'^export/$', 'export', name='raw_data_export'),
            
    #Single equation
    url(r'^(\d+)/$', 'record_id', name='raw_data_record'),
    #Single equation PDF
    url(r'^(\d+)/pdf/$', 'record_id_pdf', name='raw_data_record_pdf'),
    
    url(r'^$', RawDataSearchView.as_view(), name='raw_data_search'),
)
