# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('allometric_equations', '0002_auto_20150909_1043'),
        ('wood_densities', '0002_auto_20150909_1043'),
        ('biomass_expansion_factors', '0002_auto_20150909_1043'),
        ('raw_data', '0002_auto_20150909_1043'),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TreeType',
        ),
    ]
