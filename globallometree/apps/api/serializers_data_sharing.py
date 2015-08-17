
from rest_framework import serializers, fields

from apps.data_sharing import models 


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

    def __init__(self, *args, **kwargs):
        if 'exclude_json' in kwargs.keys():
            self.exclude_json = kwargs.pop('exclude_json')
        else:
            self.exclude_json = False
        return super(DatasetSerializer, self).__init__(*args, **kwargs)

    def get_Dataset_url(self, obj):
        return obj.get_absolute_url()

    def update(self, instance, validated_data):
        instance.Data_as_json = validated_data.get('Data_as_json', instance.Data_as_json)
        instance.Title = validated_data.get('Title', instance.Title)
        instance.Description = validated_data.get('Description', instance.Description)
        instance.save()
        return instance

    def to_representation(self, obj):
        try:
            if (not self.context['request'].user.is_superuser) and (self.context['request'].user != obj.User):
                obj.Data_as_json = None
        except:
            obj.Data_as_json = None

        if self.exclude_json:
            obj.Data_as_json = None

        return super(DatasetSerializer, self).to_representation(obj)
    
    class Meta:
        model = models.Dataset
        exclude = ('Created', 'Modified', 'User', 'Uploaded_dataset_file', 'Imported')
        read_only_fields = ('Data_license', 'Data_type_text', 'Record_count', 'Imported')
