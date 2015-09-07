from django import forms

from globallometree.apps.raw_data.models import (
    RawData
    )

from globallometree.apps.base.forms import LinkedModelSearchForm, ComponentSearchForm


class RawDataSearchForm(LinkedModelSearchForm, ComponentSearchForm):

    def __init__(self, *args, **kwargs):
        super(RawDataSearchForm, self).__init__(*args, **kwargs)

    H_m__gte = forms.DecimalField(required=False,
        label='Tree Height From (m)')
    H_m__lte = forms.DecimalField(required=False,
        label='Tree Height To (m)')

    DBH_cm__gte = forms.DecimalField(required=False,
        label='Diameter From (cm)')
    DBH_cm__lte = forms.DecimalField(required=False,
        label='Diameter To (cm)')

    Volume_m3__gte = forms.DecimalField(required=False,
        label='Volume From (m<sup>3</sup>)')
    Volume_m3__lte = forms.DecimalField(required=False,
        label='Volume To (m<sup>3</sup>)')

  