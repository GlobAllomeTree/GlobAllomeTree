# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wood_densities', '0002_auto_20150909_1043'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wooddensity',
            old_name='Reference',
            new_name='Source',
        ),
    ]
