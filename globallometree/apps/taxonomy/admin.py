from django.contrib import admin
from globallometree.apps.taxonomy.models import Family, Genus, Species, SpeciesGroup


class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'modified')
    search_fields  = ('name',)


class GenusAdmin(admin.ModelAdmin):
    raw_id_fields = ('family',)
    list_display = ('name', 'family',  'modified')
    search_fields  = ('name','family__name', )
    read_only_fields = ('created', 'modified')


class SpeciesAdmin(admin.ModelAdmin):
    raw_id_fields = ('genus',)
    list_display = ('name', 'genus', 'modified')
    search_fields  = ('name','genus__family__name', 'genus__name', )
    read_only_fields = ('created', 'modified')


class SpeciesInline(admin.TabularInline):
    #Bit of a hack to use the autogenerated through model, but it avoides the horrible multiselect
    model = SpeciesGroup.species.through
    raw_id_fields = ('species',)


class SpeciesGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'original_ID_Group', 'modified')
    search_fields  = ('name','original_ID_Group', )
    read_only_fields = ('created', 'modified')
    inlines = [
        SpeciesInline,
    ]
    exclude = ('species',)


admin.site.register(Family, FamilyAdmin)
admin.site.register(Genus, GenusAdmin)
admin.site.register(Species, SpeciesAdmin)
admin.site.register(SpeciesGroup, SpeciesGroupAdmin)