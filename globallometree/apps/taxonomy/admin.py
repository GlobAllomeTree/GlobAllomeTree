from django.contrib import admin
from globallometree.apps.taxonomy.models import (
    Family, 
    Genus, 
    Species, 
    SpeciesDefinition,
    SpeciesGroup,
    SpeciesLocalName, 
    Subspecies
    )


class FamilyAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Modified')
    search_fields  = ('Name',)


class GenusAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Family',  'Modified')
    search_fields  = ('Name','Family__Name', )
    read_only_fields = ('Created', 'Modified')


class SpeciesLocalNameInline(admin.TabularInline):
    model = SpeciesLocalName


# class SpeciesLocalNameAdmin(admin.ModelAdmin):
#     raw_id_fields = ('Species',)
#     list_display = ('Local_name_latin', 'Species', 'Local_name', 'Language_iso_639_3')
#     search_fields  = ('Local_name', 'Local_name_latin', 'Language_iso_639_3')    



class SubspeciesAdmin(admin.ModelAdmin):
    raw_id_fields = ('Species',)
    list_display = ('Name', 'Species', 'Modified')
    search_fields  = ('Name','Species__Genus__Family__Name', 'Species__Genus__Name', 'Species__Name' )
    read_only_fields = ('created', 'modified')


class SpeciesAdmin(admin.ModelAdmin):
    raw_id_fields = ('Genus',)
    list_display = ('Name', 'Genus', 'Modified')
    search_fields  = ('Name','Genus__Family__Name', 'Genus__Name', )
    read_only_fields = ('Created', 'Modified')
    inlines = (SpeciesLocalNameInline,)


class SpeciesDefinitionInline(admin.TabularInline):
    model = SpeciesGroup.Species_definitions.through
    raw_id_fields = ('speciesdefinition',)

class SpeciesDefinitionAdmin(admin.ModelAdmin):
    read_only_fields = ('Created', 'Modified')
    raw_id_fields = ('Family', 'Genus', 'Species', 'Subspecies')
    list_display = ('__unicode__', 'Family', 'Genus', 'Species', 'Subspecies')

class SpeciesGroupAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Modified')
    search_fields  = ('Name', )
    read_only_fields = ('Created', 'Modified')
    fields = ('Name', )
    inlines = [
        SpeciesDefinitionInline,
    ]
    exclude = ('Species_definitions',)


admin.site.register(Family, FamilyAdmin)
admin.site.register(Genus, GenusAdmin)
admin.site.register(Species, SpeciesAdmin)
admin.site.register(Subspecies, SubspeciesAdmin)
admin.site.register(SpeciesGroup, SpeciesGroupAdmin)
admin.site.register(SpeciesDefinition, SpeciesDefinitionAdmin)
