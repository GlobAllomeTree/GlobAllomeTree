from django import forms

from globallometree.apps.wood_densities.models import (
    WoodDensity
    )

from globallometree.apps.base.forms import LinkedModelSearchForm

class WoodDensitySearchForm(LinkedModelSearchForm):

    def __init__(self, *args, **kwargs):
        super(WoodDensitySearchForm, self).__init__(*args, **kwargs)

    H_tree_avg__gte = forms.DecimalField(required=False,
        label='From')
    H_tree_avg__lte = forms.DecimalField(required=False,
        label='To')

    H_tree_min__gte = forms.DecimalField(required=False,
        label='From')
    H_tree_min__lte = forms.DecimalField(required=False,
        label='To')

    H_tree_max__gte = forms.DecimalField(required=False,
        label='From')
    H_tree_max__lte = forms.DecimalField(required=False,
        label='To')

    DBH_tree_min__gte = forms.DecimalField(required=False,
        label='From')
    DBH_tree_min__lte = forms.DecimalField(required=False,
        label='To')

    DBH_tree_max__gte = forms.DecimalField(required=False,
        label='From')
    DBH_tree_max__lte = forms.DecimalField(required=False,
        label='To')

    DBH_tree_avg__gte = forms.DecimalField(required=False,
        label='From')
    DBH_tree_avg__lte = forms.DecimalField(required=False,
        label='To')

    m_WD__gte = forms.DecimalField(required=False,
        label='From')
    m_WD__lte = forms.DecimalField(required=False,
        label='To')

    MC_m__gte = forms.DecimalField(required=False,
        label='From')
    MC_m__lte = forms.DecimalField(required=False,
        label='To')

    V_WD__gte = forms.DecimalField(required=False,
        label='From')
    V_WD__lte = forms.DecimalField(required=False,
        label='To')

    MC_V__gte = forms.DecimalField(required=False,
        label='From')
    MC_V__lte = forms.DecimalField(required=False,
        label='To')

    CR__gte = forms.DecimalField(required=False,
        label='From')
    CR__lte = forms.DecimalField(required=False,
        label='To')

    FSP__gte = forms.DecimalField(required=False,
        label='From')
    FSP__lte = forms.DecimalField(required=False,
        label='To')

    Methodology = forms.CharField(required=False, label='Methodology')

    Bark = forms.NullBooleanField(required=False, label='Bark included')

    Density_g_cm3__gte = forms.DecimalField(required=False,
        label='From')
    Density_g_cm3__lte = forms.DecimalField(required=False,
        label='To')

    MC_Density = forms.CharField(required=False, label='Moisture Content Code')

    Data_origin = forms.CharField(required=False, label='Data origin')

    Data_type = forms.CharField(required=False, label='Data type')

    Samples_per_tree__gte = forms.IntegerField(required=False,
        label='From')
    Samples_per_tree__lte = forms.IntegerField(required=False,
        label='To')

    Number_of_trees__gte = forms.IntegerField(required=False,
        label='From')
    Number_of_trees__lte = forms.IntegerField(required=False,
        label='To')

    SD__gte = forms.DecimalField(required=False,
        label='From')
    SD__lte = forms.DecimalField(required=False,
        label='To')

    Min__gte = forms.DecimalField(required=False,
        label='From')
    Min__lte = forms.DecimalField(required=False,
        label='To')

    Max__gte = forms.DecimalField(required=False,
        label='From')
    Max__lte = forms.DecimalField(required=False,
        label='To')

    H_measure__gte = forms.DecimalField(required=False,
        label='From')
    H_measure__lte = forms.DecimalField(required=False,
        label='To')

    Bark_distance__gte = forms.DecimalField(required=False,
        label='From')
    Bark_distance__lte = forms.DecimalField(required=False,
        label='To')
