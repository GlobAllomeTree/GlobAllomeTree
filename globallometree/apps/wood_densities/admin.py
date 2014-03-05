from django.contrib import admin
from globallometree.apps.wood_densities.models import WoodDensity


class WoodDensityAdmin(admin.ModelAdmin):
    raw_id_fields = ('species_group','location_group')
    list_display = ('ID', 'modified')
    ordering = ("ID",)
    search_fields  = ('ID',)


admin.site.register(WoodDensity, WoodDensityAdmin)
