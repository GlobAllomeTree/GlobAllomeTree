
from rest_framework import serializers, fields

from globallometree.apps.data_sharing import models 


class DataLicenseSerializer(serializers.ModelSerializer):
    Permitted_use_text = fields.SerializerMethodField()
    def get_Permitted_use_text(self, obj):
        return obj.get_Permitted_use_text()
        
    class Meta:
        model = models.DataLicense        
        exclude = ('Created', 'Modified', 'User', 'Public_choice')


class DatasetSerializer(serializers.ModelSerializer):
    Data_license = DataLicenseSerializer(many=False, read_only=True)
    Dataset_url = fields.SerializerMethodField()
    Data_type_text = fields.CharField(
        source="get_Data_type_display",
        read_only=True
        )


    def get_Dataset_url(self, obj):
        return obj.get_absolute_url()

    def update(self, instance, validated_data):
        instance.Data_as_json = validated_data.get('Data_as_json', instance.Data_as_json)
        instance.Title = validated_data.get('Title', instance.Title)
        instance.Description = validated_data.get('Description', instance.Description)
        instance.save()
        return instance

    
    class Meta:
        model = models.Dataset
        fields = ('ID_Dataset', 'Title', 'Dataset_url', 'Description', 'User', 'Imported', 'Data_type_text', 'Record_count', 'Data_license')
        read_only_fields = ('Data_license', 'Data_type_text', 'Record_count', 'Imported', 'User')
