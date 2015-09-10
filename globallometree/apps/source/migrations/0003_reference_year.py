# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source', '0002_remove_reference_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='Year',
            field=models.IntegerField(null=True, db_column=b'year', blank=True),
        ),
    ]
