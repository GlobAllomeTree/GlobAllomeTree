# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_sharing', '0002_auto_20150819_0047'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='Locked',
            field=models.BooleanField(default=False, db_column=b'locked'),
        ),
    ]
