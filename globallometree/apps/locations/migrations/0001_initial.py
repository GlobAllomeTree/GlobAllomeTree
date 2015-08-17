# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_sharing', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='BiomeLocal',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Biome_local_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'biome_local_id')),
                ('Reference', models.CharField(max_length=200, db_column=b'reference')),
                ('Name', models.CharField(max_length=200, db_column=b'name')),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'locations_biome_local',
                'verbose_name': 'Local Biome',
                'verbose_name_plural': 'Local Biomes',
            },
        ),
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Continent_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'continent_id')),
                ('Code', models.CharField(max_length=2, db_column=b'code')),
                ('Name', models.CharField(max_length=100, db_column=b'name')),
            ],
            options={
                'db_table': 'locations_continent',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Country_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'country_id')),
                ('Common_name', models.CharField(max_length=159, db_column=b'common_name', blank=True)),
                ('Formal_name', models.CharField(max_length=159, db_column=b'formal_name', blank=True)),
                ('Common_name_fr', models.CharField(max_length=159, db_column=b'common_name_fr', blank=True)),
                ('Formal_name_fr', models.CharField(max_length=159, db_column=b'formal_name_fr', blank=True)),
                ('Iso3166a2', models.CharField(max_length=6, db_column=b'iso3166a2', blank=True)),
                ('Iso3166a3', models.CharField(max_length=9, db_column=b'iso3166a3', blank=True)),
                ('Iso3166n3', models.IntegerField(null=True, db_column=b'iso3166n3', blank=True)),
                ('Centroid_latitude', models.DecimalField(null=True, decimal_places=2, max_digits=5, db_column=b'centroid_latitude', blank=True)),
                ('Centroid_longitude', models.DecimalField(null=True, decimal_places=2, max_digits=5, db_column=b'centroid_longitude', blank=True)),
                ('Continent', models.ForeignKey(db_column=b'continent_id', blank=True, to='locations.Continent', null=True)),
            ],
            options={
                'ordering': ('Common_name',),
                'db_table': 'locations_country',
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='DivisionBailey',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Division_BAILEY_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'division_bailey_id')),
                ('Name', models.CharField(max_length=200, db_column=b'name')),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'locations_division_bailey',
                'verbose_name': 'Division Bailey',
                'verbose_name_plural': 'Division Bailey List',
            },
        ),
        migrations.CreateModel(
            name='EcoregionUdvardy',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Ecoregion_Udvardy_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'ecoregion_udvardy_id')),
                ('Name', models.CharField(max_length=200, db_column=b'name')),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'locations_ecoregion_udvardy',
                'verbose_name': 'Udvardy Ecoregion',
                'verbose_name_plural': 'Udvardy Ecoregions',
            },
        ),
        migrations.CreateModel(
            name='EcoregionWWF',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Ecoregion_WWF_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'ecoregion_wwf_id')),
                ('Name', models.CharField(max_length=200, db_column=b'name')),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'locations_ecoregion_wwf',
                'verbose_name': 'WWF Terrestrial Ecoregion',
                'verbose_name_plural': 'WWF Terrestrial Ecoregion',
            },
        ),
        migrations.CreateModel(
            name='ForestType',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Forest_type_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'forest_type_id')),
                ('Name', models.CharField(max_length=255, null=True, db_column=b'name', blank=True)),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'locations_forest_type',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Location_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'location_id')),
                ('Name', models.CharField(max_length=255, null=True, db_column=b'name', blank=True)),
                ('Plot_name', models.CharField(help_text=b'name or id of the plot in the study, or data import', max_length=30, null=True, db_column=b'plot_name', blank=True)),
                ('Plot_size_m2', models.DecimalField(db_column=b'plot_size_m2', decimal_places=2, max_digits=10, blank=True, help_text=b'size of the plot in m2', null=True)),
                ('Commune', models.CharField(max_length=255, null=True, db_column=b'commune', blank=True)),
                ('Province', models.CharField(max_length=255, null=True, db_column=b'province', blank=True)),
                ('Region', models.CharField(max_length=255, null=True, db_column=b'region', blank=True)),
                ('Latitude', models.DecimalField(null=True, decimal_places=9, max_digits=12, db_column=b'latitude', blank=True)),
                ('Longitude', models.DecimalField(null=True, decimal_places=9, max_digits=12, db_column=b'longitude', blank=True)),
                ('Biome_local', models.ForeignKey(db_column=b'biome_local_id', blank=True, to='locations.BiomeLocal', null=True)),
                ('Country', models.ForeignKey(db_column=b'country_id', blank=True, to='locations.Country', null=True)),
                ('Division_BAILEY', models.ForeignKey(db_column=b'division_bailey_id', blank=True, to='locations.DivisionBailey', null=True)),
                ('Ecoregion_Udvardy', models.ForeignKey(db_column=b'ecoregion_udvardy_id', blank=True, to='locations.EcoregionUdvardy', null=True)),
                ('Ecoregion_WWF', models.ForeignKey(db_column=b'ecoregion_wwf_id', blank=True, to='locations.EcoregionWWF', null=True)),
                ('Forest_type', models.ForeignKey(db_column=b'forest_type_id', blank=True, to='locations.ForestType', null=True)),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'locations_location',
            },
        ),
        migrations.CreateModel(
            name='LocationGroup',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Location_group_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'location_group_id')),
                ('Dataset_Location_group_ID', models.IntegerField(help_text=b'If group was created from a dataset, references the local group id in the source dataset', null=True, db_column=b'dataset_location_group_id', blank=True)),
                ('Name', models.CharField(max_length=255, null=True, verbose_name=b'Group Name', db_column=b'name', blank=True)),
                ('Dataset', models.ForeignKey(db_column=b'dataset_id', blank=True, to='data_sharing.Dataset', help_text=b'If group was created from a dataset, the dataset id', null=True)),
                ('Locations', models.ManyToManyField(to='locations.Location', db_table=b'locations_group_locations', verbose_name=b'List of Locations', blank=True)),
            ],
            options={
                'db_table': 'locations_group',
            },
        ),
        migrations.CreateModel(
            name='ZoneFAO',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Zone_FAO_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'zone_fao_id')),
                ('Name', models.CharField(max_length=200, db_column=b'name')),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'locations_zone_fao',
                'verbose_name': 'FAO Global Ecological Zone',
                'verbose_name_plural': 'FAO Global Ecological Zones',
            },
        ),
        migrations.CreateModel(
            name='ZoneHoldridge',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('Zone_Holdridge_ID', models.AutoField(serialize=False, primary_key=True, db_column=b'zone_holdridge_id')),
                ('Name', models.CharField(max_length=200, db_column=b'name')),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'locations_zone_holdridge',
                'verbose_name': 'Holdridge Life Zone',
                'verbose_name_plural': 'Holdridge Life Zones',
            },
        ),
        migrations.AddField(
            model_name='location',
            name='Zone_FAO',
            field=models.ForeignKey(db_column=b'zone_fao_id', blank=True, to='locations.ZoneFAO', null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='Zone_Holdridge',
            field=models.ForeignKey(db_column=b'zone_holdridge_id', blank=True, to='locations.ZoneHoldridge', null=True),
        ),
    ]
