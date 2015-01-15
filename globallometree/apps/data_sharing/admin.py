from django.contrib import admin

from . import models

class DatasetAdmin(admin.ModelAdmin):
    list_display = ('Title',  'Imported', 'User', 'Data_type',  'Data_license',)
    search_fields  = ['Title', 'Description']
    raw_id_fields = ('User',)
    readonly_fields = ('Imported',)
       
class DataLicenseAdmin(admin.ModelAdmin):
    list_display = ('Title', 'User', 'Public_choice',)
    search_fields  = ['Title',]
    raw_id_fields = ('User',)

admin.site.register(models.Dataset, DatasetAdmin)
admin.site.register(models.DataLicense, DataLicenseAdmin)
