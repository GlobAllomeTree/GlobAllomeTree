# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_sharing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='Data_as_json',
        ),
        migrations.AddField(
            model_name='dataset',
            name='Data_as_json_file',
            field=models.FileField(upload_to=b'data_json', null=True, verbose_name=b'The document converted into json format', db_column=b'data_as_json_file', blank=True),
        ),
    ]
