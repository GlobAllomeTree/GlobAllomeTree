from django.conf.urls import patterns, url

urlpatterns = patterns('apps.journals.views',
    #List of journals
    url(r'^$', 'list'),

    #Detail of a journal
    url(r'^(?P<journal_id>\d+)/$', 'detail'),
)
