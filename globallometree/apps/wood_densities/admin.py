from django.contrib import admin
from globallometree.apps.wood_densities.models import WoodDensity


class WoodDensityAdmin(admin.ModelAdmin):
    raw_id_fields = ('Species_group', 'Location_group', 'Reference')
    list_display = ('ID', 'Modified')
    ordering = ("ID",)
    search_fields  = ('ID',)


admin.site.register(WoodDensity, WoodDensityAdmin)
