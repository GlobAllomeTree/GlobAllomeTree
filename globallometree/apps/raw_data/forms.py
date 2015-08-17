from django import forms

from apps.raw_data.models import (
    RawData
    )

from apps.search_helpers.forms import LinkedModelSearchForm

class RawDataSearchForm(LinkedModelSearchForm):

    def __init__(self, *args, **kwargs):
        super(RawDataSearchForm, self).__init__(*args, **kwargs)

    H_tree_avg__gte = forms.DecimalField(required=False,
        label='H tree avg From')
    H_tree_avg__lte = forms.DecimalField(required=False,
        label='H tree avg To')

    Forest_type = forms.CharField(required=False, label='Forest type')

    Tree_ID__gte = forms.IntegerField(required=False,
        label='Tree ID From')
    Tree_ID__lte = forms.DecimalField(required=False,
        label='Tree ID To')

    Date_collection__gte = forms.DateField(required=False,
        label='Collection date From')
    Date_collection__lte = forms.DateField(required=False,
        label='Collection date To')

    DBH_cm__gte = forms.DecimalField(required=False,
        label='DBH tree in cm From')
    DBH_cm__lte = forms.DecimalField(required=False,
        label='DBHH tree in cm To')

    H_m__gte = forms.DecimalField(required=False,
        label='Tree height in m From')
    H_m__lte = forms.DecimalField(required=False,
        label='Tree height in m To')

    CD_m__gte = forms.DecimalField(required=False,
        label='Crown diameter in m From')
    CD_m__lte = forms.DecimalField(required=False,
        label='Crown diameter in m To')

    F_Bole_kg__gte = forms.DecimalField(required=False,
        label='Fresh bole weight in kg From')
    F_Bole_kg__lte = forms.DecimalField(required=False,
        label='Fresh bole weight in kg To')

    F_Branch_kg__gte = forms.DecimalField(required=False,
        label='Fresh branches weight in kg From')
    F_Branch_kg__lte = forms.DecimalField(required=False,
        label='Fresh branches weight in kg To')

    F_Foliage_kg__gte = forms.DecimalField(required=False,
        label='Fresh foliage weight in kg From')
    F_Foliage_kg__lte = forms.DecimalField(required=False,
        label='Fresh foliage weight in kg To')

    F_Stump_kg__gte = forms.DecimalField(required=False,
        label='Fresh stump weight in kg From')
    F_Stump_kg__lte = forms.DecimalField(required=False,
        label='Fresh stump weight in kg To')

    F_Buttress_kg__gte = forms.DecimalField(required=False,
        label='Fresh buttress weight in kg From')
    F_Buttress_kg__lte = forms.DecimalField(required=False,
        label='Fresh buttress weight in kg To')

    F_Roots_kg__gte = forms.DecimalField(required=False,
        label='Fresh roots weight in kg From')
    F_Roots_kg__lte = forms.DecimalField(required=False,
        label='Fresh roots weight in kg To')

    Volume_m3__gte = forms.DecimalField(required=False,
        label='Total volume of tree in m3 From')
    Volume_m3__lte = forms.DecimalField(required=False,
        label='Total volume of tree in m3 To')

    Volume_bole_m3__gte = forms.DecimalField(required=False,
        label='Volume of bole in m3 From')
    Volume_bole_m3__lte = forms.DecimalField(required=False,
        label='Volumn of bole in m3 To')

    WD_AVG_gcm3__gte = forms.DecimalField(required=False,
        label='Avg WD for tree in g/cm3 From')
    WD_AVG_gcm3__lte = forms.DecimalField(required=False,
        label='Avg WD for tree in g/cm3 To')

    DF_Bole_AVG__gte = forms.DecimalField(required=False,
        label='Avg bole weight ratio dry/fresh From')
    DF_Bole_AVG__lte = forms.DecimalField(required=False,
        label='Avg bole weight ratio dry/fresh To')

    DF_Branch_AVG__gte = forms.DecimalField(required=False,
        label='Avg branch weight ratio dry/fresh From')
    DF_Branch_AVG__lte = forms.DecimalField(required=False,
        label='Avg branch weight ratio dry/fresh To')

    DF_Foliage_AVG__gte = forms.DecimalField(required=False,
        label='Avg foliage weight ratio dry/fresh From')
    DF_Foliage_AVG__lte = forms.DecimalField(required=False,
        label='Avg foliage weight ratio dry/fresh To')

    DF_Stump_AVG__gte = forms.DecimalField(required=False,
        label='Avg stump weight ratio dry/fresh From')
    DF_Stump_AVG__lte = forms.DecimalField(required=False,
        label='Avg stump weight ratio dry/fresh To')

    DF_Buttress_AVG__gte = forms.DecimalField(required=False,
        label='Avg buttress weight ratio dry/fresh From')
    DF_Buttress_AVG__lte = forms.DecimalField(required=False,
        label='Avg buttress weight ratio dry/fresh To')

    DF_Roots_AVG__gte = forms.DecimalField(required=False,
        label='Avg roots weight ratio dry/fresh From')
    DF_Roots_AVG__lte = forms.DecimalField(required=False,
        label='Avg roots weight ratio dry/fresh To')

    D_Bole_kg__gte = forms.DecimalField(required=False,
        label='Dry bole weight in kg From')
    D_Bole_kg__lte = forms.DecimalField(required=False,
        label='Dry bole weight in kg To')

    D_Branch_kg__gte = forms.DecimalField(required=False,
        label='Dry branches weight in kg From')
    D_Branch_kg__lte = forms.DecimalField(required=False,
        label='Dry branches weight in kg To')

    D_Foliage_kg__gte = forms.DecimalField(required=False,
        label='Dry foliage weight in kg From')
    D_Foliage_kg__lte = forms.DecimalField(required=False,
        label='Dry foliage weight in kg To')

    D_Stump_kg__gte = forms.DecimalField(required=False,
        label='Dry stump weight in kg From')
    D_Stump_kg__lte = forms.DecimalField(required=False,
        label='Dry stump weight in kg To')

    D_Buttress_kg__gte = forms.DecimalField(required=False,
        label='Dry buttress weight in kg From')
    D_Buttress_kg__lte = forms.DecimalField(required=False,
        label='Dry buttress weight in kg To')

    D_Roots_kg__gte = forms.DecimalField(required=False,
        label='Dry roots weight in kg From')
    D_Roots_kg__lte = forms.DecimalField(required=False,
        label='Dry roots weight in kg To')

    ABG_kg__gte = forms.DecimalField(required=False,
        label='Total above ground biomass in kg From')
    ABG_kg__lte = forms.DecimalField(required=False,
        label='Total above ground biomass  in kg To')

    BGB_kg__gte = forms.DecimalField(required=False,
        label='Total below ground biomass in kg From')
    BGB_kg__lte = forms.DecimalField(required=False,
        label='Total below ground biomass in kg To')

    Tot_Biomass_kg__gte = forms.DecimalField(required=False,
        label='Total tree biomass in kg From')
    Tot_Biomass_kg__lte = forms.DecimalField(required=False,
        label='Total tree biomass in kg To')

    BEF__gte = forms.DecimalField(required=False,
        label='Biomass expansion factor From')
    BEF__lte = forms.DecimalField(required=False,
        label='Biomass expansion factor To')
