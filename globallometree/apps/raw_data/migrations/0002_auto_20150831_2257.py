# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raw_data', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rawdata',
            name='BEF',
        ),
        migrations.RemoveField(
            model_name='rawdata',
            name='DF_Bole_AVG',
        ),
        migrations.RemoveField(
            model_name='rawdata',
            name='DF_Branch_AVG',
        ),
        migrations.RemoveField(
            model_name='rawdata',
            name='DF_Buttress_AVG',
        ),
        migrations.RemoveField(
            model_name='rawdata',
            name='DF_Foliage_AVG',
        ),
        migrations.RemoveField(
            model_name='rawdata',
            name='DF_Roots_AVG',
        ),
        migrations.RemoveField(
            model_name='rawdata',
            name='DF_Stump_AVG',
        ),
        migrations.RemoveField(
            model_name='rawdata',
            name='Date_collection',
        ),
        migrations.RemoveField(
            model_name='rawdata',
            name='H_tree_avg',
        ),
        migrations.RemoveField(
            model_name='rawdata',
            name='Tree_ID',
        ),
        migrations.AddField(
            model_name='rawdata',
            name='B',
            field=models.NullBooleanField(db_column=b'b'),
        ),
        migrations.AddField(
            model_name='rawdata',
            name='Bd',
            field=models.NullBooleanField(db_column=b'bd'),
        ),
        migrations.AddField(
            model_name='rawdata',
            name='Bg',
            field=models.NullBooleanField(db_column=b'bg'),
        ),
        migrations.AddField(
            model_name='rawdata',
            name='Bt',
            field=models.NullBooleanField(db_column=b'bt'),
        ),
        migrations.AddField(
            model_name='rawdata',
            name='Contact',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='rawdata',
            name='F',
            field=models.NullBooleanField(db_column=b'f'),
        ),
        migrations.AddField(
            model_name='rawdata',
            name='L',
            field=models.NullBooleanField(db_column=b'l'),
        ),
        migrations.AddField(
            model_name='rawdata',
            name='Rb',
            field=models.NullBooleanField(db_column=b'rb'),
        ),
        migrations.AddField(
            model_name='rawdata',
            name='Remark',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='rawdata',
            name='Rf',
            field=models.NullBooleanField(db_column=b'rf'),
        ),
        migrations.AddField(
            model_name='rawdata',
            name='Rm',
            field=models.NullBooleanField(db_column=b'rm'),
        ),
        migrations.AddField(
            model_name='rawdata',
            name='S',
            field=models.NullBooleanField(db_column=b's'),
        ),
        migrations.AddField(
            model_name='rawdata',
            name='T',
            field=models.NullBooleanField(db_column=b't'),
        ),
    ]
