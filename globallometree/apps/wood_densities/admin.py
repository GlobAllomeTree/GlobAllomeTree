from django.contrib import admin
from globallometree.apps.wood_densities.models import WoodDensity


class WoodDensityAdmin(admin.ModelAdmin):
    raw_id_fields = ('Species_group', 'Location_group', 'Reference')
    list_display = ('Wood_density_ID', 'Modified')
    ordering = ("Wood_density_ID",)
    search_fields  = ('Wood_density_ID',)


admin.site.register(WoodDensity, WoodDensityAdmin)
