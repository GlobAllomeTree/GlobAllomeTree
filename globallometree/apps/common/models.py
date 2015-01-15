from django.db import models

class BaseModel(models.Model):
    Created = models.DateTimeField(auto_now_add=True)
    Modified = models.DateTimeField(auto_now=True, verbose_name="Last modified")

    class Meta:
        abstract = True


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
        'source.Reference', 
        blank=True, 
        null=True,
        db_column='Reference_ID')

    Operator = models.ForeignKey(
        'source.Operator', 
        blank=True, 
        null=True,
        db_column='Operator_ID'
        )

    Contributor = models.ForeignKey(
        'source.Institution', 
        blank=True, 
        null=True,
        db_column='Contributor_ID')

    Dataset = models.ForeignKey(
        'data_sharing.Dataset',null=True, blank=True,
        help_text="The Dataset that this raw data record came from")

    class Meta:
        abstract = True

