# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_sharing', '0001_initial'),
        ('locations', '0001_initial'),
        ('taxonomy', '0001_initial'),
        ('source', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawData',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Elasticsearch_doc_hash', models.CharField(db_column=b'elasticsearch_doc_hash', max_length=255, blank=True, help_text=b'The hash of the denormalized version of this model in elasticsearch, used for knowing if the es index needs to be updated or not', null=True, verbose_name=b'Elasticsearch document md5 hash')),
                ('Raw_data_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'raw_data_id')),
                ('H_tree_avg', models.DecimalField(db_column=b'h_tree_avg', decimal_places=10, max_digits=16, blank=True, help_text=b'Average height of tree measured', null=True)),
                ('Tree_ID', models.IntegerField(help_text=b'Identification number of the tree from which data were collected', null=True, db_column=b'tree_id', blank=True)),
                ('Date_collection', models.DateField(help_text=b'Date of the data collection', null=True, db_column=b'date_collection', blank=True)),
                ('DBH_cm', models.DecimalField(db_column=b'dbh_cm', decimal_places=10, max_digits=16, blank=True, help_text=b'Diameter at breast height of the tree in centimeters', null=True)),
                ('H_m', models.DecimalField(db_column=b'h_m', decimal_places=10, max_digits=16, blank=True, help_text=b'Total height of the tree in meters', null=True)),
                ('CD_m', models.DecimalField(db_column=b'cd_m', decimal_places=10, max_digits=16, blank=True, help_text=b'Crown diameter of the tree in meters', null=True)),
                ('F_Bole_kg', models.DecimalField(db_column=b'f_bole_kg', decimal_places=10, max_digits=16, blank=True, help_text=b'Fresh weight of the bole in kg', null=True)),
                ('F_Branch_kg', models.DecimalField(db_column=b'f_branch_kg', decimal_places=10, max_digits=16, blank=True, help_text=b'Fresh weight of the branches in kg', null=True)),
                ('F_Foliage_kg', models.DecimalField(db_column=b'f_foliage_kg', decimal_places=10, max_digits=16, blank=True, help_text=b'Fresh weight of the foliage in kg', null=True)),
                ('F_Stump_kg', models.DecimalField(db_column=b'f_stump_kg', decimal_places=10, max_digits=16, blank=True, help_text=b'Fresh weight of the stump in kg', null=True)),
                ('F_Buttress_kg', models.DecimalField(db_column=b'f_buttress_kg', decimal_places=10, max_digits=16, blank=True, help_text=b'Fresh weight of the buttress in kg', null=True)),
                ('F_Roots_kg', models.DecimalField(db_column=b'f_roots_kg', decimal_places=10, max_digits=16, blank=True, help_text=b'Fresh weight of the roots in kg', null=True)),
                ('Volume_m3', models.DecimalField(db_column=b'volume_m3', decimal_places=10, max_digits=16, blank=True, help_text=b'Total volume of the tree in cubic meters', null=True)),
                ('Volume_bole_m3', models.DecimalField(db_column=b'volume_bole_m3', decimal_places=10, max_digits=16, blank=True, help_text=b'Volume of the bole in cubic meters', null=True)),
                ('WD_AVG_gcm3', models.DecimalField(db_column=b'wd_avg_gcm3', decimal_places=10, max_digits=16, blank=True, help_text=b'Average wood density value for the whole tree in grams/cubic centimeters', null=True)),
                ('DF_Bole_AVG', models.DecimalField(db_column=b'df_bole_avg', decimal_places=10, max_digits=16, blank=True, help_text=b'Average ratio between dry and fresh weight of the bole', null=True)),
                ('DF_Branch_AVG', models.DecimalField(db_column=b'df_branch_avg', decimal_places=10, max_digits=16, blank=True, help_text=b'Average ratio between dry and fresh weight of the branches', null=True)),
                ('DF_Foliage_AVG', models.DecimalField(db_column=b'df_foliage_avg', decimal_places=10, max_digits=16, blank=True, help_text=b'Average ratio between dry and fresh weight of the foliage', null=True)),
                ('DF_Stump_AVG', models.DecimalField(db_column=b'df_stump_avg', decimal_places=10, max_digits=16, blank=True, help_text=b'Average ratio between dry and fresh  weight of the stump', null=True)),
                ('DF_Buttress_AVG', models.DecimalField(db_column=b'df_buttress_avg', decimal_places=10, max_digits=16, blank=True, help_text=b'Average ratio between dry and fresh  weight of the buttress', null=True)),
                ('DF_Roots_AVG', models.DecimalField(db_column=b'df_roots_avg', decimal_places=10, max_digits=16, blank=True, help_text=b'Average ratio between dry and fresh weight of the roots', null=True)),
                ('D_Bole_kg', models.DecimalField(db_column=b'd_bole_kg', decimal_places=10, max_digits=16, blank=True, help_text=b'Dry weight of the bole in kg', null=True)),
                ('D_Branch_kg', models.DecimalField(db_column=b'd_branch_kg', decimal_places=10, max_digits=16, blank=True, help_text=b'Dry weight of the branches in kg', null=True)),
                ('D_Foliage_kg', models.DecimalField(db_column=b'd_foliage_kg', decimal_places=10, max_digits=16, blank=True, help_text=b'Dry weight of the foliage in kg', null=True)),
                ('D_Stump_kg', models.DecimalField(db_column=b'd_stump_kg', decimal_places=10, max_digits=16, blank=True, help_text=b'Dry weight of the stump in kg', null=True)),
                ('D_Buttress_kg', models.DecimalField(db_column=b'd_buttress_kg', decimal_places=10, max_digits=16, blank=True, help_text=b'Dry weight of the buttress in kg', null=True)),
                ('D_Roots_kg', models.DecimalField(db_column=b'd_roots_kg', decimal_places=10, max_digits=16, blank=True, help_text=b'Dry weight of the buttress in kg', null=True)),
                ('ABG_kg', models.DecimalField(db_column=b'abg_kg', decimal_places=10, max_digits=16, blank=True, help_text=b'Total aboveground biomass in kg', null=True)),
                ('BGB_kg', models.DecimalField(db_column=b'bgb_kg', decimal_places=10, max_digits=16, blank=True, help_text=b'Total belowground biomass in kg', null=True)),
                ('Tot_Biomass_kg', models.DecimalField(db_column=b'tot_biomass_kg', decimal_places=10, max_digits=16, blank=True, help_text=b'Total biomass of the tree in kg (aboveground + belowground)', null=True)),
                ('BEF', models.DecimalField(db_column=b'bef', decimal_places=10, max_digits=16, blank=True, help_text=b'Biomass expansion factor', null=True)),
                ('Contributor', models.ForeignKey(db_column=b'contributor_id', blank=True, to='source.Institution', null=True)),
                ('Dataset', models.ForeignKey(db_column=b'dataset_id', blank=True, to='data_sharing.Dataset', help_text=b'The Dataset that this raw data record came from', null=True)),
                ('Location_group', models.ForeignKey(db_column=b'location_group_id', blank=True, to='locations.LocationGroup', null=True)),
                ('Operator', models.ForeignKey(db_column=b'operator_id', blank=True, to='source.Operator', null=True)),
                ('Reference', models.ForeignKey(db_column=b'reference_id', blank=True, to='source.Reference', null=True)),
                ('Species_group', models.ForeignKey(db_column=b'species_group_id', blank=True, to='taxonomy.SpeciesGroup', null=True)),
            ],
            options={
                'db_table': 'raw_data',
                'verbose_name': 'Raw Data Instance',
                'verbose_name_plural': 'Raw Data',
            },
        ),
    ]
