from django import forms
from haystack.forms import SearchForm
from apps.data.models import Country

class CountryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.common_name


class EquationSearchForm(SearchForm):
    
    #Full Text
    q = forms.CharField(required=False, label='Keyword')
    
    #Ordering
    order_by = forms.CharField(required=False)
        
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
            
            
        #Send used fields to the query set
        for field in ['population',
                      'ecosystem',
                      'genus',
                      'species',
                      'country',
                      'biome_FAO',
                      'biome_UDVARDY',
                      'biome_WWF',
                      'division_BAILEY',
                      'biome_HOLDRIDGE',
                      'X',
                      'unit_X',
                      'Z',
                      'unit_Z',
                      'W',
                      'unit_W',
                      'U',
                      'unit_U',
                      'V',
                      'unit_V',
                      'output',
                      'unit_Y',
                      'B',
                      'Bd',
                      'Bg',
                      'Bt',
                      'L',
                      'Rb',
                      'Rf',
                      'Rm',
                      'S',
                      'T',
                      'F',
                      'equation_y',
                      'author',
                      'reference',
                      'year',
                      'min_X__gte',
                      'max_X__gte',
                      'min_H__gte',
                      'max_H__gte',
                      'min_X__lte',
                      'max_X__lte',
                      'min_H__lte',
                      'max_H__lte'
                      ]:
            
            # Check to see if the field was used in the search and non empty
            if self.cleaned_data[field]:
                kwargs = {field : self.cleaned_data.get(field)}
                sqs = sqs.filter(**kwargs)
        
       
        
        return sqs
        
 
    def get_data_query_string(self):
    
        return '?q='       + self.cleaned_data['q'] + \
               '&genus='   + self.cleaned_data['genus'] + \
               '&species='   + self.cleaned_data['species'] 