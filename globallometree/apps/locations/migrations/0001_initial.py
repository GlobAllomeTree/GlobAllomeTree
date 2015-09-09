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
                ('ID_Biome_local', models.AutoField(serialize=False, primary_key=True, db_column=b'id_biome_local')),
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
                ('ID_Continent', models.AutoField(serialize=False, primary_key=True, db_column=b'id_continent')),
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
                ('ID_Country', models.AutoField(serialize=False, primary_key=True, db_column=b'id_country')),
                ('Common_name', models.CharField(max_length=159, db_column=b'common_name', blank=True)),
                ('Formal_name', models.CharField(max_length=159, db_column=b'formal_name', blank=True)),
                ('Common_name_fr', models.CharField(max_length=159, db_column=b'common_name_fr', blank=True)),
                ('Formal_name_fr', models.CharField(max_length=159, db_column=b'formal_name_fr', blank=True)),
                ('Iso3166a2', models.CharField(max_length=6, db_column=b'iso3166a2', blank=True)),
                ('Iso3166a3', models.CharField(max_length=9, db_column=b'iso3166a3', blank=True)),
                ('Iso3166n3', models.IntegerField(null=True, db_column=b'iso3166n3', blank=True)),
                ('Centroid_latitude', models.DecimalField(null=True, decimal_places=2, max_digits=5, db_column=b'centroid_latitude', blank=True)),
                ('Centroid_longitude', models.DecimalField(null=True, decimal_places=2, max_digits=5, db_column=b'centroid_longitude', blank=True)),
                ('Continent', models.ForeignKey(db_column=b'id_continent', blank=True, to='locations.Continent', null=True)),
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
                ('ID_Division_Bailey', models.AutoField(serialize=False, primary_key=True, db_column=b'id_division_bailey')),
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
                ('ID_Ecoregion_Udvardy', models.AutoField(serialize=False, primary_key=True, db_column=b'id_ecoregion_udvardy')),
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
                ('ID_Ecoregion_WWF', models.AutoField(serialize=False, primary_key=True, db_column=b'id_ecoregion_wwf')),
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
            name='Location',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('ID_Location', models.AutoField(serialize=False, primary_key=True, db_column=b'id_location')),
                ('Name', models.CharField(max_length=255, null=True, db_column=b'name', blank=True)),
                ('Region', models.CharField(max_length=255, null=True, db_column=b'region', blank=True)),
                ('Latitude', models.DecimalField(null=True, decimal_places=9, max_digits=12, db_column=b'latitude', blank=True)),
                ('Longitude', models.DecimalField(null=True, decimal_places=9, max_digits=12, db_column=b'longitude', blank=True)),
                ('Biome_local', models.ForeignKey(db_column=b'id_biome_local', blank=True, to='locations.BiomeLocal', null=True)),
                ('Country', models.ForeignKey(db_column=b'id_country', blank=True, to='locations.Country', null=True)),
                ('Division_Bailey', models.ForeignKey(db_column=b'id_division_bailey', blank=True, to='locations.DivisionBailey', null=True)),
                ('Ecoregion_Udvardy', models.ForeignKey(db_column=b'id_ecoregion_udvardy', blank=True, to='locations.EcoregionUdvardy', null=True)),
                ('Ecoregion_WWF', models.ForeignKey(db_column=b'id_ecoregion_wwf', blank=True, to='locations.EcoregionWWF', null=True)),
            ],
            options={
                'ordering': ('ID_Location',),
                'db_table': 'locations_location',
            },
        ),
        migrations.CreateModel(
            name='LocationGroup',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('ID_Location_group', models.AutoField(serialize=False, primary_key=True, db_column=b'id_location_group')),
                ('Dataset_ID_Location_group', models.IntegerField(help_text=b'If group was created from a dataset, references the local group id in the source dataset', null=True, db_column=b'dataset_id_location_group', blank=True)),
                ('Name', models.CharField(max_length=255, null=True, verbose_name=b'Group Name', db_column=b'name', blank=True)),
                ('Dataset', models.ForeignKey(db_column=b'id_dataset', blank=True, to='data_sharing.Dataset', help_text=b'If group was created from a dataset, the dataset id', null=True)),
                ('Locations', models.ManyToManyField(to='locations.Location', db_table=b'locations_group_locations', verbose_name=b'List of Locations', blank=True)),
            ],
            options={
                'db_table': 'locations_group',
            },
        ),
        migrations.CreateModel(
            name='VegetationType',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('ID_Vegetation_type', models.AutoField(serialize=False, primary_key=True, db_column=b'id_vegetation_type')),
                ('Name', models.CharField(max_length=255, null=True, db_column=b'name', blank=True)),
            ],
            options={
                'ordering': ('Name',),
                'db_table': 'locations_vegetation_type',
            },
        ),
        migrations.CreateModel(
            name='ZoneFAO',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('ID_Zone_FAO', models.AutoField(serialize=False, primary_key=True, db_column=b'id_zone_fao')),
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
                ('ID_Zone_Holdridge', models.AutoField(serialize=False, primary_key=True, db_column=b'id_zone_holdridge')),
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
            name='Vegetation_type',
            field=models.ForeignKey(db_column=b'id_vegetation_type', blank=True, to='locations.VegetationType', null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='Zone_FAO',
            field=models.ForeignKey(db_column=b'id_zone_fao', blank=True, to='locations.ZoneFAO', null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='Zone_Holdridge',
            field=models.ForeignKey(db_column=b'id_zone_holdridge', blank=True, to='locations.ZoneHoldridge', null=True),
        ),
    ]
