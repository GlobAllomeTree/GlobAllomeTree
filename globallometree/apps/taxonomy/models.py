from django.db import models


class Family(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True,verbose_name="Last modified")
    name = models.CharField(max_length=80, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Families'
        ordering = ('name',)
        
    def __unicode__(self):
        return self.name


class Genus(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, verbose_name="Last modified")
    name  = models.CharField(max_length=80, null=True, blank=True)
    family = models.ForeignKey(Family, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Genera'
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Species(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, verbose_name="Last modified")
    name = models.CharField(max_length=80, null=True, blank=True)
    genus = models.ForeignKey(Genus, null=True, blank=True)
    original_ID_Species = models.IntegerField(
        null=True, blank=True,
        help_text="The original ID_Species from the global import"
    )

    class Meta:
        verbose_name_plural = 'Species'
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class SpeciesGroup(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Group Name"
    )
    species = models.ManyToManyField(
        Species, verbose_name="List of Species", blank=True, null=True
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
