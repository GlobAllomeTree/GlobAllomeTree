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
            name='BiomassExpansionFactor',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Elasticsearch_doc_hash', models.CharField(db_column=b'elasticsearch_doc_hash', max_length=255, blank=True, help_text=b'The hash of the denormalized version of this model in elasticsearch, used for knowing if the es index needs to be updated or not', null=True, verbose_name=b'Elasticsearch document md5 hash')),
                ('Remark', models.TextField(null=True, blank=True)),
                ('Contact', models.CharField(max_length=255, null=True, blank=True)),
                ('ID_BEF', models.AutoField(serialize=False, primary_key=True, db_column=b'id_bef')),
                ('Growing_stock', models.DecimalField(db_column=b'growing_stock', decimal_places=10, max_digits=16, blank=True, help_text=b'Growing stock', null=True)),
                ('Aboveground_biomass', models.DecimalField(db_column=b'aboveground_biomass', decimal_places=10, max_digits=16, blank=True, help_text=b'Above ground  biomass', null=True)),
                ('Net_annual_increment', models.DecimalField(db_column=b'net_annual_increment', decimal_places=10, max_digits=16, blank=True, help_text=b'Net annual increment', null=True)),
                ('Stand_density', models.DecimalField(db_column=b'stand_density', decimal_places=10, max_digits=16, blank=True, help_text=b'Stand density', null=True)),
                ('Age', models.IntegerField(help_text=b'Age', null=True, db_column=b'age', blank=True)),
                ('BEF', models.DecimalField(db_column=b'bef', decimal_places=10, max_digits=16, blank=True, help_text=b'Biomass expansion factor', null=True)),
                ('Input', models.CharField(help_text=b'Input', max_length=b'255', null=True, db_column=b'input', blank=True)),
                ('Output', models.CharField(help_text=b'Output', max_length=b'255', null=True, db_column=b'output', blank=True)),
                ('Interval_validity', models.CharField(help_text=b'Interval validity', max_length=b'255', null=True, db_column=b'interval_validity', blank=True)),
                ('Contributor', models.ForeignKey(db_column=b'id_contributor', blank=True, to='source.Institution', null=True)),
                ('Dataset', models.ForeignKey(db_column=b'id_dataset', blank=True, to='data_sharing.Dataset', help_text=b'The Dataset that this raw data record came from', null=True)),
                ('Location_group', models.ForeignKey(db_column=b'id_location_group', blank=True, to='locations.LocationGroup', null=True)),
                ('Operator', models.ForeignKey(db_column=b'id_operator', blank=True, to='source.Operator', null=True)),
                ('Reference', models.ForeignKey(db_column=b'id_reference', blank=True, to='source.Reference', null=True)),
                ('Species_group', models.ForeignKey(db_column=b'id_species_group', blank=True, to='taxonomy.SpeciesGroup', null=True)),
                ('Tree_type', models.ForeignKey(db_column=b'id_tree_type', blank=True, to='base.TreeType', null=True)),
            ],
            options={
                'db_table': 'biomass_expansion_factors',
                'verbose_name': 'Biomass Expansion Factors Instance',
                'verbose_name_plural': 'Biomass Expansion Factors',
            },
        ),
    ]
