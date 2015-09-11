# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('linkbox', '0003_auto_20150911_0729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkbox',
            name='template',
            field=models.CharField(default=b'cms/plugins/link_box.html', help_text=b'Template that will be used to display this link', max_length=255, verbose_name=b'Template', choices=[(b'cms/plugins/link_box.html', b'BOX - Link box with a clickable button'), (b'cms/plugins/link_image.html', b'IMAGE - Featured image with no button (for logos etc...)')]),
        ),
    ]
