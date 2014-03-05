from django.db import models
from django.contrib.auth.models import User
from globallometree.apps.common.models import DataReference, Institution


class WoodDensity(models.Model):
    ID = models.IntegerField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, verbose_name="Last modified")

    prop_1 = models.CharField(max_length=255, verbose_name='Wood Density Property 1')
    prop_2 = models.CharField(max_length=255, verbose_name='Wood Density Property 2')
    prop_etc = models.CharField(max_length=255, verbose_name='Wood Density Properties Etc...')

    species_group = models.ForeignKey('taxonomy.SpeciesGroup',null=True, blank=True)
    location_group = models.ForeignKey('locations.LocationGroup',null=True, blank=True)

    reference = models.ForeignKey(
        DataReference, blank=True, null=True
    )

    contributor = models.ForeignKey(
        Institution, blank=True, null=True
    )

    Name_operator = models.CharField(max_length=150, null=True, blank=True)

    def get_absolute_url(self):
        return '/data/wood_density/%s' % self.ID

    def unicode(self):
        return 'Wood Density %s' % self.ID

    class Meta:
        verbose_name = 'Wood Density'
        verbose_name_plural = 'Wood Densities'
