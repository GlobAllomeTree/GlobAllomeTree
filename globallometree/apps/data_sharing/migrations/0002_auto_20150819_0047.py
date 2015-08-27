# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_sharing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='Marked_for_import',
            field=models.BooleanField(default=False, db_column=b'marked_for_import'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='Records_imported',
            field=models.IntegerField(default=0, db_column=b'records_imported'),
        ),
    ]
