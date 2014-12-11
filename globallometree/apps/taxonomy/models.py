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
    Name  = models.CharField(max_length=80, null=True, blank=True)
    Family = models.ForeignKey(Family, null=True, blank=True, db_column="Family_ID")

    class Meta:
        verbose_name_plural = 'Genera'
        db_table = "Genus"
        ordering = ('Name',)

    def __unicode__(self):
        return self.Name


class Species(BaseModel):
    Species_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=80, null=True, blank=True)
    Genus = models.ForeignKey(Genus, null=True, blank=True, db_column="Genus_ID")
    
    class Meta:
        verbose_name_plural = 'Species'
        db_table = "Species"
        ordering = ('Name',)

    def allometric_equation_count(self):
        """How many allometric equations there are for this species """

        equation_count = 0
        for group in self.speciesgroup_set.all():
            equation_count += group.allometricequation_set.count()
        return equation_count

    def allometric_equation_link(self):
        """ Returns a link to the allometric equations for this species """
        return u'%s?Species=%s&Genus=%s' % (
                reverse('equation_search'),
                self.Name,
                self.Genus.name
                )

    def country_list(self):
        """ Countries that this species is in """
        countries = []
        for group in self.speciesgroup_set.all():
            for equation in group.allometricequation_set.all():
                countries += equation.location_group.countries()
        return list(set(countries))

    def __unicode__(self):
        return self.name


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

    class Meta:
        db_table = "Species_group"

    def species_set(self):
        species_list = []
        for species in self.Species.all():
            #Allow for empty genus or family
            names = []
            
            try:
                names.append(species.Genus.Family.Name)
            except:
                pass

            try:
                names.append(species.Genus.Name)
            except:
                pass

            names.append(species.Name)

            species_list.append(' '.join(Names))

        return list(set(species_list)) 

    def __unicode__(self):
        return self.Name
