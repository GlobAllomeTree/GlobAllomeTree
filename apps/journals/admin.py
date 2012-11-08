from django.contrib import admin

from . import models

class JournalAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'site_url')
    search_fields  = ['title', 'description']
       
admin.site.register(models.Journal, JournalAdmin)