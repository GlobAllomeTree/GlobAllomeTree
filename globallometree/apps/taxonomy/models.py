from django.db import models


class Family(models.Model):
    name = models.CharField(max_length=80, null=True, blank=True)


class Genus(models.Model):
    name  = models.CharField(max_length=80, null=True, blank=True)
    family = models.ForeignKey(Family, null=True, blank=True)


class SpeciesGroup(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)


class Species(models.Model):
    genus = models.ForeignKey(Genus, null=True, blank=True)
    name = models.CharField(max_length=80, null=True, blank=True)
    group = models.ForeignKey(SpeciesGroup, null=True, blank=True)
