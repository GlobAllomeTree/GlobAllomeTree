from django.contrib import admin
from globallometree.apps.common.models import Institution, DataReference, Operator

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('Name', )

class OperatorAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Institution')


class DataReferenceAdmin(admin.ModelAdmin):
    list_display = ('Label', 'Author', 'Year')

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(DataReference, DataReferenceAdmin)
admin.site.register(Operator, OperatorAdmin)
