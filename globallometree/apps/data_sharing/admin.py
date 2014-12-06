from django.contrib import admin

from . import models

class DataSetAdmin(admin.ModelAdmin):
    list_display = ('Title',  'User', 'Data_type',  'Is_restricted',)
    search_fields  = ['Title', 'Description']
    raw_id_fields = ('User',)
       
class DataSharingAgreementAdmin(admin.ModelAdmin):
    list_display = ('User', 'Permitted_use', 'Expires')
    search_fields  = ['Title',]
    raw_id_fields = ('User',)

admin.site.register(models.DataSet, DataSetAdmin)
admin.site.register(models.DataSharingAgreement, DataSharingAgreementAdmin)