
from rest_framework import serializers, fields
from globallometree.apps.identification import models
from globallometree.apps.api.validators import ValidRelatedField


class VegetationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VegetationType
        fields = ('ID_Vegetation_type', 'Name',)


class TreeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TreeType
        fields = ('ID_Tree_type', 'Name',)
