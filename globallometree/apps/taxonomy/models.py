from django.db import models
from django.core.urlresolvers import reverse
from globallometree.apps.common.models import BaseModel

class Family(BaseModel):
    Family_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=80, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Families'
        db_table = "Family"
        ordering = ('Name',)
        
    def __unicode__(self):
        return self.Name


class Genus(BaseModel):
    Genus_ID = models.AutoField(primary_key=True)
    Name  = models.CharField(max_length=80)
    Family = models.ForeignKey(Family, db_column="Family_ID")

    class Meta:
        verbose_name_plural = 'Genera'
        db_table = "Genus"
        ordering = ('Name',)

    def __unicode__(self):
        return self.Name


class Species(BaseModel):
    Species_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=80)
    Genus = models.ForeignKey(Genus, db_column="Genus_ID")
    
    class Meta:
        verbose_name_plural = 'Species'
        db_table = "Species"
        ordering = ('Name',)

    def __unicode__(self):
        return self.Name


class Subspecies(BaseModel):
    Subspecies_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=80)
    Species = models.ForeignKey(Species, db_column="Species_ID")

    class Meta:
        verbose_name_plural = 'Subspecies'
        db_table = "Subspecies"
        ordering = ('Name',)

    def __unicode__(self):
        return self.Name



class SpeciesLocalName(BaseModel):

    Species_local_name_ID = models.AutoField(primary_key=True)
    
    # A local name could either be for a species or a subspecies
    Species = models.ForeignKey(Species, blank=True, null=True, related_name="Local_names", db_column="Species_ID")

    Local_name = models.CharField(
        max_length=80,
        help_text="The local name of this species in the local language"
    )

    Local_name_latin = models.CharField(
        max_length=80,
        null=True,
        blank=True,
        help_text="A phonetic version using the latin alphabet"
    )

    Language_iso_639_3 = models.CharField(
        max_length=3, 
        help_text="The ISO 639-3 Language Code for the language"
    )

    class Meta:
        db_table = "Species_local_name"


class SubspeciesLocalName(BaseModel):
    Subspecies_local_name_ID = models.AutoField(primary_key=True)
    
    # A local name could either be for a species or a subspecies
    Subspecies = models.ForeignKey(Subspecies, blank=True, null=True,related_name="Local_names", db_column="Subspecies_ID")

    Local_name = models.CharField(
        max_length=80,
        help_text="The local name of this subspecies in the local language"
    )

    Local_name_latin = models.CharField(
        max_length=80,
        null=True,
        blank=True,
        help_text="A phonetic version using the latin alphabet"
    )

    Language_iso_639_3 = models.CharField(
        max_length=3, 
        help_text="The ISO 639-3 Language Code for the language"
    )

    class Meta:
        db_table = "Subspecies_local_name"


class SpeciesGroup(BaseModel):

    Species_group_ID = models.AutoField(primary_key=True)

    Name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Group Name"
    )

    Subspecies = models.ManyToManyField(
        Subspecies, 
        verbose_name="List of Subspecies", 
        blank=True, 
        null=True,
    )

    Species = models.ManyToManyField(
        Species, 
        verbose_name="List of Species", 
        blank=True, 
        null=True,
    )

    Genera = models.ManyToManyField(
        Genus, 
        verbose_name="List of Genus", 
        blank=True, 
        null=True,
    )

    class Meta:
        db_table = "Species_group"

    def __unicode__(self):
        return self.Name
