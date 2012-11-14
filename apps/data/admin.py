from django.contrib import admin
from . import models

admin.site.register(models.Country)


class TreeEquationAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Population', 'Ecosystem', 'Country', 'Species', 'Genus',  'Equation')
    ordering = ["ID"]
    search_fields  = ['ID','Country']
    list_filter = ['Country']

admin.site.register(models.TreeEquation, TreeEquationAdmin)
