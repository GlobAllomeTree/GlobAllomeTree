# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_auto_20150910_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='Latitude',
            field=models.DecimalField(null=True, decimal_places=9, max_digits=14, db_column=b'latitude', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='Longitude',
            field=models.DecimalField(null=True, decimal_places=9, max_digits=14, db_column=b'longitude', blank=True),
        ),
    ]
