from django import forms

from globallometree.apps.allometric_equations.models import (
    AllometricEquation, 
    Population 
    )

from globallometree.apps.base.forms import LinkedModelSearchForm, ComponentSearchForm


class AllometricEquationSearchForm(LinkedModelSearchForm, ComponentSearchForm):

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
    


    Equation = forms.CharField(required=False, label='Equation')




