from django.conf import settings
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

#import the S object from contrib which reads settings.ES_URLS
from elasticutils.contrib.django import S

from .forms import SearchForm
from .indices import AllometricEquationIndex

class SearchView(TemplateView):
    template_name = 'allometric_equations/template.search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)

        self.form = SearchForm(self.request.GET)
    	results = self.search()
    	paginator = Paginator(results, 40)
        page = paginator.page(self.get_current_page())
         
        context['form'] = self.form
        context['is_page_data'] =  True

        if self.form.is_valid():
            context['page'] = page
            context['current_search_summary'] = self.current_search_summary()
        
        context['query_entered'] = self.query_entered()

        return context

    def query_entered(self):
        return bool(len(self.request.GET.keys()) and 'q' in self.request.GET.keys())

    def create_response(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        return super(SearchView, self).create_response( *args, **kwargs)

    def search(self):
       
       	s = S(AllometricEquationIndex)

        if not self.form.is_valid():
            #if form is not valid, return empty list
            return []

        if not self.query_entered():
            #If there is no query yet return all results
            return s

        # if form.cleaned_data.get('q'):
        #     s = s.??

        # ORDERING 
        # Check to see if a order_by field was chosen.
        if self.form.cleaned_data.get('order_by'):
            s = s.order_by(self.form.cleaned_data.get('order_by'))
        
        #Send search fields to the the sqs.filter
        for field in self.form.cleaned_data:
        
            if field in ['q', 'order_by', 'page']:
                continue

            val = self.form.cleaned_data.get(field, False)
            
            if val: 
                
                # if field == 'Equation':
                #     id_list = list(AllometricEquation.objects.filter(Equation__icontains=val).values_list('ID', flat=True))
                #     id_list += list(AllometricEquation.objects.filter(Substitute_equation__icontains=val).values_list('ID', flat=True))
                #     field = 'id__in'
                #     val = id_list

                if field in  ['B', 'Bd', 'Bg', 'Bt', 'L', 'Rb', 'Rf', 'Rm', 'S', 'T', 'F']:
                    if val == 'Yes':
                        val = 1
                    elif val == 'No':
                        val = 0
                kwargs = {field : val}
                s = s.filter(**kwargs)

        return s
        
        
    def get_current_page(self):
        if self.query_entered() \
          and self.form.is_valid() \
          and self.form.cleaned_data.get('page'):
            return self.form.cleaned_data.get('page')
        else:
            return 1
    
    def next_page_link(self):
        return self.get_query_string({'page' : self.get_current_page(form)+1})
    
    def prev_page_link(self):
        return self.get_query_string({'page' : self.get_current_page(form) -1})

    def export_link(self):
        return self.get_query_string(export=True)

    def sort_link(self, field_name):
        try:
            current_order_by = self.form.cleaned_data['order_by']
        except:
            current_order_by = None

        if field_name == current_order_by and current_order_by[0:1] != '-':
            field_name = '-' + field_name


        return self.get_query_string(form=form, using_values={'page' : 1, 'order_by' : field_name})

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