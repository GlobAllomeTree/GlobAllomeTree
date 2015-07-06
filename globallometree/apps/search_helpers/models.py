import hashlib
import json
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

    Elasticsearch_doc_hash = models.CharField(
        help_text="The hash of the denormalized version of this model in elasticsearch, used for knowing if the es index needs to be updated or not",
        blank=True,
        null=True,
        verbose_name="Elasticsearhch document md5 hash",
        max_length=255
        )

    class Meta:
        abstract = True

    def serialize(self, request=None):
        SerializerClass = self.get_serializer_class()
        context = {}
        if request:
            context['request'] = request
        serialized_data = SerializerClass(self, context=context).data
        return serialized_data 

    
    def update_index(self, add=True, document=None):
        IndexClass = self.get_index_class()
        if document is None:
            document = IndexClass.extract_document(obj=self)
        index = IndexClass.get_index()
        type_name = IndexClass.get_mapping_type_name()
        es = get_es()
        if add:
            es.create(index=index, doc_type=type_name, body={'doc':document}, id=self.pk)
        else:
            es.update(index=index, doc_type=type_name, body={'doc':document}, id=self.pk)

        self.update_elasticsearch_doc_hash(document)

    def update_elasticsearch_doc_hash(self, document):
        new_hash = hashlib.md5(json.dumps(document)).hexdigest()
        if new_hash != self.Elasticsearch_doc_hash:
            self.Elasticsearch_doc_hash = new_hash
            self.save()


    def remove_from_index(self):
        IndexClass = self.get_index_class()
        document = IndexClass.extract_document(obj=self)
        index = IndexClass.get_index()
        type_name = IndexClass.get_mapping_type_name()
        es = get_es()
        es.delete(index=index, doc_type=type_name, id=self.pk)
