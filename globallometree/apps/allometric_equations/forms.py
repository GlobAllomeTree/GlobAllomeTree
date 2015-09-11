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
    


    Output = forms.CharField(required=False, label='Output')

    Equation = forms.CharField(required=False, label='Equation')




