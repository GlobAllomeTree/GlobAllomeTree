from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML
from .models import AllometricEquation, Ecosystem, Population
from globallometree.apps.locations.models import (
    Country, BiomeFAO, BiomeUdvardy, BiomeWWF, DivisionBailey, BiomeHoldridge
)
from globallometree.apps.taxonomy.models import Genus, Species

class SubmissionForm(forms.Form):
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
        super(SubmissionForm, self).__init__(*args, **kwargs)
    file  = forms.FileField(label="Equation Data File")
    notes = forms.CharField(required=False,
                            widget=forms.widgets.Textarea(
                                attrs={'style': "width:380px;height:80px;"}
                                )
                            )


class CountryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.common_name


COMPONENT_CHOICES = (
            ('', ''),
            ('No', 'No'),
            ('Yes', 'Yes')
        )

class SearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        #Add on initial arguments
        if not kwargs.get('initial', False):
            kwargs['initial'] = {}
        kwargs['initial']['page'] = 1

        super(SearchForm, self).__init__(*args, **kwargs)

        for select_name, select_label in (
            ('Biome_FAO', 'Biome (FAO)'),
            ('Biome_UDVARDY', 'Biome (UDVARDY)'),
            ('Biome_WWF','Biome (WWF)'),
            ('Division_BAILEY', 'Division (BAILEY)' ),
            ('Biome_HOLDRIDGE','Biome (HOLDRIDGE)'),
            ('Ecosystem','Ecosystem'),
            ('Population','Population'),
            ('Country','Country'),
            ('Output','Output'),
            ('Unit_U','Unit U'),
            ('Unit_V','Unit V'),
            ('Unit_W','Unit W'),
            ('Unit_X','Unit X'),
            ('Unit_Y','Unit Y'),
            ('Unit_Z','Unit Z'),
        ):
            if select_name == 'Country':
                #country_ids = AllometricEquation.objects.distinct('Country').values_list('Country', flat=True)
                choices = [('', '')] + list(Country.objects.all().values_list(
                    'common_name', 'common_name'
                ))
            elif select_name == 'Biome_FAO':
                choices = [('', '')] + list(BiomeFAO.objects.all().values_list(
                    'name', 'name'
                ))
            elif select_name == 'Biome_UDVARDY':
                choices = [('', '')] + list(BiomeUdvardy.objects.all().values_list(
                    'name', 'name'
                ))
            elif select_name == 'Biome_WWF':
                choices = [('', '')] + list(BiomeWWF.objects.all().values_list(
                    'name', 'name'
                ))
            elif select_name == 'Division_BAILEY':
                choices = [('', '')] + list(DivisionBailey.objects.all().values_list(
                    'name', 'name'
                ))
            elif select_name == 'Biome_HOLDRIDGE':
                choices = [('', '')] + list(BiomeHoldridge.objects.all().values_list(
                    'name', 'name'
                ))
            elif select_name == 'Ecosystem':
                choices = [('', '')] + list(Ecosystem.objects.all().values_list(
                    'name', 'name'
                ))
            elif select_name == 'Population':
                choices = [('', '')] + list(Population.objects.all().values_list(
                    'name', 'name'
                ))
            else:
                choices = [('', '')] + list(AllometricEquation.objects
                    .distinct(select_name).values_list(select_name, select_name))

            self.fields[select_name] = forms.ChoiceField(
                choices=choices, required=False, label=select_label
            )

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'q'
        )

    #Full Text
    q = forms.CharField(required=False, label='Keyword')
    
    #Ordering and paging
    order_by = forms.CharField(required=False, widget=forms.HiddenInput())
    page     = forms.IntegerField(required=False)
    
    #Search Fields
    Genus         = forms.CharField(required=False, label='Genus')
    Species       = forms.CharField(required=False, label='Species')

     
    X = forms.CharField(required=False, label='X')
    Unit_X = forms.CharField(required=False, label='Unit X')
    Z = forms.CharField(required=False, label='Z')
    Unit_Z = forms.CharField(required=False, label='Unit Z') 
    W = forms.CharField(required=False, label='W')
    Unit_W = forms.CharField(required=False, label='Unit W')
    U = forms.CharField(required=False, label='U')
    Unit_U = forms.CharField(required=False, label='Unit U') 
    V = forms.CharField(required=False, label='V')
    Unit_V = forms.CharField(required=False, label='Unit V')
    
    Min_X__gte = forms.DecimalField(required=False, label='Min X From')
    Min_X__lte = forms.DecimalField(required=False, label='Min X To')
 
    Max_X__gte = forms.DecimalField(required=False, label='Max X From')
    Max_X__lte = forms.DecimalField(required=False, label='Max X To')

    Min_Z__gte = forms.DecimalField(required=False, label='Min Z From')
    Min_Z__lte = forms.DecimalField(required=False, label='Min Z To')

    Max_Z__gte = forms.DecimalField(required=False, label='Max Z From')
    Max_Z__lte = forms.DecimalField(required=False, label='Max Z To')
    
    Output = forms.CharField(required=False, label='Output')
    Unit_Y = forms.CharField(required=False, label='Unit Y')
    
    B = forms.ChoiceField(choices=COMPONENT_CHOICES, required=False, label='B - Bark')
    Bd = forms.ChoiceField(choices=COMPONENT_CHOICES, required=False, label='Bd - Dead branches')
    Bg = forms.ChoiceField(choices=COMPONENT_CHOICES, required=False, label='Bg - Big branches')
    Bt = forms.ChoiceField(choices=COMPONENT_CHOICES, required=False, label='Bt - Thin branches')
    L = forms.ChoiceField(choices=COMPONENT_CHOICES, required=False, label='L - Leaves')
    Rb = forms.ChoiceField(choices=COMPONENT_CHOICES, required=False, label='Rb - Large roots')
    Rf = forms.ChoiceField(choices=COMPONENT_CHOICES, required=False, label='Rf - Fine roots')
    Rm = forms.ChoiceField(choices=COMPONENT_CHOICES, required=False, label='Rm - Medium roots')
    S = forms.ChoiceField(choices=COMPONENT_CHOICES, required=False, label='S - Stump')
    T = forms.ChoiceField(choices=COMPONENT_CHOICES, required=False, label='T - Trunks' )
    F = forms.ChoiceField(choices=COMPONENT_CHOICES, required=False, label='F - Fruit')

    Equation = forms.CharField(required=False, label='Equation')
    
    Author = forms.CharField(required=False, label='Author')
    Year = forms.CharField(required=False, label='Year')
    Reference = forms.CharField(required=False, label='Reference') 

    def search(self):
       
        if not self.is_valid():
            return self.searchqueryset.all()

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