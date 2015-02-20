from django.contrib import admin
from django.contrib import messages

from . import models

class DatasetAdmin(admin.ModelAdmin):
    actions = ['run_import']
    list_display = ('Title',  'Imported', 'User', 'Data_type',  'Data_license',)
    search_fields  = ['Title', 'Description']
    raw_id_fields = ('User',)
    readonly_fields = ('Imported',)

    def run_import(self, request, queryset):
        # import pdb; pdb.set_trace()
        # self.message_user(request, "Hello!")
        messages.error(request,'Error message')
        #Make sure that there are some selected rows 
        n = queryset.count()
        if not n:
            self.message_user(request, "Please select a file to import")
            return None
  
        #Make sure multiple objects were not selected
        if n > 1:

            self.message_user(request, "Please select only ONE file to import at a time")
            return None

        #Now that we have one row, we get the data submission from the query set
        dataset = queryset[0]

        if dataset.Imported:
            self.message_user(request, "That dataset selected has already been imported")
            return None






class DataLicenseAdmin(admin.ModelAdmin):
    list_display = ('Title', 'User', 'Public_choice',)
    search_fields  = ['Title',]
    raw_id_fields = ('User',)

admin.site.register(models.Dataset, DatasetAdmin)
admin.site.register(models.DataLicense, DataLicenseAdmin)
