from django.db import models
from globallometree.apps.common.models import TimeStampedModel

class Continent(TimeStampedModel):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Country(TimeStampedModel):
    common_name = models.CharField(max_length=159, blank=True)
    formal_name = models.CharField(max_length=159, blank=True)
    common_name_fr = models.CharField(max_length=159, blank=True)
    formal_name_fr = models.CharField(max_length=159, blank=True)
    iso3166a2 = models.CharField(max_length=6, blank=True)
    iso3166a3 = models.CharField(max_length=9,blank=True)
    iso3166n3 = models.IntegerField(null=True, blank=True)
    continent = models.ForeignKey(Continent, blank=True, null=True)
    centroid_latitude = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=5)
    centroid_longitude = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=5)

    def __unicode__(self):
        return u'%s (%s)' % (self.common_name, self.iso3166a2)

    class Meta:
        verbose_name ='Country'
        verbose_name_plural = 'Countries'
        ordering = ('common_name',)


class BiomeFAO(TimeStampedModel):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Biome FAO'
        verbose_name_plural = 'Biome FAO List'
        ordering = ('name',)


class BiomeUdvardy(TimeStampedModel):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Biome Udvardy'
        verbose_name_plural = 'Biome Udvardy List'
        ordering = ('name',)


class BiomeWWF(TimeStampedModel):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Biome WWF'
        verbose_name_plural = 'Biome WWF List'
        ordering = ('name',)


class DivisionBailey(TimeStampedModel):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Division Bailey'
        verbose_name_plural = 'Division Bailey List'
        ordering = ('name',)


class BiomeHoldridge(TimeStampedModel):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Biome Holdridge'
        verbose_name_plural = 'Biome Holdridge List'
        ordering = ('name',)


class LocationGroup(TimeStampedModel):    
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Group Name")
    locations = models.ManyToManyField('locations.Location', verbose_name="List of Locations", blank=True, null=True)
    original_Group_Location = models.IntegerField(null=True, blank=True, help_text="The original Group_Location from the global import")

    def locations_string(self):
        string = ''
        for location in self.locations.all():
            if string != '': string += ', '
            string += location.name
        return string

    def lat_lon_string(self):
        return ', '.join([u'[%s, %s]'%(co['lat'], co['lon']) for co in self.get_precise_coordinates()])

    def get_precise_coordinates(self):
        locations = []
        for location in self.locations.all():
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
            location.country for location in
                self.locations.all() if location.country is not None
        ]))

    def countries_string(self):
        string = ''
        for country in self.countries():
            if string != '': string += ', '
            string += country.common_name
        return string

    def continents(self):
        return list(set([
            country.continent for country in
                self.countries() if country.continent is not None
        ]))

    def continents_string(self):
        string = ''
        for continent in self.continents():
            if string != '': string += ', '
            string += continent.name
        return string

    def biomes_fao(self):
        return list(set([
            location.biome_fao for location in
                self.locations.all() if location.biome_fao is not None
        ]))

    def biomes_fao_string(self):
        string = ''
        for biome_fao in self.biomes_fao():
            if string != '': string += ', '
            string += biome_fao.name
        return string

    def biomes_udvardy(self):
        return list(set([
            location.biome_udvardy for location in
                self.locations.all() if location.biome_udvardy is not None
        ]))

    def biomes_udvardy_string(self):
        string = ''
        for biome_udvardy in self.biomes_udvardy():
            if string != '': string += ', '
            string += biome_udvardy.name
        return string

    def biomes_wwf(self):
        return list(set([
            location.biome_wwf for location in
                self.locations.all() if location.biome_wwf is not None
        ]))

    def biomes_wwf_string(self):
        string = ''
        for biome_wwf in self.biomes_wwf():
            if string != '': string += ', '
            string += biome_wwf.name
        return string

    def divisions_bailey(self):
        return list(set([
            location.division_bailey for location in
                self.locations.all() if location.division_bailey is not None
        ]))

    def divisions_bailey_string(self):
        string = ''
        for division_bailey in self.divisions_bailey():
            if string != '': string += ', '
            string += division_bailey.name
        return string

    def biomes_holdridge(self):
        return list(set([
            location.biome_holdridge for location in
                self.locations.all() if location.biome_holdridge is not None
        ]))

    def biomes_holdridge_string(self):
        string = ''
        for biome_holdridge in self.biomes_holdridge():
            if string != '': string += ', '
            string += biome_holdridge.name
        return string

    def __unicode__(self):
        return self.name


class Location(TimeStampedModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    Latitude = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=9
    )
    Longitude = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=9
    )
    commune = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    biome_fao = models.ForeignKey(BiomeFAO, blank=True, null=True)
    biome_udvardy = models.ForeignKey(BiomeUdvardy, blank=True, null=True)
    biome_wwf = models.ForeignKey(BiomeWWF, blank=True, null=True)
    division_bailey = models.ForeignKey(DivisionBailey, blank=True, null=True)
    biome_holdridge = models.ForeignKey(BiomeHoldridge, blank=True, null=True)
    original_ID_Location = models.IntegerField(null=True, blank=True, help_text="The original ID_Location from the global import")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)

