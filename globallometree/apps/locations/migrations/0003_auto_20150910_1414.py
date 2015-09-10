# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20150909_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='Latitude',
            field=models.DecimalField(null=True, decimal_places=5, max_digits=8, db_column=b'latitude', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='Longitude',
            field=models.DecimalField(null=True, decimal_places=5, max_digits=8, db_column=b'longitude', blank=True),
        ),
    ]
