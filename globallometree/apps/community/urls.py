
from django.conf.urls import url, patterns
from .views import UserMapView

urlpatterns = patterns('apps.community.views',
    #Searchable list of equations                   
    url(r'^map/$', UserMapView.as_view(), name='user_map'),       
)