
from decimal import getcontext
getcontext().prec = 10

from django.db import models
from django.contrib.auth.models import User

from globallometree.apps.common.models import LinkedBaseModel


class WoodDensity(LinkedBaseModel):

    Wood_density_ID = models.AutoField(primary_key=True)

    H_tree_avg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Average height of tree measured")

    H_tree_min = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Min of trees' height measured if several trees where sampled")

    H_tree_max = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Max of trees' height measured if several trees where sampled")

    DBH_tree_avg = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Average DBH of tree measured")

    DBH_tree_min = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Min of trees' DBH measured if several trees where sampled")

    DBH_tree_max = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Max of trees' DBH measured if several trees where sampled")

    m_WD = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Wood mass measured")

    MC_m = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Moisture content of the wood during measurement, ex: (%) 0, 12, 15, Sat for saturation")

    V_WD = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Wood volume measured")

    MC_V= models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Moisture content of the wood during measurement, ex: (%) 0, 12, 15, Sat for saturation")

    CR = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Coefficient of retraction (%/%)")

    FSP = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Fiber saturation point (%)")

    Methodology = models.CharField(
        blank=True, null=True, max_length=80,
        help_text="Water displacment or direct measurement")

    Bark = models.NullBooleanField(
        blank=True, null=True,
        help_text="is the bark included in the measure?")

    Density_g_cm3 = models.DecimalField(
        null=True, max_digits=16, decimal_places=10,
        help_text="density of the wood in g/cm3")

    MC_Density = models.CharField(
        blank=True, null=True, max_length=80,  
        help_text="Moisture content, with code for specific cases, ex: (%) 0, 12, 15, BD for Basic density")

    Data_origin = models.CharField(
        blank=True, null=True, max_length=80,
        help_text="Calculated or  entered from biblio")

    Data_type = models.CharField(
        blank=True, null=True, max_length=80,  
        help_text="Unique value, average of data, average of min max")
    
    Samples_per_tree = models.IntegerField(
        blank=True, null=True,
        help_text="Number of samples per tree")

    Number_of_trees = models.IntegerField(
        blank=True, null=True,
        help_text="Number of trees")

    SD = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Standard Deviation")

    Min = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Min of WD in g.cm-3")

    Max = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Max of WD in g.cm-3")

    H_measure = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Height where WD sample was collected")

    Bark_distance = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Distance where the WD was collected")


    #Formulas
    #Convert BD  Formula decimal 0.861*Density if density is at 10 to 18%  IF(BB2="BD",ROUND(BA2,3),IF(0.1<=BB2,IF(BB2<=0.18,ROUND(BA2*0.861,3),"NA"),"NA"))
    #CV Formula SD/Density if Density is an average Formula: IF(BH2="NA","NA",BH2/BA2)


    def get_absolute_url(self):
        return '/data/wood_densities/%s' % self.ID

    def unicode(self):
        return 'Wood Density %s' % self.ID

    class Meta:
        verbose_name = 'Wood Density'
        verbose_name_plural = 'Wood Densities'
        db_table = "Wood_density"
