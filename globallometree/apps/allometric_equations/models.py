import codecs
from decimal import Decimal
import difflib
from decimal import getcontext
getcontext().prec = 10
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from apps.taxonomy.models import (
    Family, Genus, Species, SpeciesGroup
)
from apps.locations.models import (
    Country, Location, LocationGroup, ZoneFAO, EcoregionUdvardy, 
    EcoregionWWF, DivisionBailey, ZoneHoldridge
)
from apps.search_helpers.models import BaseModel, LinkedBaseModel


class Population(BaseModel):
    Population_ID = models.AutoField(primary_key=True, db_column="population_id")
    Name = models.CharField(max_length=255, null=True, blank=True, db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        ordering = ('Name',)
        db_table = 'allometric_equation_population'


class TreeType(BaseModel):
    Tree_type_ID = models.AutoField(primary_key=True, db_column="tree_type_id")
    Name = models.CharField(max_length=255, null=True, blank=True, db_column="name")

    def __unicode__(self):
        return self.Name

    class Meta:
        ordering = ('Name',)
        db_table = 'allometric_equation_tree_type'


class AllometricEquation(LinkedBaseModel):
    Allometric_equation_ID = models.AutoField(primary_key=True, db_column="allometric_equation_id")
   
    U = models.CharField(max_length=20, null=True, blank=True, db_column="u")
    Unit_U = models.CharField(max_length=20, null=True, blank=True, db_column="unit_u")
    V = models.CharField(max_length=20, null=True, blank=True, db_column="v")
    Unit_V = models.CharField(max_length=20, blank=True, null=True, db_column="unit_v")
    W = models.CharField(max_length=20, null=True, blank=True, db_column="w")
    Unit_W = models.CharField(max_length=20, null=True, blank=True, db_column="unit_w")
    X = models.CharField(max_length=20, null=True, blank=True, db_column="x")
    Unit_X = models.CharField(max_length=20, null=True, blank=True, db_column="unit_x")
    Z = models.CharField(max_length=20, null=True, blank=True, db_column="z")
    Unit_Z = models.CharField(max_length=20, null=True, blank=True, db_column="unit_z")

    Min_X = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10, db_column="min_x"
    )
    Max_X = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10, db_column="max_x"
    )
    Min_Z = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10, db_column="min_z"
    )
    Max_Z = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10, db_column="max_z"
    )
    Output = models.CharField(max_length=30, null=True, db_column="output")
    Output_TR = models.CharField(max_length=30, null=True, blank=True, db_column="output_tr")
    Unit_Y = models.CharField(max_length=50, null=True, blank=True, db_column="unit_y")
    Age = models.CharField(max_length=50, null=True, blank=True, db_column="age")
    Veg_Component = models.CharField(max_length=150, null=True, blank=True, db_column="veg_component")
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
    Equation = models.CharField(max_length=500, db_column="equation") 
    Substitute_equation = models.CharField(
        max_length=500, null=True, blank=True, db_column="substitute_equation"
    ) 
    Top_dob = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10, db_column="top_dob"
    )
    Stump_height = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10, db_column="stump_height"
    )
    R2 = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10, db_column="r2"
    )
    R2_Adjusted = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10, db_column="r2_adjusted"
    )
    RMSE = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10, db_column="rmse"
    )
    SEE = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10, db_column="see"
    )
    Corrected_for_bias = models.NullBooleanField(db_column="corrected_for_bias")
    Bias_correction = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10, db_column="bias_correction"
    )
    Ratio_equation = models.NullBooleanField(db_column="ratio_equation")
    Segmented_equation = models.NullBooleanField(db_column="segmented_equation")
    Sample_size = models.CharField(max_length=150, null=True, blank=True, db_column="sample_size")

    Population = models.ForeignKey(Population, blank=True, null=True, db_column="population_id")
    Tree_type = models.ForeignKey(TreeType, blank=True, null=True, db_column="tree_type_id")

    def components_string(self):
        c_string = ''
        for field in ['B', 'Bd', 'Bg', 'Bt', 'L', 'Rb', 'Rf', 'Rm', 'S', 'T', 'F']:
            if getattr(self, field):
                c_string += field + ' '
        return c_string

    def get_absolute_url(self):
        return '/data/allometric-equations/%s' % self.ID

    def get_serializer_class(self):
        from apps.api import AllometricEquationSerializer
        return AllometricEquationSerializer

    def get_index_class(self):
        from apps.allometric_equations.indices import AllometricEquationIndex
        return AllometricEquationIndex

    def __unicode__(self):
        return u"Equation %s: %s" % (self.Allometric_equation_ID, self.Equation)

    def save(self, *args, **kwargs):
        if not self.Substitute_equation and self.Equation:
            self.Substitute_equation = self.Equation
        return super(AllometricEquation, self).save(*args, **kwargs)

    class Meta:
        verbose_name ='Allometric Equation'
        verbose_name_plural = 'Allometric Equations'
        db_table = "allometric_equation"




