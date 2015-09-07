# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        ('data_sharing', '__first__'),
        ('base', '0001_initial'),
        ('taxonomy', '0001_initial'),
        ('source', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllometricEquation',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('B', models.NullBooleanField(db_column=b'b')),
                ('Bd', models.NullBooleanField(db_column=b'bd')),
                ('Bg', models.NullBooleanField(db_column=b'bg')),
                ('Bt', models.NullBooleanField(db_column=b'bt')),
                ('L', models.NullBooleanField(db_column=b'l')),
                ('Rb', models.NullBooleanField(db_column=b'rb')),
                ('Rf', models.NullBooleanField(db_column=b'rf')),
                ('Rm', models.NullBooleanField(db_column=b'rm')),
                ('S', models.NullBooleanField(db_column=b's')),
                ('T', models.NullBooleanField(db_column=b't')),
                ('F', models.NullBooleanField(db_column=b'f')),
                ('Elasticsearch_doc_hash', models.CharField(db_column=b'elasticsearch_doc_hash', max_length=255, blank=True, help_text=b'The hash of the denormalized version of this model in elasticsearch, used for knowing if the es index needs to be updated or not', null=True, verbose_name=b'Elasticsearch document md5 hash')),
                ('Remark', models.TextField(null=True, blank=True)),
                ('Contact', models.CharField(max_length=255, null=True, blank=True)),
                ('ID_AE', models.AutoField(serialize=False, primary_key=True, db_column=b'id_ae')),
                ('U', models.CharField(max_length=20, null=True, db_column=b'u', blank=True)),
                ('Unit_U', models.CharField(max_length=20, null=True, db_column=b'unit_u', blank=True)),
                ('V', models.CharField(max_length=20, null=True, db_column=b'v', blank=True)),
                ('Unit_V', models.CharField(max_length=20, null=True, db_column=b'unit_v', blank=True)),
                ('W', models.CharField(max_length=20, null=True, db_column=b'w', blank=True)),
                ('Unit_W', models.CharField(max_length=20, null=True, db_column=b'unit_w', blank=True)),
                ('X', models.CharField(max_length=20, null=True, db_column=b'x', blank=True)),
                ('Unit_X', models.CharField(max_length=20, null=True, db_column=b'unit_x', blank=True)),
                ('Z', models.CharField(max_length=20, null=True, db_column=b'z', blank=True)),
                ('Unit_Z', models.CharField(max_length=20, null=True, db_column=b'unit_z', blank=True)),
                ('Min_X', models.DecimalField(null=True, decimal_places=10, max_digits=16, db_column=b'min_x', blank=True)),
                ('Max_X', models.DecimalField(null=True, decimal_places=10, max_digits=16, db_column=b'max_x', blank=True)),
                ('Min_Z', models.DecimalField(null=True, decimal_places=10, max_digits=16, db_column=b'min_z', blank=True)),
                ('Max_Z', models.DecimalField(null=True, decimal_places=10, max_digits=16, db_column=b'max_z', blank=True)),
                ('Output', models.CharField(max_length=30, null=True, db_column=b'output')),
                ('Output_TR', models.CharField(max_length=30, null=True, db_column=b'output_tr', blank=True)),
                ('Unit_Y', models.CharField(max_length=50, null=True, db_column=b'unit_y', blank=True)),
                ('Age', models.CharField(max_length=50, null=True, db_column=b'age', blank=True)),
                ('Veg_Component', models.CharField(max_length=150, null=True, db_column=b'veg_component', blank=True)),
                ('Equation', models.CharField(max_length=500, db_column=b'equation')),
                ('Substitute_equation', models.CharField(max_length=500, null=True, db_column=b'substitute_equation', blank=True)),
                ('Top_dob', models.DecimalField(null=True, decimal_places=10, max_digits=16, db_column=b'top_dob', blank=True)),
                ('Stump_height', models.DecimalField(null=True, decimal_places=10, max_digits=16, db_column=b'stump_height', blank=True)),
                ('R2', models.DecimalField(null=True, decimal_places=10, max_digits=16, db_column=b'r2', blank=True)),
                ('R2_Adjusted', models.DecimalField(null=True, decimal_places=10, max_digits=16, db_column=b'r2_adjusted', blank=True)),
                ('RMSE', models.DecimalField(null=True, decimal_places=10, max_digits=16, db_column=b'rmse', blank=True)),
                ('SEE', models.DecimalField(null=True, decimal_places=10, max_digits=16, db_column=b'see', blank=True)),
                ('Corrected_for_bias', models.NullBooleanField(db_column=b'corrected_for_bias')),
                ('Bias_correction', models.DecimalField(null=True, decimal_places=10, max_digits=16, db_column=b'bias_correction', blank=True)),
                ('Ratio_equation', models.NullBooleanField(db_column=b'ratio_equation')),
                ('Segmented_equation', models.NullBooleanField(db_column=b'segmented_equation')),
                ('Sample_size', models.CharField(max_length=150, null=True, db_column=b'sample_size', blank=True)),
                ('Contributor', models.ForeignKey(db_column=b'id_contributor', blank=True, to='source.Institution', null=True)),
                ('Dataset', models.ForeignKey(db_column=b'id_dataset', blank=True, to='data_sharing.Dataset', help_text=b'The Dataset that this raw data record came from', null=True)),
                ('Location_group', models.ForeignKey(db_column=b'id_location_group', blank=True, to='locations.LocationGroup', null=True)),
                ('Operator', models.ForeignKey(db_column=b'id_operator', blank=True, to='source.Operator', null=True)),
            ],
            options={
                'db_table': 'allometric_equation',
                'verbose_name': 'Allometric Equation',
                'verbose_name_plural': 'Allometric Equations',
            },
        ),
        migrations.CreateModel(
            name='Population',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('ID_Population', models.AutoField(serialize=False, primary_key=True, db_column=b'id_population')),
                ('Name', models.CharField(max_length=255, null=True, db_column=b'name', blank=True)),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'allometric_equation_population',
            },
        ),
        migrations.AddField(
            model_name='allometricequation',
            name='Population',
            field=models.ForeignKey(db_column=b'id_population', blank=True, to='allometric_equations.Population', null=True),
        ),
        migrations.AddField(
            model_name='allometricequation',
            name='Reference',
            field=models.ForeignKey(db_column=b'id_reference', blank=True, to='source.Reference', null=True),
        ),
        migrations.AddField(
            model_name='allometricequation',
            name='Species_group',
            field=models.ForeignKey(db_column=b'id_species_group', blank=True, to='taxonomy.SpeciesGroup', null=True),
        ),
        migrations.AddField(
            model_name='allometricequation',
            name='Tree_type',
            field=models.ForeignKey(db_column=b'id_tree_type', blank=True, to='base.TreeType', null=True),
        ),
    ]
