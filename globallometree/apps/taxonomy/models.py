from django.db import models


class Family(models.Model):
    name = models.CharField(max_length=80, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Families'

    def __unicode__(self):
        return self.name


class Genus(models.Model):
    name  = models.CharField(max_length=80, null=True, blank=True)
    family = models.ForeignKey(Family, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Genera'

    def __unicode__(self):
        return self.name


class SpeciesGroup(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Species(models.Model):
    name = models.CharField(max_length=80, null=True, blank=True)
    genus = models.ForeignKey(Genus, null=True, blank=True)
    group = models.ForeignKey(SpeciesGroup, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Species'

    def __unicode__(self):
        return self.name
