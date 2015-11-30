from django.conf import settings
from django.contrib import admin
from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from globallometree.apps.proxy.views import es_proxy

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('globallometree.apps.accounts.urls')),
    url(r'^elastic/', es_proxy, name="es_proxy"),
    url(r'^journals/', include('globallometree.apps.journals.urls')),
    url(r'^community/', include('globallometree.apps.community.urls')),
    url(r'^api/', include('globallometree.apps.api.urls')),
    url(r'^data/allometric-equations/', include('globallometree.apps.allometric_equations.urls')),
    url(r'^data/wood-densities/', include('globallometree.apps.wood_densities.urls')),
    url(r'^data/raw-data/', include('globallometree.apps.raw_data.urls')),
    url(r'^data/biomass-expansion-factors/', include('globallometree.apps.biomass_expansion_factors.urls')),
    url(r'^data/taxonomy/', include('globallometree.apps.taxonomy.urls')),
    url(r'^data/sharing/', include('globallometree.apps.data_sharing.urls')),
    
    #redirects from removed pages
    url(r'^data/search', RedirectView.as_view(url=reverse_lazy('equation_search'))),
    url(r'^data/submit-data/', RedirectView.as_view(url=reverse_lazy('equations_upload'))),
    
    url(r'^google92eec5544d05de4e\.html$', lambda r: HttpResponse("google-site-verification: google92eec5544d05de4e.html", mimetype="text/plain")),
    #cms urls must be the last line in urls, don't add urls after this!
    url(r'^', include('cms.urls')),
)
