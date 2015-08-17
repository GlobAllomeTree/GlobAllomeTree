from django.contrib import admin
from apps.raw_data.models import RawData

class RawDataAdmin(admin.ModelAdmin):
    raw_id_fields = ('Species_group', 'Location_group', 'Reference')
    list_display = ('Raw_data_ID', 'Modified')
    ordering = ("Raw_data_ID",)
    search_fields  = ('Raw_data_ID',)

admin.site.register(RawData, RawDataAdmin)
