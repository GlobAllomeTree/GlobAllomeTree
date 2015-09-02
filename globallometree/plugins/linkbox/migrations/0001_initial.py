# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):


    operations = [
        migrations.CreateModel(
            name='LinkBox',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('image', models.ImageField(upload_to=b'linkbox', null=True, verbose_name='image', blank=True)),
                ('link_text', models.CharField(max_length=255, null=True, verbose_name=b'link text', blank=True)),
                ('url', models.CharField(help_text='If present image will be clickable.', max_length=255, null=True, verbose_name='link', blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('page_link', models.ForeignKey(blank=True, to='cms.Page', help_text='If present image will be clickable', null=True, verbose_name='page')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
