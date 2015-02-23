from django.db import models
from globallometree.apps.common.models import BaseModel


class Reference(BaseModel):
    Reference_ID = models.AutoField(primary_key=True)
    Label = models.CharField(max_length=20, null=True, blank=True)
    Author = models.CharField(max_length=200, null=True, blank=True)
    Year = models.CharField(max_length=12, null=True, blank=True)
    Reference = models.TextField(null=True, blank=True)
    Original_ID_REF = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('Label',)
        db_table = "Reference"

    def __unicode__(self):
        return u'%s' % self.Label


class Institution(BaseModel):
    Institution_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        ordering = ('Name',)
        db_table = "Institution"

    def __unicode__(self):
        return self.Name


class Operator(BaseModel):
    """Operator is at least used for the wood density database"""
    Operator_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    Institution = models.ForeignKey(Institution)

    class Meta:
        ordering = ('Name',)
        db_table = "Operator"

    def __unicode__(self):
        return self.Name
