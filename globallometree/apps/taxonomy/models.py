from django.db import models
from django.core.urlresolvers import reverse
from globallometree.apps.search_helpers.models import BaseModel
from globallometree.apps.data_sharing.models import Dataset


class TaxonomyModel(BaseModel):
    TPL_Status = models.CharField(max_length=80, blank=True, null=True, db_column="tpl_status")
    TPL_Confidence_level = models.CharField(max_length=10, blank=True, null=True, db_column="tpl_confidence_level")
    TPL_ID = models.CharField(max_length=40, blank=True, null=True, db_column="tpl_id")
    class Meta:
        abstract = True

class Family(TaxonomyModel):
    ID_Family = models.AutoField(primary_key=True, db_column="id_family")
    Name = models.CharField(max_length=120, null=True, blank=True, db_column="name")

    class Meta:
        verbose_name_plural = 'Families'
        ordering = ('ID_Family',)
        db_table = 'taxonomy_family'
        
    def __unicode__(self):
        return self.Name


class Genus(TaxonomyModel):
    ID_Genus = models.AutoField(primary_key=True, db_column="id_genus")
    Name  = models.CharField(max_length=120, db_column="name")
    Family = models.ForeignKey(Family, db_column="id_family")

    class Meta:
        verbose_name_plural = 'Genera'
        ordering = ('ID_Genus',)
        db_table = 'taxonomy_genus'

    def __unicode__(self):
        return self.Name
 

class Species(TaxonomyModel):
    ID_Species = models.AutoField(primary_key=True, db_column="id_species")
    Name = models.CharField(max_length=120, db_column="name")
    Genus = models.ForeignKey(Genus, db_column="id_genus")
    Author = models.CharField(max_length=120, db_column="author", blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Species'
        ordering = ('ID_Species',)
        db_table = 'taxonomy_species'

    def __unicode__(self):
        return self.Name


class Subspecies(TaxonomyModel):
    ID_Subspecies = models.AutoField(primary_key=True, db_column="id_subspecies")
    Name = models.CharField(max_length=120, db_column="name")
    Species = models.ForeignKey(Species, db_column="id_species")
    Author = models.CharField(max_length=120, db_column="author", blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Subspecies'
        ordering = ('ID_Subspecies',)
        db_table = 'taxonomy_subspecies'

    def __unicode__(self):
        return self.Name


class SpeciesLocalName(BaseModel):

    ID_Local_name = models.AutoField(primary_key=True, db_column="id_local_name")
    
    Species = models.ForeignKey(Species, related_name="Local_names", db_column="id_species")

    Local_name = models.CharField(
        max_length=120,
        help_text="The local name of this species in the local language",
        db_column="local_name"
    )

    Local_name_latin = models.CharField(
        max_length=80,
        null=True,
        blank=True,
        help_text="A phonetic version using the latin alphabet",
        db_column="local_name_latin"
    )

    Language_iso_639_3 = models.CharField(
        max_length=3, 
        help_text="The ISO 639-3 Language Code for the language",
        db_column="language_iso_639_3",
        null=True,
        blank=True
    )

    class Meta:
        db_table = "taxonomy_species_local_name"
        ordering = ("ID_Local_name",)


class SpeciesDefinition(BaseModel):
    ID_Species_definition = models.AutoField(primary_key=True, db_column="id_species_definition")
    Family = models.ForeignKey(Family, db_column="id_family")
    Genus = models.ForeignKey(Genus, blank=True, null=True, db_column="id_genus")
    Species = models.ForeignKey(Species, blank=True, null=True, db_column="id_species")
    Subspecies = models.ForeignKey(Subspecies, blank=True, null=True, db_column="subid_species")

    def Scientific_name(self):
        scientific_name = ''

        if self.Family:
            scientific_name += self.Family.Name

        if self.Genus:
            scientific_name += ' ' + self.Genus.Name

        if self.Species:
            scientific_name += ' ' + self.Species.Name

        if self.Subspecies:
            scientific_name += ' ' + self.Subspecies.Name

        return scientific_name

    def Species_author(self):
        if self.Subspecies and self.Subspecies.Author:
            return self.Subspecies.Author
        elif self.Species and self.Species.Author:
            return self.Species.Author
        else:
            return None


    def __unicode__(self):
        return "Species Defintion %s" % self.pk


    class Meta:
        db_table = "taxonomy_species_definition"
        ordering = ("ID_Species_definition",)


class SpeciesGroup(BaseModel):

    ID_Species_group = models.AutoField(
        primary_key=True,
        db_column="id_species_group"
        )

    Dataset = models.ForeignKey(
        'data_sharing.Dataset',
        blank = True,
        null = True,
        help_text = "If group was created from a dataset, the dataset id",
        db_column="id_dataset"
        )

    ID_Dataset_Species_group = models.IntegerField(
        blank = True,
        null = True,
        help_text = "If group was created from a dataset, references the local group id in the source dataset",
        db_column="dataset_id_species_group"
    )

    Name = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name="Group Name",
        db_column="name"
    )

    Species_definitions = models.ManyToManyField(SpeciesDefinition,
        verbose_name="List of Species Definitions",
        blank=True,
        db_table='taxonomy_species_group_definitions'
        )

    class Meta:
        db_table = "taxonomy_species_group"
        ordering = ('ID_Species_group',)

    def save(self, *args, **kwargs):

        super(SpeciesGroup, self).save(*args, **kwargs)

        if not self.Name:
            self.Name = 'Species Group %s' % self.pk
            self.save()


    def __unicode__(self):
        return self.Name if self.Name else 'Species Group'
