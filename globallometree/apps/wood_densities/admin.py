from django.contrib import admin
from globallometree.apps.wood_densities.models import WoodDensity


class WoodDensityAdmin(admin.ModelAdmin):
    raw_id_fields = ('Species_group', 'Location_group', 'Source')
    list_display = ('ID_WD', 'Modified')
    ordering = ("ID_WD",)
    search_fields  = ('ID_WD',)
    exclude = ('Elasticsearch_doc_hash',)



admin.site.register(WoodDensity, WoodDensityAdmin)
