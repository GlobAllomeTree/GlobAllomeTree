from django.db import models

class DataReference(models.Model):
    label = models.CharField(max_length=20, null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    year = models.CharField(max_length=12, null=True, blank=True)
    reference = models.TextField(null=True, blank=True)
    original_ID_REF = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('label',)

    def __unicode__(self):

        return u'%s' % self.label

class Institution(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, verbose_name="Last modified")

    class Meta:
        abstract = True


class Operator(TimeStampedModel):
    """Operator is at least used for the wood density database"""
    name = models.CharField(max_length=200)
    institution = models.ForeignKey(Institution)