# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='Biome_local',
        ),
        migrations.RemoveField(
            model_name='location',
            name='Vegetation_type',
        ),
        migrations.DeleteModel(
            name='BiomeLocal',
        ),
        migrations.DeleteModel(
            name='VegetationType',
        ),
    ]
