from django.db import models


class DataReference(models.Model):
    Label = models.CharField(max_length=20, null=True, blank=True)
    Author = models.CharField(max_length=200, null=True, blank=True)
    Year = models.CharField(max_length=12, null=True, blank=True)
    Reference = models.TextField(null=True, blank=True)


class Institution(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
