from django import forms

from globallometree.apps.biomass_expansion_factors.models import (
    BiomassExpansionFactor
    )

from globallometree.apps.base.forms import LinkedModelSearchForm

class BiomassExpansionFactorSearchForm(LinkedModelSearchForm):

    def __init__(self, *args, **kwargs):
        super(BiomassExpansionFactorSearchForm, self).__init__(*args, **kwargs)

    Growing_stock__gte = forms.DecimalField(required=False,
        label='Growing stock From')
    Growing_stock__lte = forms.DecimalField(required=False,
        label='Growing stock To')

    Aboveground_biomass__gte = forms.DecimalField(required=False,
        label='Aboveground biomass From')
    Aboveground_biomass__lte = forms.DecimalField(required=False,
        label='Aboveground biomass To')

    Net_annual_increment__gte = forms.DecimalField(required=False,
        label='Net annual increment From')
    Net_annual_increment__lte = forms.DecimalField(required=False,
        label='Net annual increment To')

    Stand_density__gte = forms.DecimalField(required=False,
        label='Stand density From')
    Stand_density__lte = forms.DecimalField(required=False,
        label='Stand density To')

    Age__gte = forms.IntegerField(required=False,
        label='Age From')
    Age__lte = forms.IntegerField(required=False,
        label='Age To')

    BEF__gte = forms.DecimalField(required=False,
        label='BEF From')
    BEF__lte = forms.DecimalField(required=False,
        label='BEF To')

    Input = forms.CharField(required=False, label='Input')

    Output = forms.CharField(required=False, label='Output')

    Interval_validity = forms.CharField(required=False, label='Interval validity')
