# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='family',
            options={'ordering': ('Family_ID',), 'verbose_name_plural': 'Families'},
        ),
        migrations.AlterModelOptions(
            name='genus',
            options={'ordering': ('Genus_ID',), 'verbose_name_plural': 'Genera'},
        ),
        migrations.AlterModelOptions(
            name='species',
            options={'ordering': ('Species_ID',), 'verbose_name_plural': 'Species'},
        ),
        migrations.AlterModelOptions(
            name='speciesdefinition',
            options={'ordering': ('Species_definition_ID',)},
        ),
        migrations.AlterModelOptions(
            name='speciesgroup',
            options={'ordering': ('Species_group_ID',)},
        ),
        migrations.AlterModelOptions(
            name='specieslocalname',
            options={'ordering': ('Species_local_name_ID',)},
        ),
        migrations.AlterModelOptions(
            name='subspecies',
            options={'ordering': ('Subspecies_ID',), 'verbose_name_plural': 'Subspecies'},
        ),
        migrations.AlterField(
            model_name='specieslocalname',
            name='Language_iso_639_3',
            field=models.CharField(help_text=b'The ISO 639-3 Language Code for the language', max_length=3, null=True, db_column=b'language_iso_639_3', blank=True),
        ),
    ]
