from django.contrib import admin
from globallometree.apps.allometric_equations.models import AllometricEquation, AllometricEquationPopulation, AllometricEquationEcosystem, AllometricEquationSubmission

class AllometricEquationPopulationAdmin(admin.ModelAdmin):
    list_display = ('name', )


class AllometricEquationEcosystemAdmin(admin.ModelAdmin):
    list_display = ('name', )


class AllometricEquationSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'submitted_file', 'submitted_notes', 'imported')
    list_filter = ['user', 'imported']


class AllometricEquationAdmin(admin.ModelAdmin):
	raw_id_fields = ('species_group','location_group')
    list_display = ('ID', 'Equation','data_submission', 'modified')
    ordering = ("ID",)
    search_fields  = ('ID',)
    list_filter = ('data_submission',)


admin.site.register(AllometricEquationPopulation, AllometricEquationPopulationAdmin)
admin.site.register(AllometricEquationEcosystem, AllometricEquationEcosystemAdmin)
admin.site.register(AllometricEquationSubmission, AllometricEquationSubmissionAdmin)
admin.site.register(AllometricEquation, AllometricEquationAdmin)
