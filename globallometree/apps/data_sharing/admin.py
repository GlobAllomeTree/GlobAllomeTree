from django.contrib import admin

from . import models

class DataSetAdmin(admin.ModelAdmin):
    list_display = ('title',  'user', 'data_type',  'is_restricted',)
    search_fields  = ['title', 'description']
    raw_id_fields = ('user',)
       
class DataSharingAgreementAdmin(admin.ModelAdmin):
    list_display = ('user', 'permitted_use', 'expires')
    search_fields  = ['title',]
    raw_id_fields = ('user',)

admin.site.register(models.DataSet, DataSetAdmin)
admin.site.register(models.DataSharingAgreement, DataSharingAgreementAdmin)