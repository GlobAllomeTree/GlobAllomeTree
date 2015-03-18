from django.conf import settings
from django.contrib import admin
from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('apps.accounts.urls')),
    url(r'^journals/', include('apps.journals.urls')),
    url(r'^community/', include('apps.community.urls')),
    url(r'^api/', include('apps.api.urls')),
    url(r'^data/allometric-equations/', include('apps.allometric_equations.urls')),
    url(r'^data/wood-densities/', include('apps.wood_densities.urls')),
    url(r'^data/taxonomy/', include('apps.taxonomy.urls')),
    url(r'^data/sharing/', include('apps.data_sharing.urls')),
    
    #redirects from removed pages
    url(r'^data/search', RedirectView.as_view(url=reverse_lazy('equation_search'))),
    url(r'^data/submit-data/', RedirectView.as_view(url=reverse_lazy('equations_upload'))),
    
    #cms urls LAST!
    url(r'^', include('cms.urls')),
)
