from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML


from ..models import AllometricEquation, Population
from globallometree.apps.locations.models import (
    Country, BiomeFAO, BiomeUdvardy, BiomeWWF, DivisionBailey, BiomeHoldridge
)
from globallometree.apps.taxonomy.models import Genus, Species


class CountryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.common_name


COMPONENT_CHOICES = (
            ('', ''),
            ('0', 'No'),
            ('1', 'Yes')
        )


class SearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        

        super(SearchForm, self).__init__(*args, **kwargs)

        for select_name, select_label in (
            ('Biome_FAO', 'Biome (FAO)'),
            ('Biome_UDVARDY', 'Biome (UDVARDY)'),
            ('Biome_WWF','Biome (WWF)'),
            ('Division_BAILEY', 'Division (BAILEY)' ),
            ('Biome_HOLDRIDGE','Biome (HOLDRIDGE)'),
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

    #Bounding Box 
    Min_Latitude = forms.DecimalField(required=False, label='Min Latitude')
    Max_Latitude = forms.DecimalField(required=False, label='Max Latitude')
    Min_Longitude = forms.DecimalField(required=False, label='Min Longitude')
    Max_Longitude = forms.DecimalField(required=False, label='Max Longitude')

    #Distance from Point
    Point_Latitude = forms.DecimalField(required=False, label='Center Point Latitude')
    Point_Longitude = forms.DecimalField(required=False, label='Center Point Longitude')
    Point_Distance = forms.DecimalField(required=False, label='Distance From Center Point in Kilometers')

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

