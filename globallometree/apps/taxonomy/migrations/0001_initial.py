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
                ('TPL_ID', models.CharField(max_length=40, null=True, db_column=b'tpl_id', blank=True)),
                ('ID_Family', models.AutoField(serialize=False, primary_key=True, db_column=b'id_family')),
                ('Name', models.CharField(max_length=120, null=True, db_column=b'name', blank=True)),
            ],
            options={
                'ordering': ('ID_Family',),
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
                ('TPL_ID', models.CharField(max_length=40, null=True, db_column=b'tpl_id', blank=True)),
                ('ID_Genus', models.AutoField(serialize=False, primary_key=True, db_column=b'id_genus')),
                ('Name', models.CharField(max_length=120, db_column=b'name')),
                ('Family', models.ForeignKey(to='taxonomy.Family', db_column=b'id_family')),
            ],
            options={
                'ordering': ('ID_Genus',),
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
                ('TPL_ID', models.CharField(max_length=40, null=True, db_column=b'tpl_id', blank=True)),
                ('ID_Species', models.AutoField(serialize=False, primary_key=True, db_column=b'id_species')),
                ('Name', models.CharField(max_length=120, db_column=b'name')),
                ('Author', models.CharField(max_length=120, null=True, db_column=b'author', blank=True)),
                ('Genus', models.ForeignKey(to='taxonomy.Genus', db_column=b'id_genus')),
            ],
            options={
                'ordering': ('ID_Species',),
                'db_table': 'taxonomy_species',
                'verbose_name_plural': 'Species',
            },
        ),
        migrations.CreateModel(
            name='SpeciesDefinition',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('ID_Species_definition', models.AutoField(serialize=False, primary_key=True, db_column=b'id_species_definition')),
                ('Family', models.ForeignKey(to='taxonomy.Family', db_column=b'id_family')),
                ('Genus', models.ForeignKey(db_column=b'id_genus', blank=True, to='taxonomy.Genus', null=True)),
                ('Species', models.ForeignKey(db_column=b'id_species', blank=True, to='taxonomy.Species', null=True)),
            ],
            options={
                'ordering': ('ID_Species_definition',),
                'db_table': 'taxonomy_species_definition',
            },
        ),
        migrations.CreateModel(
            name='SpeciesGroup',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('ID_Species_group', models.AutoField(serialize=False, primary_key=True, db_column=b'id_species_group')),
                ('ID_Dataset_Species_group', models.IntegerField(help_text=b'If group was created from a dataset, references the local group id in the source dataset', null=True, db_column=b'dataset_id_species_group', blank=True)),
                ('Name', models.CharField(max_length=255, null=True, verbose_name=b'Group Name', db_column=b'name', blank=True)),
                ('Dataset', models.ForeignKey(db_column=b'id_dataset', blank=True, to='data_sharing.Dataset', help_text=b'If group was created from a dataset, the dataset id', null=True)),
                ('Species_definitions', models.ManyToManyField(to='taxonomy.SpeciesDefinition', db_table=b'taxonomy_species_group_definitions', verbose_name=b'List of Species Definitions', blank=True)),
            ],
            options={
                'ordering': ('ID_Species_group',),
                'db_table': 'taxonomy_species_group',
            },
        ),
        migrations.CreateModel(
            name='SpeciesLocalName',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('ID_Local_name', models.AutoField(serialize=False, primary_key=True, db_column=b'id_local_name')),
                ('Local_name', models.CharField(help_text=b'The local name of this species in the local language', max_length=120, db_column=b'local_name')),
                ('Local_name_latin', models.CharField(help_text=b'A phonetic version using the latin alphabet', max_length=80, null=True, db_column=b'local_name_latin', blank=True)),
                ('Language_iso_639_3', models.CharField(help_text=b'The ISO 639-3 Language Code for the language', max_length=3, null=True, db_column=b'language_iso_639_3', blank=True)),
                ('Species', models.ForeignKey(related_name='Local_names', db_column=b'id_species', to='taxonomy.Species')),
            ],
            options={
                'ordering': ('ID_Local_name',),
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
                ('TPL_ID', models.CharField(max_length=40, null=True, db_column=b'tpl_id', blank=True)),
                ('ID_Subspecies', models.AutoField(serialize=False, primary_key=True, db_column=b'id_subspecies')),
                ('Name', models.CharField(max_length=120, db_column=b'name')),
                ('Author', models.CharField(max_length=120, null=True, db_column=b'author', blank=True)),
                ('Species', models.ForeignKey(to='taxonomy.Species', db_column=b'id_species')),
            ],
            options={
                'ordering': ('ID_Subspecies',),
                'db_table': 'taxonomy_subspecies',
                'verbose_name_plural': 'Subspecies',
            },
        ),
        migrations.AddField(
            model_name='speciesdefinition',
            name='Subspecies',
            field=models.ForeignKey(db_column=b'subid_species', blank=True, to='taxonomy.Subspecies', null=True),
        ),
    ]
