from django import forms

from globallometree.apps.wood_densities.models import (
    WoodDensity
    )

from globallometree.apps.search_helpers.forms import LinkedModelSearchForm

class WoodDensitySearchForm(LinkedModelSearchForm):

    def __init__(self, *args, **kwargs):
        super(WoodDensitySearchForm, self).__init__(*args, **kwargs)

