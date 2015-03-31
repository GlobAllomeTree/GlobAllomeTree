from django.contrib import admin
from django.shortcuts import render_to_response
from django.template import RequestContext

admin.site.disable_action('delete_selected')

from apps.allometric_equations.models import (
    AllometricEquation, Population, TreeType
)

class PopulationAdmin(admin.ModelAdmin):
    list_display = ('Name', )


class TreeTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', )


class AllometricEquationAdmin(admin.ModelAdmin):
    raw_id_fields = ('Species_group','Location_group','Reference')
    list_display = ("Allometric_equation_ID", 'Equation', 'Modified')
    ordering = ("Allometric_equation_ID",)
    search_fields  = ("Allometric_equation_ID",)
    
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
        ('Reference', {'fields': ['Reference']}),
        ('Dataset', {'fields': ['Dataset']}),
    ]


admin.site.register(AllometricEquation, AllometricEquationAdmin)
admin.site.register(TreeType, TreeTypeAdmin)
admin.site.register(Population, PopulationAdmin)

