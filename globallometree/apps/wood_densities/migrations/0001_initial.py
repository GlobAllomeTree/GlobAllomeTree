# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source', '0001_initial'),
        ('data_sharing', '0001_initial'),
        ('base', '0001_initial'),
        ('locations', '0001_initial'),
        ('taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WoodDensity',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Elasticsearch_doc_hash', models.CharField(db_column=b'elasticsearch_doc_hash', max_length=255, blank=True, help_text=b'The hash of the denormalized version of this model in elasticsearch, used for knowing if the es index needs to be updated or not', null=True, verbose_name=b'Elasticsearch document md5 hash')),
                ('Remark', models.TextField(null=True, blank=True)),
                ('Contact', models.CharField(max_length=255, null=True, blank=True)),
                ('ID_WD', models.AutoField(serialize=False, primary_key=True, db_column=b'id_wd')),
                ('H_tree_avg', models.DecimalField(db_column=b'h_tree_avg', decimal_places=10, max_digits=16, blank=True, help_text=b'Average height of tree measured', null=True)),
                ('H_tree_min', models.DecimalField(db_column=b'h_tree_min', decimal_places=10, max_digits=16, blank=True, help_text=b"Min of trees' height measured if several trees where sampled", null=True)),
                ('H_tree_max', models.DecimalField(db_column=b'h_tree_max', decimal_places=10, max_digits=16, blank=True, help_text=b"Max of trees' height measured if several trees where sampled", null=True)),
                ('DBH_tree_avg', models.DecimalField(db_column=b'dbh_tree_avg', decimal_places=10, max_digits=16, blank=True, help_text=b'Average DBH of tree measured', null=True)),
                ('DBH_tree_min', models.DecimalField(db_column=b'dbh_tree_min', decimal_places=10, max_digits=16, blank=True, help_text=b"Min of trees' DBH measured if several trees where sampled", null=True)),
                ('DBH_tree_max', models.DecimalField(db_column=b'dbh_tree_max', decimal_places=10, max_digits=16, blank=True, help_text=b"Max of trees' DBH measured if several trees where sampled", null=True)),
                ('m_WD', models.DecimalField(db_column=b'm_wd', decimal_places=10, max_digits=16, blank=True, help_text=b'Wood mass measured', null=True)),
                ('MC_m', models.DecimalField(db_column=b'mc_m', decimal_places=10, max_digits=16, blank=True, help_text=b'Moisture content of the wood during measurement, ex: (%) 0, 12, 15, Sat for saturation', null=True)),
                ('V_WD', models.DecimalField(db_column=b'v_md', decimal_places=10, max_digits=16, blank=True, help_text=b'Wood volume measured', null=True)),
                ('MC_V', models.DecimalField(db_column=b'mc_v', decimal_places=10, max_digits=16, blank=True, help_text=b'Moisture content of the wood during measurement, ex: (%) 0, 12, 15, Sat for saturation', null=True)),
                ('CR', models.DecimalField(db_column=b'cr', decimal_places=10, max_digits=16, blank=True, help_text=b'Coefficient of retraction (%/%)', null=True)),
                ('FSP', models.DecimalField(db_column=b'fsp', decimal_places=10, max_digits=16, blank=True, help_text=b'Fiber saturation point (%)', null=True)),
                ('Methodology', models.CharField(help_text=b'Water displacment or direct measurement', max_length=80, null=True, db_column=b'methodology', blank=True)),
                ('Bark', models.NullBooleanField(help_text=b'is the bark included in the measure?', db_column=b'bark')),
                ('Density_g_cm3', models.DecimalField(help_text=b'density of the wood in g/cm3', null=True, decimal_places=10, max_digits=16, db_column=b'densiy_g_cm3')),
                ('MC_Density', models.CharField(help_text=b'Moisture content, with code for specific cases, ex: (%) 0, 12, 15, BD for Basic density', max_length=80, null=True, db_column=b'mc_density', blank=True)),
                ('Data_origin', models.CharField(help_text=b'Calculated or  entered from biblio', max_length=80, null=True, db_column=b'data_origin', blank=True)),
                ('Data_type', models.CharField(help_text=b'Unique value, average of data, average of min max', max_length=80, null=True, db_column=b'data_type', blank=True)),
                ('Samples_per_tree', models.IntegerField(help_text=b'Number of samples per tree', null=True, db_column=b'samples_per_tree', blank=True)),
                ('Number_of_trees', models.IntegerField(help_text=b'Number of trees', null=True, db_column=b'number_of_trees', blank=True)),
                ('SD', models.DecimalField(db_column=b'sd', decimal_places=10, max_digits=16, blank=True, help_text=b'Standard Deviation', null=True)),
                ('Min', models.DecimalField(db_column=b'min', decimal_places=10, max_digits=16, blank=True, help_text=b'Min of WD in g.cm-3', null=True)),
                ('Max', models.DecimalField(db_column=b'max', decimal_places=10, max_digits=16, blank=True, help_text=b'Max of WD in g.cm-3', null=True)),
                ('H_measure', models.DecimalField(db_column=b'h_measure', decimal_places=10, max_digits=16, blank=True, help_text=b'Height where WD sample was collected', null=True)),
                ('Bark_distance', models.DecimalField(db_column=b'bark_distance', decimal_places=10, max_digits=16, blank=True, help_text=b'Distance where the WD was collected', null=True)),
                ('Convert_BD', models.DecimalField(db_column=b'convert_bd', decimal_places=10, max_digits=16, blank=True, help_text=b'0.861*Density if density is at 10 to 18%', null=True)),
                ('CV', models.IntegerField(help_text=b'SD/Density if Density is an average', null=True, db_column=b'cv', blank=True)),
                ('Contributor', models.ForeignKey(db_column=b'id_contributor', blank=True, to='source.Institution', null=True)),
                ('Dataset', models.ForeignKey(db_column=b'id_dataset', blank=True, to='data_sharing.Dataset', help_text=b'The Dataset that this raw data record came from', null=True)),
                ('Location_group', models.ForeignKey(db_column=b'id_location_group', blank=True, to='locations.LocationGroup', null=True)),
                ('Operator', models.ForeignKey(db_column=b'id_operator', blank=True, to='source.Operator', null=True)),
                ('Reference', models.ForeignKey(db_column=b'id_reference', blank=True, to='source.Reference', null=True)),
                ('Species_group', models.ForeignKey(db_column=b'id_species_group', blank=True, to='taxonomy.SpeciesGroup', null=True)),
                ('Tree_type', models.ForeignKey(db_column=b'id_tree_type', blank=True, to='base.TreeType', null=True)),
            ],
            options={
                'db_table': 'wood_density',
                'verbose_name': 'Wood Density',
                'verbose_name_plural': 'Wood Densities',
            },
        ),
    ]
