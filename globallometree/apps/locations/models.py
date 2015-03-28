from django.db import models
from globallometree.apps.search_helpers.models import BaseModel

class Continent(BaseModel):
    Continent_ID = models.AutoField(primary_key=True)
    Code = models.CharField(max_length=2)
    Name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.Name

    class Meta:
        db_table = 'Continent'


class Country(BaseModel):
    Country_ID = models.AutoField(primary_key=True)
    Common_name = models.CharField(max_length=159, blank=True)
    Formal_name = models.CharField(max_length=159, blank=True)
    Common_name_fr = models.CharField(max_length=159, blank=True)
    Formal_name_fr = models.CharField(max_length=159, blank=True)
    Iso3166a2 = models.CharField(max_length=6, blank=True)
    Iso3166a3 = models.CharField(max_length=9,blank=True)
    Iso3166n3 = models.IntegerField(null=True, blank=True)
    Continent = models.ForeignKey(Continent, blank=True, null=True, db_column="Continent_ID")
    Centroid_latitude = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=5)
    Centroid_longitude = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=5)

    def __unicode__(self):
        return u'%s (%s)' % (self.Common_name, self.Iso3166a2)

    class Meta:
        verbose_name ='Country'
        verbose_name_plural = 'Countries'
        ordering = ('Common_name',)
        db_table = 'Country'


class BiomeFAO(BaseModel):
    Biome_FAO_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Biome FAO'
        verbose_name_plural = 'Biome FAO List'
        ordering = ('Name',)
        db_table = 'Biome_FAO'


class BiomeUdvardy(BaseModel):
    Biome_UDVARDY_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Biome Udvardy'
        verbose_name_plural = 'Biome Udvardy List'
        ordering = ('Name',)
        db_table = 'Biome_UDVARDY'


class BiomeWWF(BaseModel):
    Biome_WWF_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Biome WWF'
        verbose_name_plural = 'Biome WWF List'
        ordering = ('Name',)
        db_table = 'Biome_WWF'


class DivisionBailey(BaseModel):
    Division_BAILEY_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Division Bailey'
        verbose_name_plural = 'Division Bailey List'
        ordering = ('Name',)
        db_table = 'Division_BAILEY'


class BiomeHoldridge(BaseModel):
    Biome_HOLDRIDGE_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Biome Holdridge'
        verbose_name_plural = 'Biome Holdridge List'
        ordering = ('Name',)
        db_table = 'Biome_HOLDRIDGE'


class ForestType(BaseModel):
    Forest_type_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.Name

    class Meta:
        ordering = ('Name',)
        db_table = 'Forest_type'


class Location(BaseModel):
    Location_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255, null=True, blank=True)
    Commune = models.CharField(max_length=255, blank=True, null=True)
    Province = models.CharField(max_length=255, blank=True, null=True)
    Region = models.CharField(max_length=255, blank=True, null=True)
    Country = models.ForeignKey(Country, blank=True, null=True)
    Latitude = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=9
    )
    Longitude = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=9
    )
    Biome_FAO = models.ForeignKey(BiomeFAO, blank=True, null=True, db_column="Biome_FAO_ID")
    Biome_UDVARDY = models.ForeignKey(BiomeUdvardy, blank=True, null=True, db_column="Biome_UDVARDY_ID")
    Biome_WWF = models.ForeignKey(BiomeWWF, blank=True, null=True, db_column="Biome_WWF_ID")
    Division_BAILEY = models.ForeignKey(DivisionBailey, blank=True, null=True, db_column="Division_BAILEY_ID")
    Biome_HOLDRIDGE = models.ForeignKey(BiomeHoldridge, blank=True, null=True, db_column="Biome_HOLDRIDGE_ID")
    Forest_type =  models.ForeignKey(ForestType, blank=True, null=True, db_column="Forest_type_ID")

    def __unicode__(self):
        if self.Name:
            return self.Name 
        else:
            return 'Location %s' % self.pk

    class Meta:
        ordering = ('Name',)
        db_table = 'Location'


class Plot(BaseModel):
    Plot_ID = models.AutoField(primary_key=True)
    Location = models.ForeignKey(Location)
    Plot_name = models.CharField(
        max_length=30,
        help_text="name or id of the plot in the study, or data import"
        )
    Plot_size_m2 = models.DecimalField(
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=10,
        help_text="size of the plot in m2")

    class Meta:
        db_table = 'Plot'


class LocationGroup(BaseModel):
    Location_group_ID = models.AutoField(primary_key=True)

    Dataset = models.ForeignKey(
        'data_sharing.Dataset',
        blank = True,
        null = True,
        help_text = "If group was created from a dataset, the dataset id"
        )

    Dataset_Location_group_ID = models.IntegerField(
        blank = True,
        null = True,
        help_text = "If group was created from a dataset, references the local group id in the source dataset"
    )

    Name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Group Name")

    Locations = models.ManyToManyField(Location,
        verbose_name="List of Locations",
        blank=True,
        null=True,
        help_text="Only add in locations here when the Plot Id is unknown"
        )

    Plots = models.ManyToManyField(Plot,
        verbose_name="List of Plots",
        blank=True,
        null=True
        )

    def Group(self):
        """
            Returns a flat list of plots and locations, etc for the LocationGroupSerializer,
            Ideally this would be in the api, but the syntax for that was not working
        """
        data = []
        from globallometree.apps.api.serializers import (
            LocationSerializer,
            PlotSerializer
            )

        for plot in self.Plots.all():
            location_data = PlotSerializer(instance=plot, many=False).data
            data.append(location_data)

        for location in self.Locations.all():
            location_data = LocationSerializer(instance=location, many=False).data
            data.append(location_data)

        return data

    def save(self, *args, **kwargs):

        super(LocationGroup, self).save(*args, **kwargs)

        if not self.Name:
            self.Name = 'Location Group %s' % self.pk
            self.save()


    class Meta:
        db_table = 'Location_group'

    def __unicode__(self):
        return self.Name
