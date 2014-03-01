from django.contrib import admin
from globallometree.apps.common.models import Institution, DataReference

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', )


class DataReferenceAdmin(admin.ModelAdmin):
    list_display = ('label', 'author', 'year')

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(DataReference, DataReferenceAdmin)
