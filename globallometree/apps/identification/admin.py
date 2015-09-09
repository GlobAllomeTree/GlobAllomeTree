
from django.contrib import admin

from globallometree.apps.identification.models import TreeType, VegetationType

class TreeTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', )

    
class VegetationTypeAdmin(admin.ModelAdmin):
    list_display = ('Name',)


admin.site.register(TreeType, TreeTypeAdmin)
admin.site.register(VegetationType, VegetationTypeAdmin)
