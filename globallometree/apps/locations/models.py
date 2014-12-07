from django.db import models
from globallometree.apps.common.models import BaseModel

class Continent(BaseModel):
    Code = models.CharField(max_length=2)
    Name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.Name


class Country(BaseModel):
    Common_name = models.CharField(max_length=159, blank=True)
    Formal_name = models.CharField(max_length=159, blank=True)
    Common_name_fr = models.CharField(max_length=159, blank=True)
    Formal_name_fr = models.CharField(max_length=159, blank=True)
    Iso3166a2 = models.CharField(max_length=6, blank=True)
    Iso3166a3 = models.CharField(max_length=9,blank=True)
    Iso3166n3 = models.IntegerField(null=True, blank=True)
    Continent = models.ForeignKey(Continent, blank=True, null=True)
    Centroid_latitude = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=5)
    Centroid_longitude = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=5)

    def __unicode__(self):
        return u'%s (%s)' % (self.Common_name, self.Iso3166a2)

    class Meta:
        verbose_name ='Country'
        verbose_name_plural = 'Countries'
        ordering = ('Common_name',)


class BiomeFAO(BaseModel):
    Name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Biome FAO'
        verbose_name_plural = 'Biome FAO List'
        ordering = ('Name',)


class BiomeUdvardy(BaseModel):
    Name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Biome Udvardy'
        verbose_name_plural = 'Biome Udvardy List'
        ordering = ('Name',)


class BiomeWWF(BaseModel):
    Name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Biome WWF'
        verbose_name_plural = 'Biome WWF List'
        ordering = ('Name',)


class DivisionBailey(BaseModel):
    Name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Division Bailey'
        verbose_name_plural = 'Division Bailey List'
        ordering = ('Name',)


class BiomeHoldridge(BaseModel):
    Name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Biome Holdridge'
        verbose_name_plural = 'Biome Holdridge List'
        ordering = ('Name',)


class GeoPoint(BaseModel):
    Latitude = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=9
    )
    Longitude = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=9
    )


class Location(BaseModel):
    Name = models.CharField(max_length=255, null=True, blank=True)
    Commune = models.CharField(max_length=255, blank=True, null=True)
    Province = models.CharField(max_length=255, blank=True, null=True)
    Region = models.CharField(max_length=255, blank=True, null=True)
    Country = models.ForeignKey(Country, blank=True, null=True)
    Original_ID_Location = models.IntegerField(null=True, blank=True, help_text="The original ID_Location from the global import")

    def __unicode__(self):
        return self.Name

    class Meta:
        ordering = ('Name',)


class LocationGroup(BaseModel):    
    Name = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name="Group Name")

    Original_group_location = models.IntegerField(null=True, blank=True, help_text="The original Group_Location from the global import")
    Biomes_FAO = models.ManyToManyField(BiomeFAO, blank=True, null=True)
    Biomes_UDVARDY = models.ManyToManyField(BiomeUdvardy, blank=True, null=True)
    Biomes_WWF = models.ManyToManyField(BiomeWWF, blank=True, null=True)
    Divisions_BAILEY = models.ManyToManyField(DivisionBailey, blank=True, null=True)
    Biomes_HOLDRIDGE = models.ManyToManyField(BiomeHoldridge, blank=True, null=True)
    Locations = models.ManyToManyField(Location, verbose_name="List of Locations", blank=True, null=True)
    Geo_points = models.ManyToManyField(GeoPoint, verbose_name="List of Geo Points", blank=True, null=True)

    def locations_string(self):
        string = ''
        for location in self.Locations.all():
            if string != '': string += ', '
            string += location.Name
        return string

    def lat_lon_string(self):
        return ', '.join([u'[%s, %s]'%(co['lat'], co['lon']) for co in self.get_precise_coordinates()])

    def get_precise_coordinates(self):
        locations = []
        for location in self.Locations.all():
            if not location.Latitude or not location.Longitude:
                #locations can just be countries or biomes
                #so in that case we just skip over the object
                continue
            #dicts do not work with unique sets
            if not any(l == {'lat' : location.Latitude,  'lon' : location.Longitude} for l in locations):
                locations.append({
                    "lat" : location.Latitude,
                    "lon" : location.Longitude
                })
        return locations

    def countries(self):
        return list(set([
            location.Country for location in
                self.Locations.all() if location.Country is not None
        ]))

    def countries_string(self):
        string = ''
        for country in self.countries():
            if string != '': string += ', '
            string += country.Common_name
        return string

    def continents(self):
        return list(set([
            country.Continent for country in
                self.countries() if country.Continent is not None
        ]))

    def continents_string(self):
        string = ''
        for continent in self.continents():
            if string != '': string += ', '
            string += continent.name
        return string

    def biomes_fao(self):
        return list(set([
            location.Biome_fao for location in
                self.Locations.all() if location.Biome_fao is not None
        ]))

    def biomes_fao_string(self):
        string = ''
        for biome_fao in self.biomes_fao():
            if string != '': string += ', '
            string += biome_fao.name
        return string

    def biomes_udvardy(self):
        return list(set([
            location.Biome_udvardy for location in
                self.Locations.all() if location.Biome_udvardy is not None
        ]))

    def biomes_udvardy_string(self):
        string = ''
        for biome_udvardy in self.biomes_udvardy():
            if string != '': string += ', '
            string += biome_udvardy.name
        return string

    def biomes_wwf(self):
        return list(set([
            location.Biome_wwf for location in
                self.Locations.all() if location.Biome_wwf is not None
        ]))

    def biomes_wwf_string(self):
        string = ''
        for biome_wwf in self.biomes_wwf():
            if string != '': string += ', '
            string += biome_wwf.name
        return string

    def divisions_bailey(self):
        return list(set([
            location.Division_bailey for location in
                self.Locations.all() if location.Division_bailey is not None
        ]))

    def divisions_bailey_string(self):
        string = ''
        for division_bailey in self.divisions_bailey():
            if string != '': string += ', '
            string += division_bailey.name
        return string

    def biomes_holdridge(self):
        return list(set([
            location.Biome_holdridge for location in
                self.Locations.all() if location.Biome_holdridge is not None
        ]))

    def biomes_holdridge_string(self):
        string = ''
        for biome_holdridge in self.biomes_holdridge():
            if string != '': string += ', '
            string += biome_holdridge.name
        return string

    def __unicode__(self):
        return self.Name


