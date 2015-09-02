from django.contrib import admin
from globallometree.apps.source.models import Institution, Reference, Operator

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('Name', )

class OperatorAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Institution')


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('Reference', 'Author', 'Year')

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Reference, ReferenceAdmin)
admin.site.register(Operator, OperatorAdmin)
