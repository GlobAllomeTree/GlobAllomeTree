from django.db import models
from globallometree.apps.base.models import BaseModel

class Continent(BaseModel):
    ID_Continent = models.AutoField(primary_key=True, db_column="id_continent")
    Code = models.CharField(max_length=2, db_column="code")
    Name = models.CharField(max_length=100, db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        db_table = 'locations_continent'


class Country(BaseModel):
    ID_Country = models.AutoField(primary_key=True, db_column="id_country")
    Common_name = models.CharField(max_length=159, blank=True, db_column="common_name")
    Formal_name = models.CharField(max_length=159, blank=True, db_column="formal_name")
    Common_name_fr = models.CharField(max_length=159, blank=True, db_column="common_name_fr")
    Formal_name_fr = models.CharField(max_length=159, blank=True, db_column="formal_name_fr")
    Iso3166a2 = models.CharField(max_length=6, blank=True, db_column="iso3166a2")
    Iso3166a3 = models.CharField(max_length=9, blank=True, db_column="iso3166a3")
    Iso3166n3 = models.IntegerField(null=True, blank=True, db_column="iso3166n3")
    Continent = models.ForeignKey(Continent, blank=True, null=True, db_column="id_continent")
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
    ID_Zone_FAO = models.AutoField(primary_key=True, db_column="id_zone_fao")
    Name = models.CharField(max_length=200,  db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'FAO Global Ecological Zone'
        verbose_name_plural = 'FAO Global Ecological Zones'
        ordering = ('Name',)
        db_table = 'locations_zone_fao'


class EcoregionUdvardy(BaseModel):
    ID_Ecoregion_Udvardy = models.AutoField(primary_key=True, db_column="id_ecoregion_udvardy")
    Name = models.CharField(max_length=200, db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Udvardy Ecoregion'
        verbose_name_plural = 'Udvardy Ecoregions'
        ordering = ('Name',)
        db_table = 'locations_ecoregion_udvardy'


class EcoregionWWF(BaseModel):
    ID_Ecoregion_WWF = models.AutoField(primary_key=True, db_column="id_ecoregion_wwf")
    Name = models.CharField(max_length=200, db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'WWF Terrestrial Ecoregion'
        verbose_name_plural = 'WWF Terrestrial Ecoregion'
        ordering = ('Name',)
        db_table = 'locations_ecoregion_wwf'


class DivisionBailey(BaseModel):
    ID_Division_Bailey = models.AutoField(primary_key=True, db_column="id_division_bailey")
    Name = models.CharField(max_length=200, db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Division Bailey'
        verbose_name_plural = 'Division Bailey List'
        ordering = ('Name',)
        db_table = 'locations_division_bailey'


class ZoneHoldridge(BaseModel):
    ID_Zone_Holdridge = models.AutoField(primary_key=True, db_column="id_zone_holdridge")
    Name = models.CharField(max_length=200, db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Holdridge Life Zone'
        verbose_name_plural = 'Holdridge Life Zones'
        ordering = ('Name',)
        db_table = 'locations_zone_holdridge'




class Location(BaseModel):
    ID_Location = models.AutoField(primary_key=True, db_column="id_location")
    Name = models.CharField(max_length=255, null=True, blank=True, db_column="name")
    Region = models.CharField(max_length=255, blank=True, null=True, db_column="region")
    Country = models.ForeignKey(Country, blank=True, null=True, db_column="id_country")
    Latitude = models.DecimalField(
        null=True, blank=True, max_digits=8, decimal_places=5, db_column="latitude"
    )
    Longitude = models.DecimalField(
        null=True, blank=True, max_digits=8, decimal_places=5, db_column="longitude"
    )
    Zone_FAO = models.ForeignKey(ZoneFAO, blank=True, null=True, db_column="id_zone_fao")
    Ecoregion_Udvardy = models.ForeignKey(EcoregionUdvardy, blank=True, null=True, db_column="id_ecoregion_udvardy")
    Ecoregion_WWF = models.ForeignKey(EcoregionWWF, blank=True, null=True, db_column="id_ecoregion_wwf")
    Division_Bailey = models.ForeignKey(DivisionBailey, blank=True, null=True, db_column="id_division_bailey")
    Zone_Holdridge = models.ForeignKey(ZoneHoldridge, blank=True, null=True, db_column="id_zone_holdridge")

    def __unicode__(self):
        if self.Name:
            return self.Name 
        else:
            return 'Location %s' % self.pk

    class Meta:
        ordering = ('ID_Location',)
        db_table = 'locations_location'


class LocationGroup(BaseModel):

    ID_Location_group = models.AutoField(primary_key=True, db_column="id_location_group")

    Dataset = models.ForeignKey(
        'data_sharing.Dataset',
        blank = True,
        null = True,
        help_text = "If group was created from a dataset, the dataset id",
        db_column="id_dataset"
        )

    Dataset_ID_Location_group = models.IntegerField(
        blank = True,
        null = True,
        help_text = "If group was created from a dataset, references the local group id in the source dataset",
        db_column="dataset_id_location_group"
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
