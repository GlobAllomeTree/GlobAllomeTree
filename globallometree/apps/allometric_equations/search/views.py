from django.conf import settings
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

#import the S object from contrib which reads settings.ES_URLS
from elasticutils.contrib.django import S

from .forms import SearchForm
from .indices import AllometricEquationIndex

class SearchView(FormView):
    template_name = 'allometric_equations/template.search.html'
    form_class = SearchForm

    def form_valid(self, form):
        pass

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)

    	results = self.search()

    	for result in results[0:10]:
    		print result
         
        context['is_page_data'] =  True
        context['query_entered'] = self.query_entered()

        return context

    def query_entered(self):
        return bool(len(self.request.GET.keys()))

    def create_response(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        return super(SearchView, self).create_response( *args, **kwargs)


    def search(self):
       
       	s = S(AllometricEquationIndex)

       	return s[0:40]

        if not self.query_entered():
            return s[0:40]

        sqs = self.searchqueryset.all()
        # import pdb;pdb.set_trace()
        if self.cleaned_data.get('q'):
            sqs = sqs.auto_query(self.cleaned_data['q'])

        # ORDERING 
        # Check to see if a order_by field was chosen.
        if self.cleaned_data.get('order_by'):
            sqs = sqs.order_by(self.cleaned_data.get('order_by'))
        
        #Send search fields to the the sqs.filter
        for field in self.cleaned_data:
        
            if field in ['q', 'order_by', 'page']:
                continue

            val = self.cleaned_data.get(field, False)
            if val: 
                
                if field == 'Equation':
                    id_list = list(AllometricEquation.objects.filter(Equation__icontains=val).values_list('ID', flat=True))
                    id_list += list(AllometricEquation.objects.filter(Substitute_equation__icontains=val).values_list('ID', flat=True))
                    field = 'id__in'
                    val = id_list

                elif field in  ['B', 'Bd', 'Bg', 'Bt', 'L', 'Rb', 'Rf', 'Rm', 'S', 'T', 'F']:
                    if val == 'Yes':
                        val = 1
                    elif val == 'No':
                        val = 0
               
                kwargs = {field : val}
                sqs = sqs.filter(**kwargs)

        return sqs
        
        
    def get_current_page(self):
        if self.is_valid():
            return  self.cleaned_data.get('page')
        return 1
    
    def next_page_link(self):
        return self.get_query_string({'page' : self.get_current_page()+1})
    
    def prev_page_link(self):
        return self.get_query_string({'page' : self.get_current_page() -1})

    def export_link(self):
        return self.get_query_string(export=True)

    # todo - reinstate sort links for templates
    # def __getattribute__(self, name):
    #     if name.startswith('sort_link_'):
    #         return self.sort_link(name.replace('sort_link_', ''))
    #     else:
    #         # Default behaviour
    #         return BaseSearchForm.__getattribute__(self, name)

    def sort_link(self, field_name):
        try:
            current_order_by = self.cleaned_data['order_by']
        except:
            current_order_by = None

        if field_name == current_order_by and current_order_by[0:1] != '-':
            field_name = '-' + field_name


        return self.get_query_string({'page' : 1, 'order_by' : field_name})

    def current_search_summary(self):
        current_search = []
        if not self.is_valid():
            return []
        #Send search fields to the the sqs.filter
        for field in self.cleaned_data:
        
            if field in ['order_by', 'page']:
                continue
            if self.cleaned_data.get(field, False): 
                current_search.append( {'field' : self.fields[field].label,
                                        'search_value' :  self.cleaned_data.get(field),
                                        'clear_link'   :  self.get_query_string({'page' : 1,
                                                                                field : ''})
                                    })
        return current_search     
 
    def get_query_string(self, using_values = {}, export=False):
    
        query_dict = {}
        query_string = ''
        first = True
       
        #Send search fields to the the sqs.filter
        if self.is_valid():
            for field in self.cleaned_data:
                if self.cleaned_data.get(field, False):
                    query_dict[field] = self.cleaned_data.get(field)
        
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