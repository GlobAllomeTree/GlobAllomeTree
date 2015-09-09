from django.db import models
from globallometree.apps.base.models import BaseModel

class TreeType(BaseModel):
    ID_Tree_type = models.AutoField(primary_key=True, db_column="id_tree_type")
    Name = models.CharField(max_length=255, null=True, blank=True, db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        ordering = ('Name',)
        db_table = 'identification_tree_type'



class VegetationType(BaseModel):
    ID_Vegetation_type = models.AutoField(primary_key=True, db_column="id_vegetation_type")
    Name = models.CharField(max_length=255, null=True, blank=True, db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        ordering = ('Name',)
        db_table = 'identification_vegetation_type'
