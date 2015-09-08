from django.contrib import admin
from globallometree.apps.locations.models import (
    Continent, Country, Location, LocationGroup,
    ZoneFAO, EcoregionUdvardy, EcoregionWWF, DivisionBailey, 
    ZoneHoldridge, VegetationType, BiomeLocal)

from django.utils.safestring import mark_safe

class ContinentAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Code')


class CountryAdmin(admin.ModelAdmin):
    list_display = ('Formal_name', 'Common_name', 'Common_name_fr', 'Iso3166a2', 'Continent', 'Centroid_longitude', 'Centroid_latitude')
    list_filter  = ('Continent', )
    search_fields = ('Formal_name', 'Common_name', 'Common_name_fr', 'Formal_name_fr','Iso3166a2',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('ID_Location', 'Name', 'Region', 'Country', 'Latitude', 'Longitude', 'Zone_FAO','Modified')
    list_filter  = ('Country',)
    search_fields = ('Name', 'Region')


class LocationInline(admin.TabularInline):
    model = LocationGroup.Locations.through
    raw_id_fields = ('location',)
    readonly_fields = ('admin_link',)

    def admin_link(self, instance):
        if instance.pk:
            return mark_safe(u'<a href="/admin/locations/location/%s/">Edit Location</a>' % instance.location.pk)
        else:
            return ''


class VegetationTypeAdmin(admin.ModelAdmin):
    list_display = ('Name',)


class LocationGroupAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Dataset', 'Dataset_ID_Location_group', 'Modified')
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
admin.site.register(VegetationType, VegetationTypeAdmin)
