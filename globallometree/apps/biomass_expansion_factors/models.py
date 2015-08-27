from decimal import getcontext
getcontext().prec = 10

from django.db import models
from django.contrib.auth.models import User

from globallometree.apps.search_helpers.models import LinkedBaseModel


class BiomassExpansionFactor(LinkedBaseModel):

    Biomass_expansion_factor_ID = models.AutoField(primary_key=True, db_column="biomass_expansion_factor_id")

    Growing_stock = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Growing stock", db_column="growing_stock")

    Aboveground_biomass = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Above ground  biomass", db_column="aboveground_biomass")

    Net_annual_increment = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Net annual increment", db_column="net_annual_increment")

    Stand_density = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Stand density", db_column="stand_density")

    Age = models.IntegerField(
        null=True, blank=True,
        help_text="Age", db_column="age"
        )

    BEF = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10,
        help_text="Biomass expansion factor", db_column="bef")

    Input = models.CharField(
        null=True, blank=True, max_length="255",
        help_text="Input", db_column="input" )

    Output = models.CharField(
        null=True, blank=True, max_length="255",
        help_text="Output", db_column="output"
        )

    Interval_validity = models.CharField(
        null=True, blank=True, max_length="255",
        help_text="Interval validity", db_column="interval_validity"
        )

    def get_serializer_class(self):
        from globallometree.apps.api import BiomassExpansionFactorSerializer
        return BiomassExpansionFactorSerializer

    def get_index_class(self):
        from globallometree.apps.biomass_expansion_factors.indices import BiomassExpansionFactorIndex
        return BiomassExpansionFactorIndex

    def get_absolute_url(self):
        return '/data/biomass_expansion_factors/%s' % self.ID

    def unicode(self):
        return 'Biomass Expansion Factors %s' % self.ID

    class Meta:
        verbose_name = 'Biomass Expansion Factors Instance'
        verbose_name_plural = 'Biomass Expansion Factors'
        db_table = "biomass_expansion_factors"
