from django.contrib import admin
from globallometree.apps.raw_data.models import RawData

class RawDataAdmin(admin.ModelAdmin):
    raw_id_fields = ('Species_group', 'Location_group', 'Reference')
    list_display = ('ID', 'Modified')
    ordering = ("ID",)
    search_fields  = ('ID',)

admin.site.register(RawData, RawDataAdmin)
