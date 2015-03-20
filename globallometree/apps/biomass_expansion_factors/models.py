from decimal import getcontext
getcontext().prec = 10

from django.db import models
from django.contrib.auth.models import User

from globallometree.apps.common.models import LinkedBaseModel


class BiomassExpansionFactor(LinkedBaseModel):

    ID_BEF = models.AutoField(primary_key=True)

    Growing_stock = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Growing stock")

    Aboveground_biomass = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Above ground  biomass")

    Net_annual_increment = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Net annual increment")

    Stand_density = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Stand density")

    Age = models.IntegerField(
        null=True, blank=True,
        help_text="Age"
        )

    BEF = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Biomass expansion factor")

    Input = models.CharField(
        null=True, blank=True, max_length="255",
        help_text="Input" )

    Output = models.IntegerField(
        null=True, blank=True,
        help_text="Output"
        )

    Interval_validity = models.IntegerField(
        null=True, blank=True,
        help_text="Interval validity"
        )

    def get_absolute_url(self):
        return '/data/biomass_expansion_factors/%s' % self.ID

    def unicode(self):
        return 'Biomass Expansion Factors %s' % self.ID

    class Meta:
        verbose_name = 'Biomass Expansion Factors Instance'
        verbose_name_plural = 'Biomass Expansion Factors'
        db_table = "biomass_expansion_factors"
