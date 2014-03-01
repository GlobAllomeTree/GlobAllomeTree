from django.contrib import admin
from globallometree.apps.locations.models import Continent, Country, Location, LocationGroup

class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter  = ('name', )


class CountryAdmin(admin.ModelAdmin):
    list_display = ('common_name', 'capital', 'continent')
    list_filter  = ('continent', )


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter  = ('country', 'biome_fao', 'biome_udvardy', 'biome_wwf', 'biome_bailey', 'biome_holdridge', 'group')

class LocationGroupAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter  = ('name', )


admin.site.register(Continent, ContinentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(LocationGroup, LocationGroupAdmin)
