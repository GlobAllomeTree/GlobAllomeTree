from django import forms

from globallometree.apps.locations.models import (
    Country, 
    ZoneFAO, 
    EcoregionUdvardy, 
    EcoregionWWF, 
    DivisionBailey, 
    ZoneHoldridge
)

from globallometree.apps.identification.models import (
    TreeType,
    VegetationType
)



COMPONENT_CHOICES = (
            ('', ''),
            ('0', 'No'),
            ('1', 'Yes')
        )

class ComponentSearchForm(forms.Form):

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


class LinkedModelSearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        
        super(LinkedModelSearchForm, self).__init__(*args, **kwargs)

        for select_name, select_label in (
            ('Zone_FAO', 'FAO Global Ecological Zone '),
            ('Ecoregion_Udvardy', 'Udvardy Ecoregion'),
            ('Ecoregion_WWF','WWF Terrestrial Ecoregion'),
            ('Division_Bailey', 'Division Bailey' ),
            ('Zone_Holdridge','Holdridge Life Zone'),
            ('Population','Population'),
            ('Country','Country'),
            ('Vegetation_type','Vegetation Type'),
            ('Tree_type','Tree Type'),
        ):
            if select_name == 'Country':
                choices = [('', '')] + list(Country.objects.all().values_list(
                    'Formal_name', 'Formal_name'
                ))
            elif select_name == 'Zone_FAO':
                choices = [('', '')] + list(ZoneFAO.objects.all().values_list(
                    'Name', 'Name'
                ))
            elif select_name == 'Ecoregion_Udvardy':
                choices = [('', '')] + list(EcoregionUdvardy.objects.all().values_list(
                    'Name', 'Name'
                ))
            elif select_name == 'Ecoregion_WWF':
                choices = [('', '')] + list(EcoregionWWF.objects.all().values_list(
                    'Name', 'Name'
                ))
            elif select_name == 'Division_Bailey':
                choices = [('', '')] + list(DivisionBailey.objects.all().values_list(
                    'Name', 'Name'
                ))
            elif select_name == 'Zone_Holdridge':
                choices = [('', '')] + list(ZoneHoldridge.objects.all().values_list(
                    'Name', 'Name'
                ))  
            elif select_name == 'Vegetation_type':
                choices = [('', '')] + list(VegetationType.objects.all().values_list(
                    'Name', 'Name'
                ))  
            elif select_name == 'Tree_type':
                choices = [('', '')] + list(TreeType.objects.all().values_list(
                    'Name', 'Name'
                ))  
     
            self.fields[select_name] = forms.ChoiceField(
                choices=choices, required=False, label=select_label
            )

    #Full Text
    q = forms.CharField(required=False, label='Keyword')
  
    
    #Taxonomy Fields
    Family        = forms.CharField(required=False, label='Family')
    Genus         = forms.CharField(required=False, label='Genus')
    Species       = forms.CharField(required=False, label='Species')

    #Bounding Box 
    Min_Latitude = forms.DecimalField(required=False, label='Min Latitude')
    Max_Latitude = forms.DecimalField(required=False, label='Max Latitude')
    Min_Longitude = forms.DecimalField(required=False, label='Min Longitude')
    Max_Longitude = forms.DecimalField(required=False, label='Max Longitude')

    #Distance from Point
    Point_Latitude = forms.DecimalField(required=False, label='Center Point Latitude')
    Point_Longitude = forms.DecimalField(required=False, label='Center Point Longitude')
    Point_Distance = forms.DecimalField(required=False, label='Distance From Center Point in Kilometers')

    # Reference Tab
    Reference_author = forms.CharField(required=False, label='Author')
    Reference_year = forms.CharField(required=False, label='Year')
    Reference = forms.CharField(required=False, label='Reference') 

