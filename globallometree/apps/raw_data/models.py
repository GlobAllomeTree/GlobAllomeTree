from decimal import getcontext
getcontext().prec = 10

from django.db import models
from django.contrib.auth.models import User

from globallometree.apps.search_helpers.models import LinkedBaseModel


class RawData(LinkedBaseModel):

    Raw_data_ID = models.AutoField(primary_key=True)

    H_tree_avg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Average height of tree measured")

    Forest_type = models.CharField(
        null=True, blank=True, max_length="255",
        help_text="Description of the forest type where the data have been collected" )

    Tree_ID = models.IntegerField(
        null=True, blank=True,
        help_text="Identification number of the tree from which data were collected"
        )

    Date_collection = models.DateField(
        null=True, blank=True,
        help_text="Date of the data collection")

    DBH_cm = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Diameter at breast height of the tree in centimeters")

    H_m = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Total height of the tree in meters")

    CD_m = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Crown diameter of the tree in meters")

    F_Bole_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Fresh weight of the bole in kg")

    F_Branch_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Fresh weight of the branches in kg")

    F_Foliage_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Fresh weight of the foliage in kg")

    F_Stump_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Fresh weight of the stump in kg")

    F_Buttress_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Fresh weight of the buttress in kg")

    F_Roots_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Fresh weight of the roots in kg")

    Volume_m3 = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Total volume of the tree in cubic meters")

    Volume_bole_m3 = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Volume of the bole in cubic meters")

    WD_AVG_gcm3 = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Average wood density value for the whole tree in grams/cubic centimeters")

    DF_Bole_AVG = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Average ratio between dry and fresh weight of the bole")

    DF_Branch_AVG = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Average ratio between dry and fresh weight of the branches")

    DF_Foliage_AVG = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Average ratio between dry and fresh weight of the foliage")

    DF_Stump_AVG = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Average ratio between dry and fresh  weight of the stump")

    DF_Buttress_AVG = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Average ratio between dry and fresh  weight of the buttress")

    DF_Roots_AVG = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Average ratio between dry and fresh weight of the roots")

    D_Bole_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Dry weight of the bole in kg")

    D_Branch_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Dry weight of the branches in kg")

    D_Foliage_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Dry weight of the foliage in kg")

    D_Stump_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Dry weight of the stump in kg")

    D_Buttress_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Dry weight of the buttress in kg")

    D_Roots_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Dry weight of the buttress in kg")

    ABG_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Total aboveground biomass in kg")

    BGB_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Total belowground biomass in kg")

    Tot_Biomass_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Total biomass of the tree in kg (aboveground + belowground)")

    BEF = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Biomass expansion factor")

    def get_serializer_class(self):
        from globallometree.apps.api import RawDataSerializer
        return RawDataSerializer

    def get_index_class(self):
        from globallometree.apps.raw_data.indices import RawDataIndex
        return RawDataIndex

    def get_absolute_url(self):
        return '/data/raw_data/%s' % self.ID

    def unicode(self):
        return 'Raw Data %s' % self.ID

    class Meta:
        verbose_name = 'Raw Data Instance'
        verbose_name_plural = 'Raw Data'
        db_table = "Raw_data"
