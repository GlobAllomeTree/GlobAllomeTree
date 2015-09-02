# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='divisionbailey',
            old_name='Division_BAILEY_ID',
            new_name='Division_Bailey_ID',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='Division_BAILEY',
            new_name='Division_Bailey',
        ),
    ]
