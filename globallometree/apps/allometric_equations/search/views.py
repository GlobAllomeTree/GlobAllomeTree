import json
import re

from django.conf import settings
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

#import the get_es object from contrib which reads settings.ES_URLS
from elasticutils.contrib.django import get_es

from .forms import SearchForm
from .indices import AllometricEquationIndex

class SearchView(TemplateView):
    template_name = 'allometric_equations/template.search.html'
    paginate_by = 40

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)

        self.form = SearchForm(self.request.GET)
    	
        context['form'] = self.form

        #This is for the menu
        context['is_page_data'] =  True

        if self.form.is_valid():
            context['form_is_valid'] = True
            context['current_search_summary'] = self.current_search_summary()
        else:
            context['form_is_valid'] = False
            context['current_search_summary'] = False
        
        return context

    def create_response(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        return super(SearchView, self).create_response( *args, **kwargs)

    def export_link(self):
        return self.get_query_string(export=True)

    def current_search_summary(self):
        current_search = []
        if not self.form.is_valid():
            return []
        #Send search fields to the the sqs.filter
        for field in self.form.cleaned_data:
        
            if field in ['order_by', 'page']:
                continue
            if self.form.cleaned_data.get(field, False): 
                current_search.append( {'field' : self.form.fields[field].label,
                                        'search_value' :  self.form.cleaned_data.get(field),
                                        'clear_link'   :  self.get_query_string({
                                                                                 'page' : 1,
                                                                                  field : ''
                                                                                })
                                    })
        return current_search     
 
    def get_query_string(self, using_values = {}, export=False):
    
        query_dict = {}
        query_string = ''
        first = True
       
        #Send search fields to the the sqs.filter
        if self.form.is_valid():
            for field in self.form.cleaned_data:
                if self.form.cleaned_data.get(field, False):
                    query_dict[field] = self.form.cleaned_data.get(field)
        
        for field in using_values.keys():
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
                    
        return query_string