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

    DBH_tree_avg__gte = forms.DecimalField(required=False,
        label='DBH tree avg From')
    DBH_tree_avg__lte = forms.DecimalField(required=False,
        label='DBH tree avg To')

    DBH_tree_min__gte = forms.DecimalField(required=False,
        label='DBH tree min From')
    DBH_tree_min__lte = forms.DecimalField(required=False,
        label='DBHH tree min To')

    DBH_tree_max__gte = forms.DecimalField(required=False,
        label='DBH tree max From')
    DBH_tree_max__lte = forms.DecimalField(required=False,
        label='DBHH tree max To')

    m_WD_max__gte = forms.DecimalField(required=False,
        label='Wood mass measured From')
    m_WD_min__lte = forms.DecimalField(required=False,
        label='Wood mass measured To')

    MC_m_max__gte = forms.DecimalField(required=False,
        label='Moisture content while measuring From')
    MC_m_min__lte = forms.DecimalField(required=False,
        label='Moisture content while measuring To')

    V_WD_max__gte = forms.DecimalField(required=False,
        label='Wood volume measured From')
    V_WD_min__lte = forms.DecimalField(required=False,
        label='Wood volume measured To')

    MC_V_max__gte = forms.DecimalField(required=False,
        label='Moisture content while measuring From')
    MC_V_min__lte = forms.DecimalField(required=False,
        label='Moisture content while measuring To')

    CR_max__gte = forms.DecimalField(required=False,
        label='Coefficient of retraction From')
    CR_min__lte = forms.DecimalField(required=False,
        label='Coefficient of retraction To')

    FSP_max__gte = forms.DecimalField(required=False,
        label='Fiber saturation point From')
    FSP_min__lte = forms.DecimalField(required=False,
        label='Fiber saturation point To')

    Methodology = forms.CharField(required=False, label='Methodology')

    Bark = forms.NullBooleanField(required=False, label='Bark included')

    Density_g_cm3_max__gte = forms.DecimalField(required=False,
        label='Wood density From')
    Density_g_cm3_min__lte = forms.DecimalField(required=False,
        label='Wood density To')

    MC_Density = forms.CharField(required=False, label='Moisture Content Code')

    Data_origin = forms.CharField(required=False, label='Data origin')

    Data_type = forms.CharField(required=False, label='Data type')

    Samples_per_tree_max__gte = forms.IntegerField(required=False,
        label='Samples per tree From')
    Samples_per_tree_min__lte = forms.IntegerField(required=False,
        label='Samples per tree To')

    Number_of_trees_max__gte = forms.IntegerField(required=False,
        label='Number of trees From')
    Number_of_trees_min__lte = forms.IntegerField(required=False,
        label='Number of trees To')

    SD_max__gte = forms.DecimalField(required=False,
        label='Standard deviation From')
    SD_min__lte = forms.DecimalField(required=False,
        label='Standard deviation To')

    Min_max__gte = forms.DecimalField(required=False,
        label='Min of WD From')
    Min_min__lte = forms.DecimalField(required=False,
        label='Min of WD To')

    Max_max__gte = forms.DecimalField(required=False,
        label='Max of WD From')
    Max_min__lte = forms.DecimalField(required=False,
        label='Max of WD To')

    H_measure_max__gte = forms.DecimalField(required=False,
        label='Height of sample From')
    H_measure_min__lte = forms.DecimalField(required=False,
        label='Height of sample To')

    Bark_distance_max__gte = forms.DecimalField(required=False,
        label='Distance where WD collected From')
    Bark_distance_min__lte = forms.DecimalField(required=False,
        label='Distance where WD collected To')
