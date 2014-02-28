from django.db import models

class Continent(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

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

class BiomeUdvardy(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

class BiomeWWF(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

class BiomeBailey(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

class BiomeHoldridge(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True) 

class Location(models.Model):
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
    biome_bailey = models.ForeignKey(BiomeBailey, blank=True, null=True)
    biome_holdridge = models.ForeignKey(BiomeHoldridge, blank=True, null=True)
