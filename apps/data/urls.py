from django.conf.urls.defaults import patterns, url
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory
from .forms import EquationSearchForm
from .views import EquationSearchView
urlpatterns = patterns('',

    # password reset
    url(r'^species/$', 
         'apps.data.views.species'),
   
)

sqs = SearchQuerySet()
urlpatterns += patterns('haystack.views',
    url(r'^search/$', search_view_factory(
        view_class=EquationSearchView,
        template='data/template.search.html',
        form_class=EquationSearchForm,
        searchqueryset=sqs,
        results_per_page=40,
    ), name='haystack_search'),                    
)