# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_sharing', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('TPL_Status', models.CharField(max_length=80, null=True, db_column=b'tpl_status', blank=True)),
                ('TPL_Confidence_level', models.CharField(max_length=10, null=True, db_column=b'tpl_confidence_level', blank=True)),
                ('TPL_ID', models.CharField(max_length=40, null=True, db_column=b'tpl_ip', blank=True)),
                ('Family_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'family_id')),
                ('Name', models.CharField(max_length=120, null=True, db_column=b'name', blank=True)),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'taxonomy_family',
                'verbose_name_plural': 'Families',
            },
        ),
        migrations.CreateModel(
            name='Genus',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('TPL_Status', models.CharField(max_length=80, null=True, db_column=b'tpl_status', blank=True)),
                ('TPL_Confidence_level', models.CharField(max_length=10, null=True, db_column=b'tpl_confidence_level', blank=True)),
                ('TPL_ID', models.CharField(max_length=40, null=True, db_column=b'tpl_ip', blank=True)),
                ('Genus_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'genus_id')),
                ('Name', models.CharField(max_length=120, db_column=b'name')),
                ('Family', models.ForeignKey(to='taxonomy.Family', db_column=b'family_id')),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'taxonomy_genus',
                'verbose_name_plural': 'Genera',
            },
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('TPL_Status', models.CharField(max_length=80, null=True, db_column=b'tpl_status', blank=True)),
                ('TPL_Confidence_level', models.CharField(max_length=10, null=True, db_column=b'tpl_confidence_level', blank=True)),
                ('TPL_ID', models.CharField(max_length=40, null=True, db_column=b'tpl_ip', blank=True)),
                ('Species_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'species_id')),
                ('Name', models.CharField(max_length=120, db_column=b'name')),
                ('Author', models.CharField(max_length=120, null=True, db_column=b'author', blank=True)),
                ('Genus', models.ForeignKey(to='taxonomy.Genus', db_column=b'genus_id')),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'taxonomy_species',
                'verbose_name_plural': 'Species',
            },
        ),
        migrations.CreateModel(
            name='SpeciesDefinition',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Species_definition_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'species_definition_id')),
                ('Family', models.ForeignKey(to='taxonomy.Family', db_column=b'family_id')),
                ('Genus', models.ForeignKey(db_column=b'genus_id', blank=True, to='taxonomy.Genus', null=True)),
                ('Species', models.ForeignKey(db_column=b'species_id', blank=True, to='taxonomy.Species', null=True)),
            ],
            options={
                'db_table': 'taxonomy_species_definition',
            },
        ),
        migrations.CreateModel(
            name='SpeciesGroup',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Species_group_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'species_group_id')),
                ('Dataset_Species_group_ID', models.IntegerField(help_text=b'If group was created from a dataset, references the local group id in the source dataset', null=True, db_column=b'dataset_species_group_id', blank=True)),
                ('Name', models.CharField(max_length=255, null=True, verbose_name=b'Group Name', db_column=b'name', blank=True)),
                ('Dataset', models.ForeignKey(db_column=b'dataset_id', blank=True, to='data_sharing.Dataset', help_text=b'If group was created from a dataset, the dataset id', null=True)),
                ('Species_definitions', models.ManyToManyField(to='taxonomy.SpeciesDefinition', db_table=b'taxonomy_species_group_definitions', verbose_name=b'List of Species Definitions', blank=True)),
            ],
            options={
                'db_table': 'taxonomy_species_group',
            },
        ),
        migrations.CreateModel(
            name='SpeciesLocalName',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Species_local_name_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'species_local_name_id')),
                ('Local_name', models.CharField(help_text=b'The local name of this species in the local language', max_length=120, db_column=b'local_name')),
                ('Local_name_latin', models.CharField(help_text=b'A phonetic version using the latin alphabet', max_length=80, null=True, db_column=b'local_name_latin', blank=True)),
                ('Language_iso_639_3', models.CharField(help_text=b'The ISO 639-3 Language Code for the language', max_length=3, db_column=b'language_iso_639_3')),
                ('Species', models.ForeignKey(related_name='Local_names', db_column=b'species_id', to='taxonomy.Species')),
            ],
            options={
                'db_table': 'taxonomy_species_local_name',
            },
        ),
        migrations.CreateModel(
            name='Subspecies',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('TPL_Status', models.CharField(max_length=80, null=True, db_column=b'tpl_status', blank=True)),
                ('TPL_Confidence_level', models.CharField(max_length=10, null=True, db_column=b'tpl_confidence_level', blank=True)),
                ('TPL_ID', models.CharField(max_length=40, null=True, db_column=b'tpl_ip', blank=True)),
                ('Subspecies_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'subspecies_id')),
                ('Name', models.CharField(max_length=120, db_column=b'name')),
                ('Author', models.CharField(max_length=120, null=True, db_column=b'author', blank=True)),
                ('Species', models.ForeignKey(to='taxonomy.Species', db_column=b'species_id')),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'taxonomy_subspecies',
                'verbose_name_plural': 'Subspecies',
            },
        ),
        migrations.AddField(
            model_name='speciesdefinition',
            name='Subspecies',
            field=models.ForeignKey(db_column=b'subspecies_id', blank=True, to='taxonomy.Subspecies', null=True),
        ),
    ]
