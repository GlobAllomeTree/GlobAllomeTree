import codecs
from decimal import Decimal
import difflib
from decimal import getcontext
getcontext().prec = 10
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from globallometree.apps.taxonomy.models import (
    Family, Genus, Species, SpeciesGroup
)
from globallometree.apps.locations.models import (
    Country, Location, LocationGroup, BiomeFAO, BiomeUdvardy, 
    BiomeWWF, DivisionBailey, BiomeHoldridge
)
from globallometree.apps.search_helpers.models import BaseModel, LinkedBaseModel


class Population(BaseModel):
    Population_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.Name

    class Meta:
        ordering = ('Name',)
        db_table = 'Population'


class TreeType(BaseModel):
    Tree_type_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.Name

    class Meta:
        ordering = ('Name',)
        db_table = 'Tree_type'


class AllometricEquation(LinkedBaseModel):
    Allometric_equation_ID = models.AutoField(primary_key=True)
    Allometric_equation_ID_original = models.IntegerField(blank=True, null=True)
   
    U = models.CharField(max_length=20, null=True, blank=True)
    Unit_U = models.CharField(max_length=20, null=True, blank=True)
    V = models.CharField(max_length=20, null=True, blank=True)
    Unit_V = models.CharField(max_length=20, blank=True)
    W = models.CharField(max_length=20, null=True, blank=True)
    Unit_W = models.CharField(max_length=20, null=True, blank=True)
    X = models.CharField(max_length=20, null=True, blank=True)
    Unit_X = models.CharField(max_length=20, null=True, blank=True)
    Z = models.CharField(max_length=20, null=True, blank=True)
    Unit_Z = models.CharField(max_length=20, null=True, blank=True)

    Min_X = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    Max_X = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    Min_Z = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    Max_Z = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    Output = models.CharField(max_length=30, null=True)
    Output_TR = models.CharField(max_length=30, null=True, blank=True)
    Unit_Y = models.CharField(max_length=50, null=True, blank=True)
    Age = models.CharField(max_length=50, null=True, blank=True)
    Veg_Component = models.CharField(max_length=150, null=True, blank=True)
    B = models.NullBooleanField()
    Bd = models.NullBooleanField()
    Bg = models.NullBooleanField()
    Bt = models.NullBooleanField()
    L = models.NullBooleanField()
    Rb = models.NullBooleanField()
    Rf = models.NullBooleanField()
    Rm = models.NullBooleanField()
    S = models.NullBooleanField()
    T = models.NullBooleanField()
    F = models.NullBooleanField()
    Equation = models.CharField(max_length=500) 
    Substitute_equation = models.CharField(
        max_length=500, null=True, blank=True
    ) 
    Top_dob = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    Stump_height = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    R2 = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    R2_Adjusted = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    RMSE = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    SEE = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    Corrected_for_bias = models.NullBooleanField()
    Bias_correction = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    Ratio_equation = models.NullBooleanField()
    Segmented_equation = models.NullBooleanField()
    Sample_size = models.CharField(max_length=150, null=True, blank=True)

    Population = models.ForeignKey(Population, blank=True, null=True, db_column="Population_ID")
    Tree_type = models.ForeignKey(TreeType, blank=True, null=True, db_column="Tree_type_ID")

    def components_string(self):
        c_string = ''
        for field in ['B', 'Bd', 'Bg', 'Bt', 'L', 'Rb', 'Rf', 'Rm', 'S', 'T', 'F']:
            if getattr(self, field):
                c_string += field + ' '
        return c_string

    def get_absolute_url(self):
        return '/data/allometric-equations/%s' % self.ID

    def get_serializer_class(self):
        from globallometree.apps.api import AllometricEquationSerializer
        return AllometricEquationSerializer

    def get_index_class(self):
        from globallometree.apps.allometric_equations.indices import AllometricEquationIndex
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
        db_table = "Allometric_equation"




