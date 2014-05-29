
from django.contrib import admin
from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy


admin.autodiscover()


urlpatterns = patterns(
    '',
    ('^admin/', include(admin.site.urls)),

    ('^allometric-equations/', include('apps.allometric_equations.urls')),
    ('^accounts/', include('apps.accounts.urls')),
    ('^journals/', include('apps.journals.urls')),
    
    #redirects from removed pages
    url(r'^data/search', RedirectView.as_view(url=reverse_lazy('equation_search'))),
    url(r'^data/submit-data/', RedirectView.as_view(url=reverse_lazy('equations_upload'))),
    #cms urls LAST!
    url(r'^', include('cms.urls')),

)