from django.db import models
from globallometree.apps.search_helpers.models import BaseModel

class Continent(BaseModel):
    Continent_ID = models.AutoField(primary_key=True, db_column="continent_id")
    Code = models.CharField(max_length=2, db_column="code")
    Name = models.CharField(max_length=100, db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        db_table = 'locations_continent'


class Country(BaseModel):
    Country_ID = models.AutoField(primary_key=True, db_column="country_id")
    Common_name = models.CharField(max_length=159, blank=True, db_column="common_name")
    Formal_name = models.CharField(max_length=159, blank=True, db_column="formal_name")
    Common_name_fr = models.CharField(max_length=159, blank=True, db_column="common_name_fr")
    Formal_name_fr = models.CharField(max_length=159, blank=True, db_column="formal_name_fr")
    Iso3166a2 = models.CharField(max_length=6, blank=True, db_column="iso3166a2")
    Iso3166a3 = models.CharField(max_length=9, blank=True, db_column="iso3166a3")
    Iso3166n3 = models.IntegerField(null=True, blank=True, db_column="iso3166n3")
    Continent = models.ForeignKey(Continent, blank=True, null=True, db_column="continent_id")
    Centroid_latitude = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=5, db_column="centroid_latitude")
    Centroid_longitude = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=5, db_column="centroid_longitude")

    def __unicode__(self):
        return u'%s (%s)' % (self.Common_name, self.Iso3166a2)

    class Meta:
        verbose_name ='Country'
        verbose_name_plural = 'Countries'
        ordering = ('Common_name',)
        db_table = 'locations_country'


class ZoneFAO(BaseModel):
    Zone_FAO_ID = models.AutoField(primary_key=True, db_column="zone_fao_id")
    Name = models.CharField(max_length=200,  db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'FAO Global Ecological Zone'
        verbose_name_plural = 'FAO Global Ecological Zones'
        ordering = ('Name',)
        db_table = 'locations_zone_fao'



class BiomeLocal(BaseModel):
    Biome_local_ID = models.AutoField(primary_key=True, db_column="biome_local_id")
    Reference = models.CharField(max_length=200,  db_column="reference")
    Name = models.CharField(max_length=200,  db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Local Biome'
        verbose_name_plural = 'Local Biomes'
        ordering = ('Name',)
        db_table = 'locations_biome_local'


class EcoregionUdvardy(BaseModel):
    Ecoregion_Udvardy_ID = models.AutoField(primary_key=True, db_column="ecoregion_udvardy_id")
    Name = models.CharField(max_length=200, db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Udvardy Ecoregion'
        verbose_name_plural = 'Udvardy Ecoregions'
        ordering = ('Name',)
        db_table = 'locations_ecoregion_udvardy'


class EcoregionWWF(BaseModel):
    Ecoregion_WWF_ID = models.AutoField(primary_key=True, db_column="ecoregion_wwf_id")
    Name = models.CharField(max_length=200, db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'WWF Terrestrial Ecoregion'
        verbose_name_plural = 'WWF Terrestrial Ecoregion'
        ordering = ('Name',)
        db_table = 'locations_ecoregion_wwf'


class DivisionBailey(BaseModel):
    Division_BAILEY_ID = models.AutoField(primary_key=True, db_column="division_bailey_id")
    Name = models.CharField(max_length=200, db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Division Bailey'
        verbose_name_plural = 'Division Bailey List'
        ordering = ('Name',)
        db_table = 'locations_division_bailey'


class ZoneHoldridge(BaseModel):
    Zone_Holdridge_ID = models.AutoField(primary_key=True, db_column="zone_holdridge_id")
    Name = models.CharField(max_length=200, db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Holdridge Life Zone'
        verbose_name_plural = 'Holdridge Life Zones'
        ordering = ('Name',)
        db_table = 'locations_zone_holdridge'


class ForestType(BaseModel):
    Forest_type_ID = models.AutoField(primary_key=True, db_column="forest_type_id")
    Name = models.CharField(max_length=255, null=True, blank=True, db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        ordering = ('Name',)
        db_table = 'locations_forest_type'


class Location(BaseModel):
    Location_ID = models.AutoField(primary_key=True, db_column="location_id")
    Name = models.CharField(max_length=255, null=True, blank=True, db_column="name")
    Plot_name = models.CharField(
        max_length=30,
        help_text="name or id of the plot in the study, or data import",
        blank=True,
        null=True,
        db_column="plot_name"
        )
    Plot_size_m2 = models.DecimalField(
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=10,
        help_text="size of the plot in m2",
        db_column="plot_size_m2"
        )
    Commune = models.CharField(max_length=255, blank=True, null=True, db_column="commune")
    Province = models.CharField(max_length=255, blank=True, null=True, db_column="province")
    Region = models.CharField(max_length=255, blank=True, null=True, db_column="region")
    Country = models.ForeignKey(Country, blank=True, null=True, db_column="country_id")
    Latitude = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=9, db_column="latitude"
    )
    Longitude = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=9, db_column="longitude"
    )
    Zone_FAO = models.ForeignKey(ZoneFAO, blank=True, null=True, db_column="zone_fao_id")
    Ecoregion_Udvardy = models.ForeignKey(EcoregionUdvardy, blank=True, null=True, db_column="ecoregion_udvardy_id")
    Ecoregion_WWF = models.ForeignKey(EcoregionWWF, blank=True, null=True, db_column="ecoregion_wwf_id")
    Division_BAILEY = models.ForeignKey(DivisionBailey, blank=True, null=True, db_column="division_bailey_id")
    Zone_Holdridge = models.ForeignKey(ZoneHoldridge, blank=True, null=True, db_column="zone_holdridge_id")
    Forest_type =  models.ForeignKey(ForestType, blank=True, null=True, db_column="forest_type_id")
    Biome_local =  models.ForeignKey(BiomeLocal, blank=True, null=True, db_column="biome_local_id")

    def __unicode__(self):
        if self.Name:
            return self.Name 
        else:
            return 'Location %s' % self.pk

    class Meta:
        ordering = ('Name',)
        db_table = 'locations_location'


class LocationGroup(BaseModel):

    Location_group_ID = models.AutoField(primary_key=True, db_column="location_group_id")

    Dataset = models.ForeignKey(
        'data_sharing.Dataset',
        blank = True,
        null = True,
        help_text = "If group was created from a dataset, the dataset id",
        db_column="dataset_id"
        )

    Dataset_Location_group_ID = models.IntegerField(
        blank = True,
        null = True,
        help_text = "If group was created from a dataset, references the local group id in the source dataset",
        db_column="dataset_location_group_id"
        )

    Name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Group Name",
        db_column="name"
        )

    Locations = models.ManyToManyField(Location,
        verbose_name="List of Locations",
        blank=True,
        db_table="locations_group_locations"
        )


    def save(self, *args, **kwargs):

        super(LocationGroup, self).save(*args, **kwargs)

        if not self.Name:
            self.Name = 'Location Group %s' % self.pk
            self.save()


    class Meta:
        db_table = 'locations_group'

    def __unicode__(self):
        return self.Name
