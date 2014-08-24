import json
import re
from decimal import Decimal

from django.conf import settings
from django.views.generic import TemplateView

from globallometree.apps.locations.models import Country

from .forms import SearchForm

class SearchView(TemplateView):
    template_name = 'allometric_equations/template.search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)

        self.form = SearchForm(self.request.GET)
    	
        context['form'] = self.form

        #This is for the menu
        context['is_page_data'] =  True

        if self.form.is_valid():
            context['form_is_valid'] = True
            context['current_search_summary'] = self.current_search_summary()
            context['search_dict'] = json.dumps(self.get_search_dict());
            context['country_centroids'] = json.dumps(self.get_country_centroids());
        else:
            context['form_is_valid'] = False
            
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

    def get_search_dict(self, safe=False):
        search_dict = {}
        if self.form.is_valid():
            for field in self.form.cleaned_data:
                if self.form.cleaned_data.get(field, None) not in [None, '']:
                    value = self.form.cleaned_data.get(field)
                    #Handle decimal types which don't have unicode casting
                    #and instead use string
                    if hasattr(value, '__unicode__'):
                        value = unicode(value)
                    elif type(value) == Decimal:
                        value = str(value)
                    search_dict[field] = value;
        return search_dict

    def current_search_summary(self):
        current_search = []
        if not self.form.is_valid():
            return []
        #Send search fields to the the sqs.filter
        for field in self.form.cleaned_data:
        
            if field in ['order_by','Point_Latitude', 'Point_Longitude']:
                continue

            if self.form.cleaned_data.get(field, None) not in [None, '']:
                if field == 'Point_Distance':
                    latitude = self.form.cleaned_data.get('Point_Latitude')
                    longitude = self.form.cleaned_data.get('Point_Longitude')
                    distance = self.form.cleaned_data.get('Point_Distance')
                    summary = "%s km from %s and %s " % (distance, latitude, longitude)

                    current_search.append( {'field' : 'Distance From Point',
                                            'search_value' :  summary,
                                            'clear_link'   :  self.get_query_string({ 'Point_Latitude' : None,
                                                                                      'Point_Longitude' : None,
                                                                                      'Point_Distance' : None,
                                                                                     })
                                        })
                else: 
                    current_search.append( {'field' : self.form.fields[field].label,
                                            'search_value' :  self.form.cleaned_data.get(field),
                                            'clear_link'   :  self.get_query_string({ field : None})
                                        })
        return current_search     
 
    def export_link(self):
        return self.get_query_string(export=True)

    def get_query_string(self, using_values = {}, export=False):
    
        query_dict = self.get_search_dict()
        query_string = ''
        first = True
       
        for field in using_values.keys():
            if using_values[field] is None:
                del query_dict[field]
            else:
                query_dict[field] = using_values[field]
            
        if export and 'page' in query_dict.keys():
            del query_dict['page']
        
        for field in query_dict.keys():
            if first:
                c = '?'
                first = False
            else:
                c = '&'
                
            query_string += '%s%s=%s' % (c, field, query_dict[field])
          
        if not len(query_string):
            query_string = '?'

        return query_string