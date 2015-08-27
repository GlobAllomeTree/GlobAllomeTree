# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_sharing', '0003_dataset_locked'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='Import_error',
            field=models.BooleanField(default=False, db_column=b'import_error'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='Import_error_details',
            field=models.TextField(null=True, db_column=b'import_error_details', blank=True),
        ),
    ]
