from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.contrib import admin
from django.conf import settings

from views import start_page, docs, links, principles, software
from fantaDB.models import fantaDB
from fantaDB.views import continents_map, fantaDB_id, geo_map, geo_map_id, database, export_db, export_db_all

admin.autodiscover()

fantaDB_list = {
    'queryset': fantaDB.objects.all(),
	'template_name': 'fantaDB_list.html',
}

urlpatterns = patterns('',
    # Example:
    # (r'^test_project/', include('test_project.foo.urls')),

    ('^admin/', include(admin.site.urls)),
	(r'^$', start_page),
	(r'^continents/$', continents_map),
	(r'^continent_002/$', list_detail.object_list, fantaDB_list),
    (r'^fantaDB_(\d+)/$', fantaDB_id),
	(r'^geo_map/$', geo_map),
	(r'^geo_map_([A-Za-z]+)/$', geo_map_id),   
	(r'^docs/$', docs),
	(r'^links/$', links),
	(r'^principles/$', principles),
	(r'^software/$', software),
    (r'^database/$', database),
    (r'^export_db/$', export_db), 
    (r'^export_db_(\d+)/$', export_db_all),  
)


#THIS IS FOR DEVELOPMENT STATIC MEDIA
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


