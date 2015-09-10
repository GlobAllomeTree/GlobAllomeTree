# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wood_densities', '0003_auto_20150910_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wooddensity',
            name='Bark_distance',
            field=models.DecimalField(db_column=b'bark_distance', decimal_places=3, max_digits=10, blank=True, help_text=b'Distance where the WD was collected', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='CR',
            field=models.DecimalField(db_column=b'cr', decimal_places=3, max_digits=10, blank=True, help_text=b'Coefficient of retraction (%/%)', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='CV',
            field=models.DecimalField(db_column=b'cv', decimal_places=5, max_digits=10, blank=True, help_text=b'SD/Density if Density is an average', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='Convert_BD',
            field=models.DecimalField(db_column=b'convert_bd', decimal_places=5, max_digits=10, blank=True, help_text=b'0.861*Density if density is at 10 to 18%', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='DBH_tree_avg',
            field=models.DecimalField(db_column=b'dbh_tree_avg', decimal_places=3, max_digits=10, blank=True, help_text=b'Average DBH of tree measured', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='DBH_tree_max',
            field=models.DecimalField(db_column=b'dbh_tree_max', decimal_places=3, max_digits=10, blank=True, help_text=b"Max of trees' DBH measured if several trees where sampled", null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='DBH_tree_min',
            field=models.DecimalField(db_column=b'dbh_tree_min', decimal_places=3, max_digits=10, blank=True, help_text=b"Min of trees' DBH measured if several trees where sampled", null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='FSP',
            field=models.DecimalField(db_column=b'fsp', decimal_places=3, max_digits=10, blank=True, help_text=b'Fiber saturation point (%)', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='H_measure',
            field=models.DecimalField(db_column=b'h_measure', decimal_places=3, max_digits=10, blank=True, help_text=b'Height where WD sample was collected', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='H_tree_avg',
            field=models.DecimalField(db_column=b'h_tree_avg', decimal_places=3, max_digits=10, blank=True, help_text=b'Average height of tree measured', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='H_tree_max',
            field=models.DecimalField(db_column=b'h_tree_max', decimal_places=3, max_digits=10, blank=True, help_text=b"Max of trees' height measured if several trees where sampled", null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='H_tree_min',
            field=models.DecimalField(db_column=b'h_tree_min', decimal_places=3, max_digits=10, blank=True, help_text=b"Min of trees' height measured if several trees where sampled", null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='MC_V',
            field=models.DecimalField(db_column=b'mc_v', decimal_places=3, max_digits=10, blank=True, help_text=b'Moisture content of the wood during measurement, ex: (%) 0, 12, 15, Sat for saturation', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='MC_m',
            field=models.DecimalField(db_column=b'mc_m', decimal_places=3, max_digits=10, blank=True, help_text=b'Moisture content of the wood during measurement, ex: (%) 0, 12, 15, Sat for saturation', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='Max',
            field=models.DecimalField(db_column=b'max', decimal_places=3, max_digits=10, blank=True, help_text=b'Max of WD in g.cm-3', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='Min',
            field=models.DecimalField(db_column=b'min', decimal_places=3, max_digits=10, blank=True, help_text=b'Min of WD in g.cm-3', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='SD',
            field=models.DecimalField(db_column=b'sd', decimal_places=3, max_digits=10, blank=True, help_text=b'Standard Deviation', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='V_WD',
            field=models.DecimalField(db_column=b'v_md', decimal_places=3, max_digits=10, blank=True, help_text=b'Wood volume measured', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='m_WD',
            field=models.DecimalField(db_column=b'm_wd', decimal_places=3, max_digits=10, blank=True, help_text=b'Wood mass measured', null=True),
        ),
    ]
