from django.db import models


class Continent(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Country(models.Model):
    common_name = models.CharField(max_length=159, blank=True)
    formal_name = models.CharField(max_length=159, blank=True)
    type = models.CharField(max_length=69, blank=True)
    sub_type = models.CharField(max_length=102, blank=True)
    sovereignty = models.CharField(max_length=72, blank=True)
    capital = models.CharField(max_length=234, blank=True)
    iso_4217_currency_code = models.CharField(max_length=33, blank=True)
    iso_4217_currency_name = models.CharField(max_length=42, blank=True)
    telephone_code = models.CharField(max_length=48, blank=True)
    iso_3166_1_2_letter_code = models.CharField(max_length=6, blank=True)
    iso_3166_1_3_letter_code = models.CharField(max_length=9,blank=True)
    iso_3166_1_number = models.IntegerField(null=True, blank=True)
    iana_country_code_tld = models.CharField(max_length=33, blank=True)
    continent = models.ForeignKey(Continent, blank=True, null=True)

    def __unicode__(self):
        return self.common_name

    class Meta:
        verbose_name ='Country'
        verbose_name_plural = 'Countries'


class BiomeFAO(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Biome FAO'
        verbose_name_plural = 'Biome FAO List'


class BiomeUdvardy(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Biome Udvardy'
        verbose_name_plural = 'Biome Udvardy List'


class BiomeWWF(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Biome WWF'
        verbose_name_plural = 'Biome WWF List'


class DivisionBailey(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Division Bailey'
        verbose_name_plural = 'Division Bailey List'


class BiomeHoldridge(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Biome Holdridge'
        verbose_name_plural = 'Biome Holdridge List'


class LocationGroup(models.Model):    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    locations = models.ManyToManyField('locations.Location', verbose_name="List of Locations", blank=True, null=True)
    original_Group_Location = models.IntegerField(null=True, blank=True, help_text="The original Group_Location from the global import")


class Location(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    Latitude = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=9
    )
    Longitude = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=9
    )
    country = models.ForeignKey(Country, blank=True, null=True)
    biome_fao = models.ForeignKey(BiomeFAO, blank=True, null=True)
    biome_udvardy = models.ForeignKey(BiomeUdvardy, blank=True, null=True)
    biome_wwf = models.ForeignKey(BiomeWWF, blank=True, null=True)
    division_bailey = models.ForeignKey(DivisionBailey, blank=True, null=True)
    biome_holdridge = models.ForeignKey(BiomeHoldridge, blank=True, null=True)
    original_ID_Location = models.IntegerField(null=True, blank=True, help_text="The original ID_Location from the global import")

    def __unicode__(self):
        return self.name
