# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_auto_20150901_2350'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ('Location_ID',)},
        ),
    ]
