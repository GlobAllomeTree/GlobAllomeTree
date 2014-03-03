from django.db import models


class DataReference(models.Model):
    label = models.CharField(max_length=20, null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    year = models.CharField(max_length=12, null=True, blank=True)
    reference = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.year + ' ' + self.author


class Institution(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)

    def __unicode__(self):
        return self.name
