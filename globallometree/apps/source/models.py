from django.db import models
from globallometree.apps.search_helpers.models import BaseModel


class Reference(BaseModel):
    Reference_ID = models.AutoField(primary_key=True, db_column="reference_id")
    Author = models.CharField(max_length=200, null=True, blank=True, db_column="author")
    Year = models.CharField(max_length=12, null=True, blank=True, db_column="year")
    Reference = models.TextField(null=True, blank=True, db_column="reference")

    class Meta:
        ordering = ('Reference',)
        db_table = "source_reference"

    def __unicode__(self):
        return u'%s' % self.Reference


class Institution(BaseModel):
    Institution_ID = models.AutoField(primary_key=True, db_column="institution_id")
    Name = models.CharField(max_length=150, null=True, blank=True, db_column="name")

    class Meta:
        ordering = ('Name',)
        db_table = "source_institution"

    def __unicode__(self):
        return self.Name


class Operator(BaseModel):
    """Operator is at least used for the wood density database"""
    Operator_ID = models.AutoField(primary_key=True, db_column="operator_id")
    Name = models.CharField(max_length=200, db_column="name")
    Institution = models.ForeignKey(Institution, db_column="institution_id")

    class Meta:
        ordering = ('Name',)
        db_table = "source_operator"

    def __unicode__(self):
        return self.Name
