from django import forms

from globallometree.apps.wood_densities.models import (
    WoodDensity
    )

from globallometree.apps.search_helpers.forms import LinkedModelSearchForm

class WoodDensitySearchForm(LinkedModelSearchForm):

    def __init__(self, *args, **kwargs):
        super(WoodDensitySearchForm, self).__init__(*args, **kwargs)

    H_tree_avg__gte = forms.DecimalField(required=False,
        label='H tree avg From')
    H_tree_avg__lte = forms.DecimalField(required=False,
        label='H tree avg To')

    H_tree_min__gte = forms.DecimalField(required=False,
        label='H tree min From')
    H_tree_min__lte = forms.DecimalField(required=False,
        label='H tree min To')

    H_tree_max__gte = forms.DecimalField(required=False,
        label='H tree max From')
    H_tree_max__lte = forms.DecimalField(required=False,
        label='H tree max To')

    DBH_tree_min__gte = forms.DecimalField(required=False,
        label='DBH tree avg From')
    DBH_tree_min__lte = forms.DecimalField(required=False,
        label='DBH tree avg To')

    DBH_tree_max__gte = forms.DecimalField(required=False,
        label='DBH tree min From')
    DBH_tree_max__lte = forms.DecimalField(required=False,
        label='DBHH tree min To')

    DBH_tree_avg__gte = forms.DecimalField(required=False,
        label='DBH tree max From')
    DBH_tree_avg__lte = forms.DecimalField(required=False,
        label='DBHH tree max To')

    m_WD__gte = forms.DecimalField(required=False,
        label='Wood mass measured From')
    m_WD__lte = forms.DecimalField(required=False,
        label='Wood mass measured To')

    MC_m__gte = forms.DecimalField(required=False,
        label='Moisture content while measuring From')
    MC_m__lte = forms.DecimalField(required=False,
        label='Moisture content while measuring To')

    V_WD__gte = forms.DecimalField(required=False,
        label='Wood volume measured From')
    V_WD__lte = forms.DecimalField(required=False,
        label='Wood volume measured To')

    MC_V__gte = forms.DecimalField(required=False,
        label='Moisture content while measuring From')
    MC_V__lte = forms.DecimalField(required=False,
        label='Moisture content while measuring To')

    CR__gte = forms.DecimalField(required=False,
        label='Coefficient of retraction From')
    CR__lte = forms.DecimalField(required=False,
        label='Coefficient of retraction To')

    FSP__gte = forms.DecimalField(required=False,
        label='Fiber saturation point From')
    FSP__lte = forms.DecimalField(required=False,
        label='Fiber saturation point To')

    Methodology = forms.CharField(required=False, label='Methodology')

    Bark = forms.NullBooleanField(required=False, label='Bark included')

    Density_g_cm3__gte = forms.DecimalField(required=False,
        label='Wood density From')
    Density_g_cm3__lte = forms.DecimalField(required=False,
        label='Wood density To')

    MC_Density = forms.CharField(required=False, label='Moisture Content Code')

    Data_origin = forms.CharField(required=False, label='Data origin')

    Data_type = forms.CharField(required=False, label='Data type')

    Samples_per_tree__gte = forms.IntegerField(required=False,
        label='Samples per tree From')
    Samples_per_tree__lte = forms.IntegerField(required=False,
        label='Samples per tree To')

    Number_of_trees__gte = forms.IntegerField(required=False,
        label='Number of trees From')
    Number_of_trees__lte = forms.IntegerField(required=False,
        label='Number of trees To')

    SD__gte = forms.DecimalField(required=False,
        label='Standard deviation From')
    SD__lte = forms.DecimalField(required=False,
        label='Standard deviation To')

    Min__gte = forms.DecimalField(required=False,
        label='Min of WD From')
    Min__lte = forms.DecimalField(required=False,
        label='Min of WD To')

    Max__gte = forms.DecimalField(required=False,
        label='Max of WD From')
    Max__lte = forms.DecimalField(required=False,
        label='Max of WD To')

    H_measure__gte = forms.DecimalField(required=False,
        label='Height of sample From')
    H_measure__lte = forms.DecimalField(required=False,
        label='Height of sample To')

    Bark_distance__gte = forms.DecimalField(required=False,
        label='Distance where WD collected From')
    Bark_distance__lte = forms.DecimalField(required=False,
        label='Distance where WD collected To')
