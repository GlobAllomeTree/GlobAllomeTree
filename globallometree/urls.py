
from django.contrib import admin
from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy


admin.autodiscover()

#from django.views.generic.list import ListView
# from apps.data.models import TreeEquation
# from apps.data.views import continents_map, geo_map, geo_map_id
# TreeEquation_list = {
#     'queryset': TreeEquation.objects.all(),
#     'template_name': 'TreeEquation_list.html',
# }
#    (r'^continents/$', continents_map),
#    (r'^continent_002/$', ListView.as_view(), TreeEquation_list),
#    (r'^geo_map/$', geo_map),
#    (r'^geo_map_([A-Za-z]+)/$', geo_map_id),
#    ('^data/', include('apps.data.urls')),

urlpatterns = patterns(
    '',
    ('^admin/', include(admin.site.urls)),

    ('^allometric-equations/', include('apps.allometric_equations.urls')),
    ('^accounts/', include('apps.accounts.urls')),
    ('^journals/', include('apps.journals.urls')),
    
    #redirects from removed pages
    url(r'^data/search', RedirectView.as_view(url=reverse_lazy('equation_search'))),
    
    #cms urls LAST!
    url(r'^', include('cms.urls')),


)