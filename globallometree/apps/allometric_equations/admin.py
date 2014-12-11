from django.contrib import admin
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.allometric_equations.models import (
    AllometricEquation, Population, TreeType
)


class PopulationAdmin(admin.ModelAdmin):
    list_display = ('Name', )


class TreeTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', )


# class AllometricEquationSubmissionAdmin(admin.ModelAdmin):
#     list_display = ('User', 'Submitted_file', 'Submitted_notes', 'Date_uploaded', 'Imported')
#     list_filter = ['User', 'Imported']
#     read_only = ('Date_uploaded',)
#     actions = ['Run_import']

#     def run_import(self, request, queryset):

#         #Make sure that there are some selected rows 
#         n = queryset.count()
#         if not n:
#             self.message_user(request, "Please select a file to import")
#             return None

#         #Make sure multiple objects were not selected
#         if n > 1:
#             self.message_user(
#                 request, "Please select only ONE file to import at a time"
#             )
#             return None

#         #Now that we have one row, we get the data submission from the query set
#         data_submission = queryset[0]

#         run_verified = request.POST.get('run', False)
#         import_good_rows_anyway = request.POST.get(
#             'import_good_rows_anyway', False
#         )

#         context = data_submission.import_data(
#             run_verified, import_good_rows_anyway
#         )
#         context['action_checkbox_name'] =  admin.helpers.ACTION_CHECKBOX_NAME
#         context['data_submission'] = data_submission
#         context['queryset'] = queryset

#         return render_to_response(
#             'allometric_equations/template.admin.run_import_confirm.html',
#             context, context_instance=RequestContext(request)
#         )


class AllometricEquationAdmin(admin.ModelAdmin):
    raw_id_fields = ('Species_group','Location_group','Reference')
    list_display = ("Allometric_equation_ID", 'Equation', 'Modified')
    ordering = ("Allometric_equation_ID",)
    search_fields  = ("Allometric_equation_ID",)
    
    fieldsets = [
        ('Identification',   {'fields': [
          'Population', 'TreeType',
        ]}),
        ('Taxonomy', {'fields': ['Species_group']}),
        ('Location', {'fields': ['Location_group'], 'classes': ['collapse']}),
        ('Components', {'fields': [
            'B', 'Bd', 'Bg', 'Bt', 'L', 'Rb', 'Rf', 'Rm', 'S', 'T',
            'F','Veg_Component'
        ], 'classes': ['collapse']}),
        ('Input/Output', {'fields': [
            'X', 'Unit_X', 'Z', 'Unit_Z', 'W', 'Unit_W', 'U', 'Unit_U', 'V',
            'Unit_V', 'Min_X', 'Max_X', 'Min_Z', 'Max_Z', 'Output', 'Output_TR',
            'Unit_Y', 'Sample_size', 'R2', 'R2_Adjusted', 'RMSE', 'SEE',
            'Top_dob', 'Stump_height', 'Corrected_for_bias', 'Bias_correction'
        ], 'classes': ['collapse']}),
        ('Allometry', {'fields': [
            'Age', 'Equation','Ratio_equation', 'Segmented_equation'
        ], 'classes': ['collapse']}),
        ('Reference', {'fields': ['Reference'], 'classes': ['collapse']}),
    ]


admin.site.register(AllometricEquation, AllometricEquationAdmin)
admin.site.register(TreeType, TreeTypeAdmin)
admin.site.register(Population, PopulationAdmin)

