from django.db import models
from elasticutils.contrib.django import get_es

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

    def serialize(self, request=None):
        SerializerClass = self.get_serializer_class()
        context = {}
        if request:
            context['request'] = request
        serialized_data = SerializerClass(self, context=context).data
        return serialized_data 

    def update_index(self):
        IndexClass = self.get_index_class()
        document = IndexClass.extract_document(obj=self)
        index = IndexClass.get_index()
        type_name = IndexClass.get_mapping_type_name()
        es = get_es()
        es.index(index=index, doc_type=type_name, body=document, id=self.pk)

    def remove_from_index(self):
        IndexClass = self.get_index_class()
        document = IndexClass.extract_document(obj=self)
        index = IndexClass.get_index()
        type_name = IndexClass.get_mapping_type_name()
        es = get_es()
        es.delete(index=index, doc_type=type_name, id=self.pk)

    def save(self, *args, **kwargs):
        return_val = super(LinkedBaseModel, self).save(*args, **kwargs)
        self.update_index()
        return return_val
        
    def delete(self, *args, **kwargs):
        self.remove_from_index()
        return super(LinkedBaseModel, self).delete(*args, **kwargs)

