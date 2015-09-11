# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('linkbox', '0002_auto_20150910_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkbox',
            name='template',
            field=models.CharField(choices=[(b'cms/plugins/link_box.html', b'BOX - Link box with a clickable button'), (b'cms/plugins/link_image.html', b'IMAGE - Featured image with no button (for logos etc...)')], max_length=255, blank=True, help_text=b'Template that will be used to display this link', null=True, verbose_name=b'Template'),
        ),
        migrations.AddField(
            model_name='linkbox',
            name='url_target',
            field=models.CharField(choices=[(b'_blank', b'Opens in a new window'), (b'_self', b'Opens in the same window')], max_length=255, blank=True, help_text=b'If present image will be clickable.', null=True, verbose_name=b'Link Target'),
        ),
        migrations.AlterField(
            model_name='linkbox',
            name='description',
            field=models.TextField(default=b'<p></p>', null=True, verbose_name=b'Description', blank=True),
        ),
        migrations.AlterField(
            model_name='linkbox',
            name='image',
            field=models.ImageField(upload_to=b'linkbox', null=True, verbose_name=b'Image', blank=True),
        ),
        migrations.AlterField(
            model_name='linkbox',
            name='link_text',
            field=models.CharField(help_text='If present this text will be used on the button.', max_length=255, null=True, verbose_name=b'Button text', blank=True),
        ),
        migrations.AlterField(
            model_name='linkbox',
            name='title',
            field=models.CharField(max_length=255, verbose_name=b'Title'),
        ),
        migrations.AlterField(
            model_name='linkbox',
            name='url',
            field=models.CharField(help_text='If present image will be clickable.', max_length=255, null=True, verbose_name=b'Link', blank=True),
        ),
    ]
