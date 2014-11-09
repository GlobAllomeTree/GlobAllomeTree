from django.conf.urls import patterns, url, include
from .views import SpeciesListView

urlpatterns = patterns('apps.allometric_equations.views',
    url(r'^species/$', SpeciesListView.as_view(), name='species_list'),
)