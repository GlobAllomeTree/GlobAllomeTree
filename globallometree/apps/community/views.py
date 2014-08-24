import json

from django.views.generic import TemplateView
from globallometree.apps.locations.models import Country

class UserMapView(TemplateView):
    template_name = 'community/template.user_map.html'

    def get_context_data(self, **kwargs):
        context = super(UserMapView, self).get_context_data(**kwargs)

    	#This is for the menu
        context['is_page_community'] =  True
        context['country_centroids'] = json.dumps(self.get_country_centroids());

        return context

    def get_country_centroids(self):
        countries = {}
        for country in Country.objects.all():
            if country.iso3166a3:
                countries[country.iso3166a3] = {
                    'latitude' : str(country.centroid_latitude),
                    'longitude' : str(country.centroid_longitude),
                    'common_name' : str(country.common_name)
                }
            else:
                print "MISSING COUNTRY 3166 3 for Country %s!" % country.common_name
        return countries

    def create_response(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        return super(SearchView, self).create_response( *args, **kwargs)
