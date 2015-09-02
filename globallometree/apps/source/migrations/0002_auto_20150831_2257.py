# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reference',
            options={'ordering': ('Reference',)},
        ),
        migrations.RemoveField(
            model_name='reference',
            name='Label',
        ),
    ]
