from django.contrib import admin
from globallometree.apps.common.models import Institution, Reference, Operator

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('Name', )

class OperatorAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Institution')


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('Label', 'Author', 'Year')

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Reference, ReferenceAdmin)
admin.site.register(Operator, OperatorAdmin)
