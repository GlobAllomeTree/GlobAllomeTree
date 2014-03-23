from django.db import models


class Family(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True,verbose_name="Last modified")
    name = models.CharField(max_length=80, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Families'

    def __unicode__(self):
        return self.name


class Genus(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, verbose_name="Last modified")
    name  = models.CharField(max_length=80, null=True, blank=True)
    family = models.ForeignKey('taxonomy.Family', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Genera'

    def __unicode__(self):
        return self.name


class Species(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, verbose_name="Last modified")

    name = models.CharField(max_length=80, null=True, blank=True)
    genus = models.ForeignKey(Genus, null=True, blank=True)
    original_ID_Species = models.IntegerField(null=True, blank=True, help_text="The original ID_Species from the global import")

    class Meta:
        verbose_name_plural = 'Species'

    def __unicode__(self):
        return self.name


class SpeciesGroup(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Group Name")
    species = models.ManyToManyField('taxonomy.Species', verbose_name="List of Species", blank=True, null=True)
    original_ID_Group = models.IntegerField(null=True, blank=True, help_text="The original ID_Group from the global import")

    def species_string(self):
        string = ''
        for species in self.species.all():
            if string != '': string += ', '
            string += species.name
        return string

    def genera(self):
        return list(set([
            species.genus for species in
                self.species.all() if species.genus is not None
        ]))

    def genera_string(self):
        string = ''
        for genus in self.genera():
            if string != '': string += ', '
            string += genus.name
        return string

    def __unicode__(self):
        return self.name

        
