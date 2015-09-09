import hashlib
import json
from django.db import models
from elasticutils.contrib.django import get_es

class BaseModel(models.Model):
    Created = models.DateTimeField(auto_now_add=True, db_column='created')
    Modified = models.DateTimeField(auto_now=True, verbose_name="Last modified", db_column='modified')

    class Meta:
        abstract = True


class ComponentBaseModel(models.Model):
    B = models.NullBooleanField(db_column="b")
    Bd = models.NullBooleanField(db_column="bd")
    Bg = models.NullBooleanField(db_column="bg")
    Bt = models.NullBooleanField(db_column="bt")
    L = models.NullBooleanField(db_column="l")
    Rb = models.NullBooleanField(db_column="rb")
    Rf = models.NullBooleanField(db_column="rf")
    Rm = models.NullBooleanField(db_column="rm")
    S = models.NullBooleanField(db_column="s")
    T = models.NullBooleanField(db_column="t")
    F = models.NullBooleanField(db_column="f")

    class Meta:
        abstract = True


class LinkedBaseModel(BaseModel):
    Species_group = models.ForeignKey(
        'taxonomy.SpeciesGroup',
        null=True, 
        blank=True,
        db_column='id_species_group')

    Location_group = models.ForeignKey(
        'locations.LocationGroup',
        null=True, 
        blank=True,
        db_column='id_location_group')

    Reference = models.ForeignKey(
        'source.Reference', 
        blank=True, 
        null=True,
        db_column='id_reference')

    Operator = models.ForeignKey(
        'source.Operator', 
        blank=True, 
        null=True,
        db_column='id_operator'
        )

    Contributor = models.ForeignKey(
        'source.Institution', 
        blank=True, 
        null=True,
        db_column='id_contributor')

    Dataset = models.ForeignKey(
        'data_sharing.Dataset',
        null=True, 
        blank=True,
        help_text="The Dataset that this raw data record came from",
        db_column="id_dataset"
        )

    Tree_type = models.ForeignKey(
        'identification.TreeType',
         blank=True,
         null=True, 
         db_column="id_tree_type"
         )

    Vegetation_type = models.ForeignKey(
        'identification.VegetationType',
         blank=True,
         null=True, 
         db_column="id_vegetation_type"
         )

    Elasticsearch_doc_hash = models.CharField(
        help_text="The hash of the denormalized version of this model in elasticsearch, used for knowing if the es index needs to be updated or not",
        blank=True,
        null=True,
        verbose_name="Elasticsearch document md5 hash",
        max_length=255,
        db_column="elasticsearch_doc_hash"
        )

    Remark = models.TextField(
        null=True, 
        blank=True
        )

    Contact = models.CharField(
        null=True, 
        blank=True, 
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
            es.create(index=index, doc_type=type_name, body=document, id=self.pk)
        else:
            es.update(index=index, doc_type=type_name, body=document, id=self.pk)

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
