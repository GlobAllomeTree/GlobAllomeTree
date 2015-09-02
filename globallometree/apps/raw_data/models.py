from decimal import getcontext
getcontext().prec = 10

from django.db import models
from django.contrib.auth.models import User

from globallometree.apps.search_helpers.models import LinkedBaseModel, ComponentBaseModel


class RawData(LinkedBaseModel, ComponentBaseModel):

    Raw_data_ID = models.AutoField(primary_key=True, db_column="raw_data_id")


    DBH_cm = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Diameter at breast height of the tree in centimeters",
        db_column="dbh_cm")

    H_m = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Total height of the tree in meters",
        db_column="h_m")

    CD_m = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Crown diameter of the tree in meters",
        db_column="cd_m")

    F_Bole_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Fresh weight of the bole in kg",
        db_column="f_bole_kg")

    F_Branch_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Fresh weight of the branches in kg",
        db_column="f_branch_kg")

    F_Foliage_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Fresh weight of the foliage in kg",
        db_column="f_foliage_kg")

    F_Stump_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Fresh weight of the stump in kg",
        db_column="f_stump_kg")

    F_Buttress_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Fresh weight of the buttress in kg",
        db_column="f_buttress_kg")

    F_Roots_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Fresh weight of the roots in kg",
        db_column="f_roots_kg")

    Volume_m3 = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Total volume of the tree in cubic meters",
        db_column="volume_m3")

    Volume_bole_m3 = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Volume of the bole in cubic meters",
        db_column="volume_bole_m3")

    WD_AVG_gcm3 = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Average wood density value for the whole tree in grams/cubic centimeters",
        db_column="wd_avg_gcm3")

    D_Bole_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Dry weight of the bole in kg",
        db_column="d_bole_kg")

    D_Branch_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Dry weight of the branches in kg",
        db_column="d_branch_kg")

    D_Foliage_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Dry weight of the foliage in kg",
        db_column="d_foliage_kg")

    D_Stump_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Dry weight of the stump in kg",
        db_column="d_stump_kg")

    D_Buttress_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Dry weight of the buttress in kg",
        db_column="d_buttress_kg")

    D_Roots_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Dry weight of the buttress in kg",
        db_column="d_roots_kg")

    ABG_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Total aboveground biomass in kg",
        db_column="abg_kg")

    BGB_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Total belowground biomass in kg",
        db_column="bgb_kg")

    Tot_Biomass_kg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Total biomass of the tree in kg (aboveground + belowground)",
        db_column="tot_biomass_kg")

    Remark = models.TextField(
        null=True, blank=True)

    Contact = models.CharField(
        null=True, blank=True, max_length=255)

    def get_serializer_class(self):
        from globallometree.apps.api import RawDataSerializer
        return RawDataSerializer

    def get_index_class(self):
        from globallometree.apps.raw_data.indices import RawDataIndex
        return RawDataIndex

    def get_absolute_url(self):
        return '/data/raw_data/%s' % self.ID

    def unicode(self):
        return 'Raw Data Instance %s' % self.ID

    class Meta:
        verbose_name = 'Raw Data Instance'
        verbose_name_plural = 'Raw Data'
        db_table = "raw_data"
