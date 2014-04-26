from django.conf.urls import patterns, url, include
from django.views.generic.list import ListView
from django.contrib import admin
from django.conf import settings
from apps.data.models import TreeEquation
from apps.data.views import continents_map, geo_map, geo_map_id

admin.autodiscover()

TreeEquation_list = {
    'queryset': TreeEquation.objects.all(),
    'template_name': 'TreeEquation_list.html',
}

urlpatterns = patterns(
    '',
    ('^admin/', include(admin.site.urls)),
    ('^data/', include('apps.data.urls')),
    ('^allometric-equations/', include('apps.allometric_equations.urls')),
    ('^accounts/', include('apps.accounts.urls')),
    ('^journals/', include('apps.journals.urls')),
    (r'^continents/$', continents_map),
    # (r'^continent_002/$', list_detail.object_list, TreeEquation_list),
    (r'^continent_002/$', ListView.as_view(), TreeEquation_list),
    (r'^geo_map/$', geo_map),
    (r'^geo_map_([A-Za-z]+)/$', geo_map_id),
    url(r'^', include('cms.urls')),
)

# askbot
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
