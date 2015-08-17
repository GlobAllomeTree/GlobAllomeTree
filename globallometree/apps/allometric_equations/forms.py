from django import forms

from apps.allometric_equations.models import (
    AllometricEquation, 
    Population 
    )

from apps.search_helpers.forms import LinkedModelSearchForm

COMPONENT_CHOICES = (
            ('', ''),
            ('0', 'No'),
            ('1', 'Yes')
        )



class AllometricEquationSearchForm(LinkedModelSearchForm):

    def __init__(self, *args, **kwargs):
        
        super(AllometricEquationSearchForm, self).__init__(*args, **kwargs)

        for select_name, select_label in (
            ('Population','Population'),
            ('Output','Output'),
            ('Unit_U','Unit U'),
            ('Unit_V','Unit V'),
            ('Unit_W','Unit W'),
            ('Unit_X','Unit X'),
            ('Unit_Z','Unit Z'),
        ):

            if select_name == 'Population':
                choices = [('', '')] + list(Population.objects.all().values_list(
                    'Name', 'Name'
                ))
            else:
                choices = [('', '')] + list(AllometricEquation.objects
                    .distinct(select_name).values_list(select_name, select_name))

            self.fields[select_name] = forms.ChoiceField(
                choices=choices, required=False, label=select_label
            )
    
    X = forms.CharField(required=False, label='X')
    Z = forms.CharField(required=False, label='Z')
    W = forms.CharField(required=False, label='W')
    U = forms.CharField(required=False, label='U')
    V = forms.CharField(required=False, label='V')

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




