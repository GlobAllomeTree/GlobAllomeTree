from django.contrib import admin
from globallometree.apps.locations.models import (
    Continent, Country, Location, LocationGroup,
    BiomeFAO, BiomeUdvardy, BiomeWWF, DivisionBailey, BiomeHoldridge, ForestType)

class ContinentAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Code')


class CountryAdmin(admin.ModelAdmin):
    list_display = ('Common_name', 'Common_name_fr', 'Iso3166a2', 'Continent', 'Centroid_longitude', 'Centroid_latitude')
    list_filter  = ('Continent', )


class LocationAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Country', 'Modified')
    list_filter  = ('Country',)


class LocationInline(admin.TabularInline):
    model = LocationGroup.Locations.through
    raw_id_fields = ('location',)


class ForestTypeAdmin(admin.ModelAdmin):
    list_display = ('Name',)


class LocationGroupAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Dataset', 'Dataset_Location_group_ID', 'Modified')
    list_filter  = ('Dataset',)
    search_fields = ('Name',)
    exclude = ('Locations',)
    fields = ('Name', )
    inlines = [
    	 LocationInline
    	]

class BiomeFAOAdmin(admin.ModelAdmin):
    list_display = ('Name', )


class BiomeUdvardyAdmin(admin.ModelAdmin):
    list_display = ('Name', )


class BiomeWWFAdmin(admin.ModelAdmin):
    list_display = ('Name', )


class DivisionBaileyAdmin(admin.ModelAdmin):
    list_display = ('Name', )


class BiomeHoldridgeAdmin(admin.ModelAdmin):
    list_display = ('Name', )    


admin.site.register(Continent, ContinentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(LocationGroup, LocationGroupAdmin)
admin.site.register(BiomeFAO, BiomeFAOAdmin)
admin.site.register(BiomeUdvardy, BiomeUdvardyAdmin)
admin.site.register(BiomeWWF, BiomeWWFAdmin)
admin.site.register(DivisionBailey, DivisionBaileyAdmin)
admin.site.register(BiomeHoldridge, BiomeHoldridgeAdmin)
admin.site.register(ForestType, ForestTypeAdmin)
