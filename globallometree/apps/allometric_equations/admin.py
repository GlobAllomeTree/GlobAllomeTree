from django.contrib import admin
from django.shortcuts import render_to_response
from django.template import RequestContext

from globallometree.apps.allometric_equations.models import (
    AllometricEquation, Population, Ecosystem, Submission
)

class PopulationAdmin(admin.ModelAdmin):
    list_display = ('name', )


class EcosystemAdmin(admin.ModelAdmin):
    list_display = ('name', )


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'submitted_file', 'submitted_notes', 'imported')
    list_filter = ['user', 'imported']
    actions = ['run_import']

    def run_import(self, request, queryset):

        #Make sure that there are some selected rows 
        n = queryset.count()
        if not n:
            self.message_user(request, "Please select a file to import")
            return None

        #Make sure multiple objects were not selected
        if n > 1:
            self.message_user(
                request, "Please select only ONE file to import at a time"
            )
            return None

        #Now that we have one row, we get the data submission from the query set
        data_submission = queryset[0]

        run_verified = request.POST.get('run', False)
        import_good_rows_anyway = request.POST.get(
            'import_good_rows_anyway', False
        )

        context = data_submission.import_data(
            run_verified, import_good_rows_anyway
        )
        context['action_checkbox_name'] =  admin.helpers.ACTION_CHECKBOX_NAME
        context['data_submission'] = data_submission
        context['queryset'] = queryset

        return render_to_response(
            'allometric_equations/template.admin.run_import_confirm.html',
            context, context_instance=RequestContext(request)
        )


class AllometricEquationAdmin(admin.ModelAdmin):
    raw_id_fields = ('species_group','location_group','reference')
    list_display = ('ID', 'Equation','data_submission', 'modified')
    ordering = ("ID",)
    search_fields  = ('ID',)
    list_filter = ('data_submission',)


admin.site.register(Population, PopulationAdmin)
admin.site.register(Ecosystem, EcosystemAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(AllometricEquation, AllometricEquationAdmin)
