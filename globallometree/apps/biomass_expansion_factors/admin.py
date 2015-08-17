from django.contrib import admin
from apps.biomass_expansion_factors.models import BiomassExpansionFactor


class BiomassExpansionFactorAdmin(admin.ModelAdmin):
    raw_id_fields = ('Species_group', 'Location_group', 'Reference')
    list_display = ('ID_BEF', 'Modified')
    ordering = ("ID_BEF",)
    search_fields  = ('ID_BEF',)

admin.site.register(BiomassExpansionFactor, BiomassExpansionFactorAdmin)
