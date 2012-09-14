from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.contrib import admin
from django.conf import settings

from views import start_page, docs, links, principles, software, backbone
from apps.data.models import TreeEquation
from apps.data.views import continents_map, geo_map, geo_map_id, database

admin.autodiscover()

TreeEquation_list = {
    'queryset': TreeEquation.objects.all(),
	'template_name': 'TreeEquation_list.html',
}

urlpatterns = patterns('',
    # Example:
    # (r'^test_project/', include('test_project.foo.urls')),

    ('^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    ('^data/', include('apps.data.urls')),
    ('^accounts/', include('apps.accounts.urls')),
	(r'^$', start_page),
	(r'^continents/$', continents_map),
	(r'^continent_002/$', list_detail.object_list, TreeEquation_list),
	(r'^geo_map/$', geo_map),
	(r'^geo_map_([A-Za-z]+)/$', geo_map_id),   
	(r'^docs/$', docs),
	(r'^links/$', links),
	(r'^principles/$', principles),
	(r'^software/$', software),
    (r'^backbone/$', backbone),
    (r'^database/$', database)
)


#THIS IS FOR DEVELOPMENT  MEDIA
# -----------------------------------
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {
                'document_root': settings.MEDIA_ROOT,
                'show_indexes': True
            }
        ),
    )
# -----------------------------------


