from django.contrib import admin
from globallometree.apps.biomass_expansion_factors.models import BiomassExpansionFactor

from globallometree.apps.search_helpers.admin_helpers import ImproveRawIdFieldsForm


class BiomassExpansionFactorAdmin(ImproveRawIdFieldsForm):
    raw_id_fields = ('Species_group', 'Location_group', 'Reference')
    list_display = ('ID_BEF', 'Modified')
    ordering = ("ID_BEF",)
    search_fields  = ('ID_BEF',)
    exclude = ('Elasticsearch_doc_hash',)

admin.site.register(BiomassExpansionFactor, BiomassExpansionFactorAdmin)
