# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('linkbox', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkbox',
            name='description',
            field=models.TextField(default=b'<p></p>', null=True, verbose_name='description', blank=True),
        ),
    ]
