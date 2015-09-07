# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=510)),
                ('summary', models.TextField(null=True, blank=True)),
                ('url', models.URLField(unique=True, max_length=400)),
                ('published', models.DateTimeField(null=True)),
            ],
            options={
                'ordering': ['-published'],
            },
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('site_url', models.URLField()),
                ('feed_url', models.URLField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='journal',
            field=models.ForeignKey(related_name='articles', to='journals.Journal'),
        ),
    ]
