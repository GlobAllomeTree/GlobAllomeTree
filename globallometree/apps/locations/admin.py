from django.contrib import admin
from globallometree.apps.locations.models import Continent, Country, Location, LocationGroup
from globallometree.apps.locations.models import BiomeFAO, BiomeUdvardy, BiomeWWF, DivisionBailey, BiomeHoldridge

class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name', )


class CountryAdmin(admin.ModelAdmin):
    list_display = ('common_name', 'capital', 'continent')
    list_filter  = ('continent', )


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'biome_fao', 'country', 'modified')
    list_filter  = ('biome_fao','country')


class BiomeFAOAdmin(admin.ModelAdmin):
    list_display = ('name', )

class BiomeUdvardyAdmin(admin.ModelAdmin):
    list_display = ('name', )

class BiomeWWFAdmin(admin.ModelAdmin):
    list_display = ('name', )

class DivisionBaileyAdmin(admin.ModelAdmin):
    list_display = ('name', )

class BiomeHoldridgeAdmin(admin.ModelAdmin):
    list_display = ('name', )    


admin.site.register(Continent, ContinentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(BiomeFAO, BiomeFAOAdmin)
admin.site.register(BiomeUdvardy, BiomeUdvardyAdmin)
admin.site.register(BiomeWWF, BiomeWWFAdmin)
admin.site.register(DivisionBailey, DivisionBaileyAdmin)
admin.site.register(BiomeHoldridge, BiomeHoldridgeAdmin)
