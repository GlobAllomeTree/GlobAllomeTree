# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TreeType',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('ID_Tree_type', models.AutoField(serialize=False, primary_key=True, db_column=b'id_tree_type')),
                ('Name', models.CharField(max_length=255, null=True, db_column=b'name', blank=True)),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'tree_type',
            },
        ),
    ]
