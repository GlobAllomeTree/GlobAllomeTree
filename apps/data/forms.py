from django import forms
from haystack.forms import SearchForm
#from DB_MIXED.models import country as Country

class EquationSearchForm(SearchForm):
    q = forms.CharField(required=False, label='Keyword')
    genus    = forms.CharField(required=False)
    species  = forms.CharField(required=False)
    order_by = forms.CharField(required=False)
#    country = forms.ModelChoiceField(queryset = Country.objects.all() )


    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(EquationSearchForm, self).search()

        if hasattr(self, 'cleaned_data'):
    
            # Check to see if a genus was chosen.
            if self.cleaned_data['genus']:
                sqs = sqs.filter(genus=self.cleaned_data['genus'])
           
            # Check to see if a species was chosen.
            if self.cleaned_data['species']:
                sqs = sqs.filter(species=self.cleaned_data['species'])
              
            # Check to see if a order_by field was chosen.
            if self.cleaned_data['order_by']:
                sqs = sqs.order_by(self.cleaned_data['order_by'])
    
            return sqs
        
    def no_query_found(self):
        #Define the behavior when there is no initial query
        return self.searchqueryset.all()
    
    def get_data_query_string(self):
    
        return '?q='       + self.cleaned_data['q'] + \
               '&genus='   + self.cleaned_data['genus'] + \
               '&species='   + self.cleaned_data['species'] 