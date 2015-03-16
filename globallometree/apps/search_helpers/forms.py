from django import forms

from globallometree.apps.locations.models import (
    Country, 
    BiomeFAO, 
    BiomeUdvardy, 
    BiomeWWF, 
    DivisionBailey, 
    BiomeHoldridge
)

class LinkedModelSearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        
        super(LinkedModelSearchForm, self).__init__(*args, **kwargs)

        for select_name, select_label in (
            ('Biome_FAO', 'Biome (FAO)'),
            ('Biome_UDVARDY', 'Biome (UDVARDY)'),
            ('Biome_WWF','Biome (WWF)'),
            ('Division_BAILEY', 'Division (BAILEY)' ),
            ('Biome_HOLDRIDGE','Biome (HOLDRIDGE)'),
            ('Population','Population'),
            ('Country','Country')
        ):
            if select_name == 'Country':
                choices = [('', '')] + list(Country.objects.all().values_list(
                    'Formal_name', 'Formal_name'
                ))
            elif select_name == 'Biome_FAO':
                choices = [('', '')] + list(BiomeFAO.objects.all().values_list(
                    'Name', 'Name'
                ))
            elif select_name == 'Biome_UDVARDY':
                choices = [('', '')] + list(BiomeUdvardy.objects.all().values_list(
                    'Name', 'Name'
                ))
            elif select_name == 'Biome_WWF':
                choices = [('', '')] + list(BiomeWWF.objects.all().values_list(
                    'Name', 'Name'
                ))
            elif select_name == 'Division_BAILEY':
                choices = [('', '')] + list(DivisionBailey.objects.all().values_list(
                    'Name', 'Name'
                ))
            elif select_name == 'Biome_HOLDRIDGE':
                choices = [('', '')] + list(BiomeHoldridge.objects.all().values_list(
                    'Name', 'Name'
                ))  

            self.fields[select_name] = forms.ChoiceField(
                choices=choices, required=False, label=select_label
            )

    #Full Text
    q = forms.CharField(required=False, label='Keyword')
    
    #Ordering and paging
    order_by = forms.CharField(required=False, widget=forms.HiddenInput())
    
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
    Author = forms.CharField(required=False, label='Author')
    Year = forms.CharField(required=False, label='Year')
    Reference = forms.CharField(required=False, label='Reference') 

