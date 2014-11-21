from django.contrib import admin
from globallometree.apps.common.models import Institution, DataReference, Operator

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', )

class OperatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution')


class DataReferenceAdmin(admin.ModelAdmin):
    list_display = ('label', 'author', 'year')

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(DataReference, DataReferenceAdmin)
admin.site.register(Operator, OperatorAdmin)
