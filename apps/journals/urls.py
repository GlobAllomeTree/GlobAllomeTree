from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('apps.journals.views',
    #List of journals
    url(r'^$', 'journal_list'),
)