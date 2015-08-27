from django.contrib import admin
from globallometree.apps.biomass_expansion_factors.models import BiomassExpansionFactor


class BiomassExpansionFactorAdmin(admin.ModelAdmin):
    raw_id_fields = ('Species_group', 'Location_group', 'Reference')
    list_display = ('Biomass_expansion_factor_ID', 'Modified')
    ordering = ("Biomass_expansion_factor_ID",)
    search_fields  = ('Biomass_expansion_factor_ID',)

admin.site.register(BiomassExpansionFactor, BiomassExpansionFactorAdmin)
