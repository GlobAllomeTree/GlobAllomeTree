# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wood_densities', '0004_auto_20150910_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wooddensity',
            name='CV',
            field=models.DecimalField(db_column=b'cv', decimal_places=2, max_digits=8, blank=True, help_text=b'SD/Density if Density is an average', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='Max',
            field=models.DecimalField(db_column=b'max', decimal_places=2, max_digits=8, blank=True, help_text=b'Max of WD in g.cm-3', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='Min',
            field=models.DecimalField(db_column=b'min', decimal_places=2, max_digits=8, blank=True, help_text=b'Min of WD in g.cm-3', null=True),
        ),
        migrations.AlterField(
            model_name='wooddensity',
            name='SD',
            field=models.DecimalField(db_column=b'sd', decimal_places=2, max_digits=8, blank=True, help_text=b'Standard Deviation', null=True),
        ),
    ]
