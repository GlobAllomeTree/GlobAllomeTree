from django.db import models

class BaseModel(models.Model):
    ID = models.AutoField(primary_key=True)
    Created = models.DateTimeField(auto_now_add=True)
    Modified = models.DateTimeField(auto_now=True, verbose_name="Last modified")

    class Meta:
        abstract = True


class DataReference(BaseModel):
    Label = models.CharField(max_length=20, null=True, blank=True)
    Author = models.CharField(max_length=200, null=True, blank=True)
    Year = models.CharField(max_length=12, null=True, blank=True)
    Reference = models.TextField(null=True, blank=True)
    Original_ID_REF = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('Label',)

    def __unicode__(self):
        return u'%s' % self.Label


class Institution(BaseModel):
    Name = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        ordering = ('Name',)

    def __unicode__(self):
        return self.Name


class Operator(BaseModel):
    """Operator is at least used for the wood density database"""
    Name = models.CharField(max_length=200)
    Institution = models.ForeignKey(Institution)
