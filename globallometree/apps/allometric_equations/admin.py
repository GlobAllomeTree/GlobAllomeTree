from django.contrib import admin
from django.shortcuts import render_to_response
from django.template import RequestContext


from globallometree.apps.allometric_equations.models import (
    AllometricEquation, Population
)

from globallometree.apps.base.admin_helpers import ImproveRawIdFieldsForm

class PopulationAdmin(admin.ModelAdmin):
    list_display = ('Name', )


class AllometricEquationAdmin(ImproveRawIdFieldsForm):
    raw_id_fields = ('Species_group','Location_group','Source')
    list_display = ("ID_AE", 'Equation', 'Modified')
    ordering = ("ID_AE",)
    search_fields  = ("ID_AE",)
    
    fieldsets = [
        ('Identification',   {'fields': [
          'Population', 'Tree_type',
        ]}),
        ('Taxonomy', {'fields': ['Species_group']}),
        ('Location', {'fields': ['Location_group']}),
        ('Components', {'fields': [
            'B', 'Bd', 'Bg', 'Bt', 'L', 'Rb', 'Rf', 'Rm', 'S', 'T',
            'F','Veg_Component'
        ]}),
        ('Input/Output', {'fields': [
            'X', 'Unit_X', 'Z', 'Unit_Z', 'W', 'Unit_W', 'U', 'Unit_U', 'V',
            'Unit_V', 'Min_X', 'Max_X', 'Min_Z', 'Max_Z', 'Output', 'Output_TR',
            'Unit_Y', 'Sample_size', 'R2', 'R2_Adjusted', 'RMSE', 'SEE',
            'Top_dob', 'Stump_height', 'Corrected_for_bias', 'Bias_correction'
        ]}),
        ('Allometry', {'fields': [
            'Age', 'Equation','Substitute_equation', 'Ratio_equation', 'Segmented_equation'
        ]}),
        ('Reference', {'fields': ['Source']}),
        ('Dataset', {'fields': ['Dataset']}),
    ]


admin.site.register(AllometricEquation, AllometricEquationAdmin)
admin.site.register(Population, PopulationAdmin)
