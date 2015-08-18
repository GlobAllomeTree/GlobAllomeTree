# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Institution_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'institution_id')),
                ('Name', models.CharField(max_length=150, null=True, db_column=b'name', blank=True)),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'source_institution',
            },
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Operator_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'operator_id')),
                ('Name', models.CharField(max_length=200, db_column=b'name')),
                ('Institution', models.ForeignKey(to='source.Institution', db_column=b'institution_id')),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'source_operator',
            },
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Reference_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'reference_id')),
                ('Label', models.CharField(max_length=20, null=True, db_column=b'label', blank=True)),
                ('Author', models.CharField(max_length=200, null=True, db_column=b'author', blank=True)),
                ('Year', models.CharField(max_length=12, null=True, db_column=b'year', blank=True)),
                ('Reference', models.TextField(null=True, db_column=b'reference', blank=True)),
            ],
            options={
                'ordering': ('Label',),
                'db_table': 'source_reference',
            },
        ),
    ]
