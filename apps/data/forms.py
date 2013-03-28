from django import forms
from haystack.forms import SearchForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML
from .models import TreeEquation

class DataSubmissionForm(forms.Form):
    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Submit Data', #Fieldset Title
                 HTML("""
                    <p>Use this form to submit your data to GlobAllomeTree</p>
                 """),
                'file', #Form Fields
                'notes'
            ),
            ButtonHolder(
                Submit('submit', 'Submit Data', css_class='button btn-success pull-right')
            )
        )
        super(DataSubmissionForm, self).__init__(*args, **kwargs)
    file  = forms.FileField(label="Equation Data File")
    notes = forms.CharField(required=False,
                            widget=forms.widgets.Textarea(
                                attrs={'style': "width:380px;height:80px;"}
                                )
                            )


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
    Population    = forms.CharField(required=False, label='Population')
    Ecosystem     = forms.CharField(required=False, label='Ecosystem')
    Genus         = forms.CharField(required=False, label='Genus')
    Species       = forms.CharField(required=False, label='Species')
    Country       = forms.CharField(required=False, label='Country')


    Biome_FAO                       = forms.CharField(required=False, label='Biome (FAO)')
    Biome_UDVARDY                   = forms.CharField(required=False, label='Biome (UDVARDY)')
    Biome_WWF                       = forms.CharField(required=False, label='Biome (WWF)')
    Division_BAILEY                 = forms.CharField(required=False, label='Division (BAILEY)') 
    Biome_HOLDRIDGE                 = forms.CharField(required=False, label='Biome (HOLDRIDGE)')
     
    X                               = forms.CharField(required=False, label='X')
    Unit_X                          = forms.CharField(required=False, label='Unit X')
    Z                               = forms.CharField(required=False, label='Z')
    Unit_Z                          = forms.CharField(required=False, label='Unit Z') 
    W                               = forms.CharField(required=False, label='W')
    Unit_W                          = forms.CharField(required=False, label='Unit W')
    U                               = forms.CharField(required=False, label='U')
    Unit_U                          = forms.CharField(required=False, label='Unit U') 
    V                               = forms.CharField(required=False, label='V')
    Unit_V                          = forms.CharField(required=False, label='Unit V')
    
    Min_X__gte                      = forms.DecimalField(required=False, label='Min X From')
    Min_X__lte                      = forms.DecimalField(required=False, label='Min X To')
 
    Max_X__gte                      = forms.DecimalField(required=False, label='Max X From')
    Max_X__lte                      = forms.DecimalField(required=False, label='Max X To')

    Min_Z__gte                      = forms.DecimalField(required=False, label='Min Z From')
    Min_Z__lte                      = forms.DecimalField(required=False, label='Min Z To')

    Max_Z__gte                      = forms.DecimalField(required=False, label='Max Z From')
    Max_Z__lte                      = forms.DecimalField(required=False, label='Max Z To')
    
    Output                          = forms.CharField(required=False, label='Output')
    Unit_Y                          = forms.CharField(required=False, label='Unit Y')
    
    B                               = forms.BooleanField(required=False, label='B')
    Bd                              = forms.BooleanField(required=False, label='Bd')
    Bg                              = forms.BooleanField(required=False, label='Bg')
    Bt                              = forms.BooleanField(required=False, label='Bt')
    L                               = forms.BooleanField(required=False, label='L')
    Rb                              = forms.BooleanField(required=False, label='Rb')
    Rf                              = forms.BooleanField(required=False, label='Rf')
    Rm                              = forms.BooleanField(required=False, label='Rm')
    S                               = forms.BooleanField(required=False, label='S')
    T                               = forms.BooleanField(required=False, label='T')
    F                               = forms.BooleanField(required=False, label='F')
    
    Equation                        = forms.CharField(required=False, label='Equation')
    
    Author                          = forms.CharField(required=False, label='Author')
    Year                            = forms.IntegerField(required=False, label='Year')
    Reference                       = forms.CharField(required=False, label='Reference') 


    def search(self):
       
        if not self.is_valid():
            return self.searchqueryset.all()

        sqs = self.searchqueryset.all()
        
        if self.cleaned_data.get('q'):
            sqs = sqs.auto_query(self.cleaned_data['q'])
    
        #import pdb;pdb.set_trace()
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
                
                if field == 'Equation' and val:
                    val = TreeEquation.objects.filter(Equation__icontains=val).values_list('ID', flat=True)
                    field = 'id__in'

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

    def __getattribute__(self, name):
        if name.startswith('sort_link_'):
            return self.sort_link(name.replace('sort_link_', ''))
        else:
            # Default behaviour
            return SearchForm.__getattribute__(self, name)

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