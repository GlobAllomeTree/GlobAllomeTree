from django.conf.urls import patterns, url
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory
from .forms import SearchForm
from .views import SearchView, SubmissionView, SubmissionCompleteView


urlpatterns = patterns('apps.allometric_equations.views',

    url(r'^autocomplete/(.+)/$', 'autocomplete'),

    url(r'^export/$', 'export'),
            
    url(r'^submit$', SubmissionView.as_view()),
    url(r'^submit/complete/$', SubmissionCompleteView.as_view()),

    #Searchable list of equations                   
    url(r'^$', search_view_factory(
        view_class=SearchView,
        template='allometric_equations/template.search.html',
        form_class=SearchForm,
        searchqueryset=SearchQuerySet(),
        results_per_page=40,
    ), name='haystack_search'),        
    #Single equation
    (r'^(\d+)/$', 'allometric_equation_id'),
    #Single equation PDF
    (r'^(\d+)/pdf$', 'allometric_equation_id_pdf')
)