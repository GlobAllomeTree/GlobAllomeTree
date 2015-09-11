from django import forms

from globallometree.apps.raw_data.models import (
    RawData
    )

from globallometree.apps.base.forms import LinkedModelSearchForm, ComponentSearchForm


class RawDataSearchForm(LinkedModelSearchForm, ComponentSearchForm):

    def __init__(self, *args, **kwargs):
        super(RawDataSearchForm, self).__init__(*args, **kwargs)

    H_m__gte = forms.DecimalField(required=False,
        label='From')
    H_m__lte = forms.DecimalField(required=False,
        label='To')

    DBH_cm__gte = forms.DecimalField(required=False,
        label='From')
    DBH_cm__lte = forms.DecimalField(required=False,
        label='To')

    Volume_m3__gte = forms.DecimalField(required=False,
        label='From')
    Volume_m3__lte = forms.DecimalField(required=False,
        label='To')

  