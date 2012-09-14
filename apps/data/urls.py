from django.conf.urls.defaults import patterns, url
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory
from .forms import EquationSearchForm
from .views import EquationSearchView



sqs = SearchQuerySet()

urlpatterns = patterns('apps.data.views',


    #List of genus / species
    url(r'^species/$', 'species'),

    #Field Autocomplete
    url(r'^autocomplete/(.+)/$', 'autocomplete'),

    #Sample code for json based search
    #url(r'^json/$', 'json_search'),

    url(r'^export/$', 'export'),
            
    #Searchable list of equations                   
    url(r'^search/$', search_view_factory(
        view_class=EquationSearchView,
        template='data/template.search.html',
        form_class=EquationSearchForm,
        searchqueryset=sqs,
        results_per_page=40,
    ), name='haystack_search'), 
                       

    #Single equation
    (r'^equation/(\d+)/$', 'tree_equation_id'),

   
)


