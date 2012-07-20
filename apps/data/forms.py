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
            
            
        #Char and ngram fields
        for field in ['population',
                      'ecosystem',
                      'genus',
                      'species',
                      'country',]:
            
            # Check to see if a genus was chosen.
            if self.cleaned_data[field]:
                kwargs = {field : self.cleaned_data.get(field)}
                sqs = sqs.filter(**kwargs)
          
        return sqs
        
 
    def get_data_query_string(self):
    
        return '?q='       + self.cleaned_data['q'] + \
               '&genus='   + self.cleaned_data['genus'] + \
               '&species='   + self.cleaned_data['species'] 