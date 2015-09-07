from django.contrib import admin
from globallometree.apps.raw_data.models import RawData

from globallometree.apps.base.admin_helpers import ImproveRawIdFieldsForm


class RawDataAdmin(ImproveRawIdFieldsForm):
    raw_id_fields = ('Species_group', 'Location_group', 'Reference')
    list_display = ('Raw_data_ID', 'Modified')
    ordering = ("Raw_data_ID",)
    search_fields  = ('Raw_data_ID',)
    exclude = ('Elasticsearch_doc_hash',)


admin.site.register(RawData, RawDataAdmin)
