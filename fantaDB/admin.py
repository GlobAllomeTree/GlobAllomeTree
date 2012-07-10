from django.contrib import admin
from fantaDB.models import fantaDB

class fantaDBAdmin(admin.ModelAdmin):
    list_display = ('id', 'population', 'ecosystem', 'country', 'species', 'genus',  'equation_y')
    ordering = ["id"]
    search_fields  = ['id','country']
    list_filter = ['country']

admin.site.register(fantaDB,fantaDBAdmin)

