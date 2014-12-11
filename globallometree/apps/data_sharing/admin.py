from django.contrib import admin

from . import models

class DatasetAdmin(admin.ModelAdmin):
    list_display = ('Title',  'User', 'Data_type',  'Is_restricted',)
    search_fields  = ['Title', 'Description']
    raw_id_fields = ('User',)
       
class DataLicenseAdmin(admin.ModelAdmin):
    list_display = ('Title', 'User', 'Permitted_use', 'Expires')
    search_fields  = ['Title',]
    raw_id_fields = ('User',)

admin.site.register(models.Dataset, DatasetAdmin)
admin.site.register(models.DataLicense, DataLicenseAdmin)
