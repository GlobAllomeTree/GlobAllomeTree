
from decimal import getcontext
getcontext().prec = 10

from django.db import models
from django.contrib.auth.models import User

from globallometree.apps.base.models import LinkedBaseModel


class WoodDensity(LinkedBaseModel):

    ID_WD = models.AutoField(primary_key=True, db_column="id_wd")

    H_tree_avg = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=3,
        help_text="Average height of tree measured",
        db_column="h_tree_avg")

    H_tree_min = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=3,
        help_text="Min of trees' height measured if several trees where sampled",
        db_column="h_tree_min")

    H_tree_max = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=3,
        help_text="Max of trees' height measured if several trees where sampled",
        db_column="h_tree_max")

    DBH_tree_avg = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=3,
        help_text="Average DBH of tree measured",
        db_column="dbh_tree_avg")

    DBH_tree_min = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=3,
        help_text="Min of trees' DBH measured if several trees where sampled",
        db_column="dbh_tree_min")

    DBH_tree_max = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=3,
        help_text="Max of trees' DBH measured if several trees where sampled",
        db_column="dbh_tree_max")

    m_WD = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=3,
        help_text="Wood mass measured",
        db_column="m_wd")

    MC_m = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=3,
        help_text="Moisture content of the wood during measurement, ex: (%) 0, 12, 15, Sat for saturation",
        db_column="mc_m")

    V_WD = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=3,
        help_text="Wood volume measured",
        db_column="v_md")

    MC_V= models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=3,
        help_text="Moisture content of the wood during measurement, ex: (%) 0, 12, 15, Sat for saturation",
        db_column="mc_v")

    CR = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=3,
        help_text="Coefficient of retraction (%/%)",
        db_column="cr")

    FSP = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=3,
        help_text="Fiber saturation point (%)",
        db_column="fsp")

    Methodology = models.CharField(
        blank=True, null=True, max_length=80,
        help_text="Water displacment or direct measurement",
        db_column="methodology")

    Bark = models.NullBooleanField(
        blank=True, null=True,
        help_text="is the bark included in the measure?",
        db_column="bark")

    Density_g_cm3 = models.DecimalField(
        null=True, max_digits=16, decimal_places=10,
        help_text="density of the wood in g/cm3",
        db_column="densiy_g_cm3")

    MC_Density = models.CharField(
        blank=True, null=True, max_length=80,  
        help_text="Moisture content, with code for specific cases, ex: (%) 0, 12, 15, BD for Basic density",
        db_column="mc_density")

    Data_origin = models.CharField(
        blank=True, null=True, max_length=80,
        help_text="Calculated or  entered from biblio",
        db_column="data_origin")

    Data_type = models.CharField(
        blank=True, null=True, max_length=80,  
        help_text="Unique value, average of data, average of min max",
        db_column="data_type")
    
    Samples_per_tree = models.IntegerField(
        blank=True, null=True,
        help_text="Number of samples per tree",
        db_column="samples_per_tree")

    Number_of_trees = models.IntegerField(
        blank=True, null=True,
        help_text="Number of trees",
        db_column="number_of_trees")

    SD = models.DecimalField(
        null=True, blank=True, max_digits=8, decimal_places=2,
        help_text="Standard Deviation",
        db_column="sd")

    Min = models.DecimalField(
        null=True, blank=True, max_digits=8, decimal_places=2,
        help_text="Min of WD in g.cm-3",
        db_column="min")

    Max = models.DecimalField(
        null=True, blank=True, max_digits=8, decimal_places=2,
        help_text="Max of WD in g.cm-3",
        db_column="max")

    H_measure = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=3,
        help_text="Height where WD sample was collected",
        db_column="h_measure")

    Bark_distance = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=3,
        help_text="Distance where the WD was collected",
        db_column="bark_distance")


    Convert_BD = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=5,
        help_text="0.861*Density if density is at 10 to 18%",
        db_column="convert_bd")

    CV = models.DecimalField(
        null=True, blank=True, max_digits=8, decimal_places=2,
        help_text="SD/Density if Density is an average",
        db_column="cv")

    #Formulas
    #Convert BD  Formula decimal 0.861*Density if density is at 10 to 18%  IF(BB2="BD",ROUND(BA2,3),IF(0.1<=BB2,IF(BB2<=0.18,ROUND(BA2*0.861,3),"NA"),"NA"))
    #CV Formula SD/Density if Density is an average Formula: IF(BH2="NA","NA",BH2/BA2)

    def get_serializer_class(self):
        from globallometree.apps.api import WoodDensitySerializer
        return WoodDensitySerializer

    def get_index_class(self):
        from globallometree.apps.wood_densities.indices import WoodDensityIndex
        return WoodDensityIndex

    def get_absolute_url(self):
        return '/data/wood_densities/%s' % self.ID_WD

    def __unicode__(self):
        return 'Wood Density %s' % self.ID_WD

    class Meta:
        verbose_name = 'Wood Density'
        verbose_name_plural = 'Wood Densities'
        db_table = "wood_density"
