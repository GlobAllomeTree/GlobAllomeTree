from django.db import models
from django.core.urlresolvers import reverse
from globallometree.apps.common.models import TimeStampedModel

class Family(TimeStampedModel):
    name = models.CharField(max_length=80, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Families'
        ordering = ('name',)
        
    def __unicode__(self):
        return self.name


class Genus(TimeStampedModel):
    name  = models.CharField(max_length=80, null=True, blank=True)
    family = models.ForeignKey(Family, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Genera'
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Species(TimeStampedModel):
    name = models.CharField(max_length=80, null=True, blank=True)
    genus = models.ForeignKey(Genus, null=True, blank=True)
    original_ID_Species = models.IntegerField(
        null=True, blank=True,
        help_text="The original ID_Species from the global import"
    )

    class Meta:
        verbose_name_plural = 'Species'
        ordering = ('name',)

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
                self.name,
                self.genus.name
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


class Subspecies(TimeStampedModel):
    name = models.CharField(max_length=80)
    species = models.ForeignKey(Species)
    

    class Meta:
        verbose_name_plural = 'Subspecies'
        ordering = ('name',)

    def __unicode__(self):
        return self.name



class SpeciesLocalName(TimeStampedModel):
    # A local name could either be for a species or a subspecies
    species = models.ForeignKey(Species, blank=True, null=True, related_name="local_names")

    local_name = models.CharField(
        max_length=80,
        help_text="The local name of this species in the local language"
    )

    local_name_latin = models.CharField(
        max_length=80,
        null=True,
        blank=True,
        help_text="A phonetic version using the latin alphabet"
    )

    language_iso_639_3 = models.CharField(
        max_length=3, 
        help_text="The ISO 639-3 Language Code for the language"
    )



class SubspeciesLocalName(TimeStampedModel):
    # A local name could either be for a species or a subspecies
    subspecies = models.ForeignKey(Subspecies, blank=True, null=True,related_name="local_names")

    local_name = models.CharField(
        max_length=80,
        help_text="The local name of this subspecies in the local language"
    )

    local_name_latin = models.CharField(
        max_length=80,
        null=True,
        blank=True,
        help_text="A phonetic version using the latin alphabet"
    )

    language_iso_639_3 = models.CharField(
        max_length=3, 
        help_text="The ISO 639-3 Language Code for the language"
    )


class SpeciesGroup(TimeStampedModel):
    name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Group Name"
    )

    subspecies = models.ManyToManyField(
        Subspecies, 
        verbose_name="List of Subspecies", 
        blank=True, 
        null=True,
    )

    species = models.ManyToManyField(
        Species, 
        verbose_name="List of Species", 
        blank=True, 
        null=True,
    )
    original_ID_Group = models.IntegerField(
        null=True, blank=True,
        help_text="The original ID_Group from the global import"
    )

    def species_set(self):
        species_list = []
        for species in self.species.all():
            #Allow for empty genus or family
            names = []
            
            try:
                names.append(species.genus.family.name)
            except:
                pass

            try:
                names.append(species.genus.name)
            except:
                pass

            names.append(species.name)

            species_list.append(' '.join(names))

        return list(set(species_list)) 

    def __unicode__(self):
        return self.name
