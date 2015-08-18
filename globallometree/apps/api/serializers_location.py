import Geohash
from django.contrib.auth.models import User

from rest_framework import serializers, fields

from globallometree.apps.locations import models
from .validators import ValidRelatedField

class ZoneFAOSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ZoneFAO
        fields = ('Zone_FAO_ID', 'Name',)


class EcoregionUdvardySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EcoregionUdvardy
        fields = ('Ecoregion_Udvardy_ID', 'Name',)


class EcoregionWWFSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EcoregionWWF
        fields = ('Ecoregion_WWF_ID', 'Name',)


class ZoneHoldridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ZoneHoldridge
        fields = ('Zone_Holdridge_ID','Name',)


class DivisionBaileySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DivisionBailey
        fields = ('Division_BAILEY_ID', 'Name',)


class ForestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForestType
        fields = ('Forest_type_ID', 'Name',)


class LocationSerializer(serializers.ModelSerializer):
 
    Location_name = fields.CharField(
        source="Name", 
        allow_null=True,
        required=False
        )

    Country = fields.CharField(
        source="Country.Formal_name", 
        allow_null=True,
        required=False,
        validators=[ValidRelatedField(model=models.Country, 
                                     field_name="Formal_name")]
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

    Division_BAILEY = fields.CharField(
        source="Division_BAILEY.Name", 
        allow_null=True,
        required=False,
        validators=[ValidRelatedField(model=models.DivisionBailey, 
                                     field_name="Name")]
        )

    Forest_type = fields.CharField(
        source="Forest_type.Name", 
        allow_null=True,
        required=False,
        validators=[ValidRelatedField(model=models.ForestType, 
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
    Country_ID = fields.IntegerField(
        source="Country.Country_ID", 
        read_only=True
        )

    Continent_ID = fields.IntegerField(
        source="Country.Continent.Continent_ID", 
        read_only=True
        ) 

    Zone_FAO_ID = fields.IntegerField(
        source="Zone_FAO.Zone_FAO_ID", 
        read_only=True
        )
    Ecoregion_Udvardy_ID = fields.IntegerField(
        source="Ecoregion_Udvardy.Ecoregion_Udvardy_ID", 
        read_only=True)

    Ecoregion_WWF_ID = fields.IntegerField(
        source="Ecoregion_WWF.Ecoregion_WWF_ID",
        read_only=True
        )    
    Division_BAILEY_ID = fields.IntegerField(
        source="Division_BAILEY.Division_BAILEY_ID", 
        read_only=True
        ) 
    Zone_Holdridge_ID = fields.IntegerField(
        source="Zone_Holdridge.Zone_Holdridge_ID",
        read_only=True) 
    Forest_type_ID = fields.IntegerField(
        source="Forest_type.Forest_type_ID", 
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
            "Location_ID",
            "Location_name",
            "Plot_name",
            "Plot_size_m2",
            "Commune",
            "Province",
            "Region",
            "Country",
            "Country_3166_3",
            "Continent", 
            "Zone_FAO",
            "Zone_Holdridge", 
            "Ecoregion_Udvardy", 
            "Ecoregion_WWF",
            "Division_BAILEY",
            "Forest_type",
            "Geohash", 
            "Latitude",
            "Longitude",
            "LatLonString",
            "Zone_FAO_ID",
            "Ecoregion_Udvardy_ID",
            "Zone_Holdridge_ID", 
            "Ecoregion_WWF_ID",
            "Division_BAILEY_ID", 
            "Country_ID",
            "Continent_ID",
            "Forest_type_ID",
            )


class LocationGroupSerializer(serializers.ModelSerializer):

    Group = LocationSerializer(many=True, source="Locations")
    Location_group_ID = fields.IntegerField()

    class Meta:
        model = models.LocationGroup
        fields = ('Location_group_ID', 'Group',)

     
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
        fields = ('Country_ID', 'Name', 'Code', 'Continent')   
