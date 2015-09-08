from django.contrib import admin
from globallometree.apps.raw_data.models import RawData

from globallometree.apps.base.admin_helpers import ImproveRawIdFieldsForm


class RawDataAdmin(ImproveRawIdFieldsForm):
    raw_id_fields = ('Species_group', 'Location_group', 'Reference')
    list_display = ('ID_RD', 'Modified')
    ordering = ("ID_RD",)
    search_fields  = ('ID_RD',)
    exclude = ('Elasticsearch_doc_hash',)


admin.site.register(RawData, RawDataAdmin)
