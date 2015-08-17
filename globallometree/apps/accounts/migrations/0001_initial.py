# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserChanged',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=80, blank=True)),
                ('region', models.CharField(max_length=80, blank=True)),
                ('subregion', models.CharField(max_length=80, blank=True)),
                ('education', models.CharField(max_length=300, blank=True)),
                ('institution_name', models.CharField(max_length=200, blank=True)),
                ('institution_address', models.CharField(max_length=200, blank=True)),
                ('institution_phone', models.CharField(max_length=60, blank=True)),
                ('institution_fax', models.CharField(max_length=60, blank=True)),
                ('field_subject', models.CharField(max_length=60, blank=True)),
                ('data_may_provide', models.CharField(blank=True, max_length=40, choices=[(b'no_data', b'No data available'), (b'Species_data', b'Species data'), (b'wood_density', b'Wood Density'), (b'allometric_equation', b'Allometric Equation'), (b'reports', b'Reports and scientific literature containing new allometric equations'), (b'biomass_factors', b'Biomass Expansion Factors'), (b'volume_tables', b'Volume Tables')])),
                ('location_latitude', models.DecimalField(null=True, max_digits=8, decimal_places=5, blank=True)),
                ('location_longitude', models.DecimalField(null=True, max_digits=8, decimal_places=5, blank=True)),
                ('privacy', models.CharField(default=b'anonymous', max_length=20, choices=[(b'none', b"Private   - Don't share my profile or location at all"), (b'anonymous', b"Anonymous - Share my location anonymously, but don't share my profile"), (b'public', b'Public    - Share my location and my profile information')])),
                ('location_country', models.ForeignKey(blank=True, to='locations.Country', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
