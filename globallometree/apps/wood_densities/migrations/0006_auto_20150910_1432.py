# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wood_densities', '0005_auto_20150910_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wooddensity',
            name='CV',
            field=models.DecimalField(db_column=b'cv', decimal_places=3, max_digits=8, blank=True, help_text=b'SD/Density if Density is an average', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='Convert_BD',
            field=models.DecimalField(db_column=b'convert_bd', decimal_places=3, max_digits=10, blank=True, help_text=b'0.861*Density if density is at 10 to 18%', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='Max',
            field=models.DecimalField(db_column=b'max', decimal_places=3, max_digits=8, blank=True, help_text=b'Max of WD in g.cm-3', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='Min',
            field=models.DecimalField(db_column=b'min', decimal_places=3, max_digits=8, blank=True, help_text=b'Min of WD in g.cm-3', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='SD',
            field=models.DecimalField(db_column=b'sd', decimal_places=3, max_digits=8, blank=True, help_text=b'Standard Deviation', null=True),
        ),
    ]
