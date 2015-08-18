from django.contrib import admin
from globallometree.apps.locations.models import (
    Continent, Country, Location, LocationGroup,
    ZoneFAO, EcoregionUdvardy, EcoregionWWF, DivisionBailey, 
    ZoneHoldridge, ForestType, BiomeLocal)

class ContinentAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Code')


class CountryAdmin(admin.ModelAdmin):
    list_display = ('Common_name', 'Common_name_fr', 'Iso3166a2', 'Continent', 'Centroid_longitude', 'Centroid_latitude')
    list_filter  = ('Continent', )


class LocationAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Country', 'Modified')
    list_filter  = ('Country',)
    search_fields = ('Name',)


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

class ZoneFAOAdmin(admin.ModelAdmin):
    list_display = ('Name', )


class EcoregionUdvardyAdmin(admin.ModelAdmin):
    list_display = ('Name', )


class EcoregionWWFAdmin(admin.ModelAdmin):
    list_display = ('Name', )


class DivisionBaileyAdmin(admin.ModelAdmin):
    list_display = ('Name', )


class ZoneHoldridgeAdmin(admin.ModelAdmin):
    list_display = ('Name', )    


class BiomeLocalAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Reference') 

admin.site.register(Continent, ContinentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(LocationGroup, LocationGroupAdmin)
admin.site.register(BiomeLocal, BiomeLocalAdmin)
admin.site.register(ZoneFAO, ZoneFAOAdmin)
admin.site.register(EcoregionUdvardy, EcoregionUdvardyAdmin)
admin.site.register(EcoregionWWF, EcoregionWWFAdmin)
admin.site.register(DivisionBailey, DivisionBaileyAdmin)
admin.site.register(ZoneHoldridge, ZoneHoldridgeAdmin)
admin.site.register(ForestType, ForestTypeAdmin)
