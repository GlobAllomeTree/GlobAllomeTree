from django.contrib import admin
from globallometree.apps.taxonomy.models import Family, Genus, Species, SpeciesGroup

class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter  = ('name', )


class GenusAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter  = ('family', )


class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter  = ('genus', )


class SpeciesGroupAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter  = ('name', )


admin.site.register(Family, FamilyAdmin)
admin.site.register(Genus, GenusAdmin)
admin.site.register(Species, SpeciesAdmin)
admin.site.register(SpeciesGroup, SpeciesGroupAdmin)
