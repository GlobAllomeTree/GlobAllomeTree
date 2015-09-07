import Geohash
from django.contrib.auth.models import User

from rest_framework import serializers, fields

from globallometree.apps.locations import models
from globallometree.apps.api.validators import ValidRelatedField

class ZoneFAOSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ZoneFAO
        fields = ('ID_Zone_FAO', 'Name',)


class EcoregionUdvardySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EcoregionUdvardy
        fields = ('ID_Ecoregion_Udvardy', 'Name',)


class EcoregionWWFSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EcoregionWWF
        fields = ('id_ecoregion_wwf', 'Name',)


class ZoneHoldridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ZoneHoldridge
        fields = ('ID_Zone_Holdridge','Name',)


class DivisionBaileySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DivisionBailey
        fields = ('ID_Division_Bailey', 'Name',)


class VegetationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VegetationType
        fields = ('ID_Vegetation_type', 'Name',)


class LocationSerializer(serializers.ModelSerializer):
 
    Location_name = fields.CharField(
        source="Name", 
        allow_null=True,
        required=False,
        max_length=255
        )

    Country = fields.CharField(
        source="Country.Formal_name", 
        allow_null=True,
        required=False,
        validators=[ValidRelatedField(model=models.Country, 
                                     field_name="Formal_name")],
        )

    Continent = fields.CharField(
        source="Country.Continent.Name", 
        read_only=True
        ) 

    Zone_FAO = fields.CharField(
        source="Zone_FAO.Name", 
        allow_null=True,
        required=False,
        validators=[ValidRelatedField(model=models.ZoneFAO, 
                                     field_name="Name")]
        )

    Ecoregion_Udvardy = fields.CharField(
        source="Ecoregion_Udvardy.Name", 
        allow_null=True,
        required=False,
        validators=[ValidRelatedField(model=models.EcoregionUdvardy, 
                                     field_name="Name")]
        )

    Ecoregion_WWF = fields.CharField(
        source="Ecoregion_WWF.Name", 
        allow_null=True,
        required=False,
        validators=[ValidRelatedField(model=models.EcoregionWWF, 
                                     field_name="Name")]
        )

    Zone_Holdridge = fields.CharField(
        source="Zone_Holdridge.Name", 
        allow_null=True,
        required=False,
        validators=[ValidRelatedField(model=models.ZoneHoldridge, 
                                     field_name="Name")]
        )

    Division_Bailey = fields.CharField(
        source="Division_Bailey.Name", 
        allow_null=True,
        required=False,
        validators=[ValidRelatedField(model=models.DivisionBailey, 
                                     field_name="Name")]
        )

    Biome_local = fields.CharField(
        source="Biome_local.Name", 
        allow_null=True,
        required=False,
        max_length=200
        )

    Biome_local_reference = fields.CharField(
        source="Biome_local.Reference", 
        allow_null=True,
        required=False,
        max_length=200
        )

    Vegetation_type = fields.CharField(
        source="Vegetation_type.Name", 
        allow_null=True,
        required=False,
        validators=[ValidRelatedField(model=models.VegetationType, 
                                     field_name="Name")]
        )

    Country_3166_3 = fields.CharField(
        source="Country.Iso3166a3", 
        allow_null=True,
        required=False,
        validators=[ValidRelatedField(model=models.Country, 
                                     field_name="Iso3166a3")]
        )

    # IDs are read only since we are not trusting them at the moment
    # They could be ids internal to a single dataset or study
    ID_Country = fields.IntegerField(
        source="Country.ID_Country", 
        read_only=True
        )

    ID_Continent = fields.IntegerField(
        source="Country.Continent.ID_Continent", 
        read_only=True
        ) 

    ID_Zone_FAO = fields.IntegerField(
        source="Zone_FAO.ID_Zone_FAO", 
        read_only=True
        )
    ID_Ecoregion_Udvardy = fields.IntegerField(
        source="Ecoregion_Udvardy.ID_Ecoregion_Udvardy", 
        read_only=True)

    id_ecoregion_wwf = fields.IntegerField(
        source="Ecoregion_WWF.id_ecoregion_wwf",
        read_only=True
        )    
    ID_Division_Bailey = fields.IntegerField(
        source="Division_Bailey.ID_Division_Bailey", 
        read_only=True
        ) 
    ID_Zone_Holdridge = fields.IntegerField(
        source="Zone_Holdridge.ID_Zone_Holdridge",
        read_only=True) 
    ID_Vegetation_type = fields.IntegerField(
        source="Vegetation_type.ID_Vegetation_type", 
        read_only=True) 

    ID_Biome_local = fields.IntegerField(
        source="Biome_local.ID_Biome_local", 
        read_only=True) 

    # Serializer fields are always read only
    Geohash = fields.SerializerMethodField()
    LatLonString = fields.SerializerMethodField()

    # Geohash and LatLonString are designed to help out with elasticsearch queries 
    def get_Geohash(self, obj):
        if obj.Latitude and obj.Longitude:
            return Geohash.encode(float(obj.Latitude), float(obj.Longitude))
        else:
            return None

    def get_LatLonString(self, obj):
        if obj.Latitude:
            lat_lon_string = "%s,%s" % (obj.Latitude, obj.Longitude)
        else:
            lat_lon_string = None  
        return lat_lon_string

    class Meta: 
        model = models.Location
        
        fields = (
            "ID_Location",
            "Location_name",
            "Plot_name",
            "Plot_size_m2",
            "Commune",
            "Province",
            "Region",
            "Country",
            "Country_3166_3",
            "Continent", 
            "Vegetation_type",
            "Zone_FAO",
            "Zone_Holdridge", 
            "Ecoregion_Udvardy", 
            "Ecoregion_WWF",
            "Division_Bailey",
            "Biome_local",
            "Biome_local_reference",
            "Geohash", 
            "Latitude",
            "Longitude",
            "LatLonString",
            "ID_Vegetation_type",
            "ID_Zone_FAO",
            "ID_Ecoregion_Udvardy",
            "ID_Zone_Holdridge", 
            "id_ecoregion_wwf",
            "ID_Division_Bailey", 
            "ID_Country",
            "ID_Continent",
            "ID_Biome_local",
            )


class LocationGroupSerializer(serializers.ModelSerializer):

    Group = LocationSerializer(many=True, source="Locations")
    ID_Location_group = fields.IntegerField()

    class Meta:
        model = models.LocationGroup
        fields = ('ID_Location_group', 'Group',)

     
class ContinentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Continent
        fields = ('Name',)


class CountrySerializer(serializers.ModelSerializer):
    Name = fields.CharField(source='Formal_name')
    Code = fields.CharField(source='Iso3166a3')
    Continent = fields.CharField(source="Continent.Name")
    class Meta:
        model = models.Country
        fields = ('ID_Country', 'Name', 'Code', 'Continent')   
