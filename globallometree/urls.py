
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

admin.autodiscover()

urlpatterns = patterns(
    '',
    ('^admin/', include(admin.site.urls)),

    ('^allometric-equations/', include('apps.allometric_equations.urls')),
    ('^accounts/', include('apps.accounts.urls')),
    ('^journals/', include('apps.journals.urls')),
)

# askbot
if getattr(settings, 'ASKBOT_MULTILINGUAL', False) == True:
    from django.conf.urls.i18n import i18n_patterns
    urlpatterns += i18n_patterns('',
        (r'%s' % settings.ASKBOT_URL, include('askbot.urls'))
    )
else:
    urlpatterns += patterns('',
        (r'%s' % settings.ASKBOT_URL, include('askbot.urls'))
    )
urlpatterns += patterns('',
    (r'^followit/', include('followit.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^robots.txt$', include('robots.urls')),
    url( # TODO: replace with django.conf.urls.static ?
        r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT.replace('\\','/')},
    ),
)

# cms
urlpatterns += patterns('',
   
    #redirects from removed pages
    url(r'^data/search', RedirectView.as_view(url=reverse_lazy('equation_search'))),
    
    #cms urls LAST!
    url(r'^', include('cms.urls')),
)
