from django import forms
from haystack.forms import SearchForm
from apps.data.models import Country

class CountryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.common_name


class EquationSearchForm(SearchForm):
    
    def __init__(self, *args, **kwargs):
        #Add on initial arguments
        if not kwargs.get('initial', False):
            kwargs['initial'] = {}
        kwargs['initial']['page'] = 1
        return super(EquationSearchForm, self).__init__(*args, **kwargs)



    #Full Text
    q = forms.CharField(required=False, label='Keyword')
    
    #Ordering and paging
    order_by = forms.CharField(required=False, widget=forms.HiddenInput())
    page     = forms.IntegerField(required=False)
    
    #Search Fields    
    population    = forms.CharField(required=False)
    ecosystem     = forms.CharField(required=False)
    genus         = forms.CharField(required=False)
    species       = forms.CharField(required=False)
    country       = forms.CharField(required=False)


    biome_FAO                       = forms.CharField(required=False)
    biome_UDVARDY                   = forms.CharField(required=False)
    biome_WWF                       = forms.CharField(required=False)
    division_BAILEY                 = forms.CharField(required=False) 
    biome_HOLDRIDGE                 = forms.CharField(required=False)
     
    X                               = forms.CharField(required=False)
    unit_X                          = forms.CharField(required=False)
    Z                               = forms.CharField(required=False)
    unit_Z                          = forms.CharField(required=False) 
    W                               = forms.CharField(required=False)
    unit_W                          = forms.CharField(required=False)
    U                               = forms.CharField(required=False)
    unit_U                          = forms.CharField(required=False) 
    V                               = forms.CharField(required=False)
    unit_V                          = forms.CharField(required=False)
    
    min_X__gte                      = forms.DecimalField(required=False)
    min_X__lte                      = forms.DecimalField(required=False)
 
    max_X__gte                      = forms.DecimalField(required=False)
    max_X__lte                      = forms.DecimalField(required=False)

    min_H__gte                      = forms.DecimalField(required=False)
    min_H__lte                      = forms.DecimalField(required=False)

    max_H__gte                      = forms.DecimalField(required=False)
    max_H__lte                      = forms.DecimalField(required=False)
    
    output                          = forms.CharField(required=False)
    unit_Y                          = forms.CharField(required=False)
    
    B                               = forms.BooleanField(required=False)
    Bd                              = forms.BooleanField(required=False)
    Bg                              = forms.BooleanField(required=False)
    Bt                              = forms.BooleanField(required=False)
    L                               = forms.BooleanField(required=False)
    Rb                              = forms.BooleanField(required=False)
    Rf                              = forms.BooleanField(required=False)
    Rm                              = forms.BooleanField(required=False)
    S                               = forms.BooleanField(required=False)
    T                               = forms.BooleanField(required=False)
    F                               = forms.BooleanField(required=False)
    
    equation_y                      = forms.CharField(required=False)
    
    author                          = forms.CharField(required=False)
    year                            = forms.IntegerField(required=False)
    reference                       = forms.CharField(required=False) 


    def search(self):
       
        if not self.is_valid():
            return self.searchqueryset.all()

        sqs = self.searchqueryset.all()
        
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
            if self.cleaned_data.get(field, False): 
                kwargs = {field : self.cleaned_data.get(field)}
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
 
    def get_query_string(self, using_values = {}):
    
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
            
        
        
        for field in query_dict.keys():
            if first:
                c = '?'
                first = False
            else:
                c = '&'
                
            query_string += '%s%s=%s' % (c, field, query_dict[field])
                    
        return query_string
        