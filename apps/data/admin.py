from django.contrib import admin
from . import models

admin.site.register(models.Country)


class TreeEquationAdmin(admin.ModelAdmin):
    list_display = ('id', 'population', 'ecosystem', 'country', 'species', 'genus',  'equation_y')
    ordering = ["id"]
    search_fields  = ['id','country']
    list_filter = ['country']

admin.site.register(models.TreeEquation, TreeEquationAdmin)
