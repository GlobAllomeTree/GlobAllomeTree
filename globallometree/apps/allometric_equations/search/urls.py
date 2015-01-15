
from django.conf.urls import url, patterns


urlpatterns = patterns('apps.allometric_equations.views',

    #Searchable list of equations                   
    url(r'^search/$', SearchView.as_view(), name='equation_search'),  
      
)