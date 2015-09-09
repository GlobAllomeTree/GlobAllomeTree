# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('identification', '__first__'),
        ('allometric_equations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='allometricequation',
            name='Vegetation_type',
            field=models.ForeignKey(db_column=b'id_vegetation_type', blank=True, to='identification.VegetationType', null=True),
        ),
        migrations.AlterField(
            model_name='allometricequation',
            name='Tree_type',
            field=models.ForeignKey(db_column=b'id_tree_type', blank=True, to='identification.TreeType', null=True),
        ),
    ]
