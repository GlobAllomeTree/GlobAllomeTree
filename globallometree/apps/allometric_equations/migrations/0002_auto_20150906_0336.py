# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('allometric_equations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='allometricequation',
            name='Contact',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='allometricequation',
            name='Remark',
            field=models.TextField(null=True, blank=True),
        ),
    ]
