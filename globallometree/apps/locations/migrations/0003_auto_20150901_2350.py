# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20150901_2015'),
    ]

    operations = [
        migrations.CreateModel(
            name='VegetationType',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Vegetation_type_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'vegetation_type_id')),
                ('Name', models.CharField(max_length=255, null=True, db_column=b'name', blank=True)),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'locations_vegetation_type',
            },
        ),
        migrations.RemoveField(
            model_name='location',
            name='Forest_type',
        ),
        migrations.DeleteModel(
            name='ForestType',
        ),
        migrations.AddField(
            model_name='location',
            name='Vegetation_type',
            field=models.ForeignKey(db_column=b'vegetation_type_id', blank=True, to='locations.VegetationType', null=True),
        ),
    ]
