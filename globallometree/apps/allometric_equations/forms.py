from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML
from .models import AllometricEquation, Population
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
