from django.conf.urls import patterns, url
from .views import SubmissionView, SubmissionCompleteView
from .search.views import SearchView

urlpatterns = patterns('apps.allometric_equations.views',

    url(r'^autocomplete/(.+)/$', 'autocomplete'),

    url(r'^export/$', 'export'),
            
    url(r'^submit$', SubmissionView.as_view()),
    url(r'^submit/complete/$', SubmissionCompleteView.as_view()),
    #Searchable list of equations                   
    url(r'^search/$', SearchView.as_view(), name='equation_search'),  

    #Single equation
    (r'^(\d+)/$', 'allometric_equation_id'),
    #Single equation PDF
    (r'^(\d+)/pdf$', 'allometric_equation_id_pdf')
      
)