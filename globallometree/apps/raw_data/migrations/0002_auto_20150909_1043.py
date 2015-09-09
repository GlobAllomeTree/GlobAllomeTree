# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('identification', '__first__'),
        ('raw_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawdata',
            name='Vegetation_type',
            field=models.ForeignKey(db_column=b'id_vegetation_type', blank=True, to='identification.VegetationType', null=True),
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='Tree_type',
            field=models.ForeignKey(db_column=b'id_tree_type', blank=True, to='identification.TreeType', null=True),
        ),
    ]
