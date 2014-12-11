from django.db import models

class BaseModel(models.Model):
    Created = models.DateTimeField(auto_now_add=True)
    Modified = models.DateTimeField(auto_now=True, verbose_name="Last modified")

    class Meta:
        abstract = True


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


class LinkedBaseModel(BaseModel):
    Species_group = models.ForeignKey(
        'taxonomy.SpeciesGroup',
        null=True, 
        blank=True,
        db_column='Species_group_ID')

    Location_group = models.ForeignKey(
        'locations.LocationGroup',
        null=True, 
        blank=True,
        db_column='Location_group_ID')

    Reference = models.ForeignKey(
        Reference, 
        blank=True, 
        null=True,
        db_column='Reference_ID')

    Operator = models.ForeignKey(
        Operator, 
        blank=True, 
        null=True,
        db_column='Operator_ID'
        )

    Contributor = models.ForeignKey(
        Institution, 
        blank=True, 
        null=True,
        db_column='Contributor_ID')

    Dataset = models.ForeignKey(
        'data_sharing.Dataset',null=True, blank=True,
        help_text="The Dataset that this raw data record came from")

    class Meta:
        abstract = True

