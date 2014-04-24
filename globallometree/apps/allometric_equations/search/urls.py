
from django.conf.urls import url, patterns
from .views import SearchView

urlpatterns = patterns('apps.allometric_equations.views',

    #Searchable list of equations                   
    url(r'^search/$', SearchView.as_view(), name='equation_search'),  
      
)