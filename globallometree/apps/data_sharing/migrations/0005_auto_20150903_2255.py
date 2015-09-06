# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_sharing', '0004_auto_20150827_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datalicense',
            name='Available_to_registered_users',
            field=models.BooleanField(default=False, help_text=b'Is this license automatically granted to all registered globallometree users?', verbose_name=b'Automatically granted', db_column=b'available_to_registered_users'),
        ),
        migrations.AlterField(
            model_name='datalicense',
            name='Expires',
            field=models.CharField(default=b'on_activity_completion', max_length=100, db_column=b'expires', choices=[(b'on_activity_completion', b'When Data User has completed the activities for which the Data was provided.'), (b'on_three_months_notice', b'If either Party terminates this Agreement by notifying the other by email of its intent to terminate at least three months in advance of the effective date of termination, and indicating such termination date.'), (b'on_date', b'On the indicated date'), (b'none', b'No expiry')]),
        ),
        migrations.AlterField(
            model_name='datalicense',
            name='Restrict_attributed_ownership',
            field=models.BooleanField(default=False, help_text=b'The Data Provider shall be acknowledged as the data source. If changes are made to the Data, attribution should be given to the Data Provider as owner of the Data.', db_column=b'restrict_attributed_ownership'),
        ),
        migrations.AlterField(
            model_name='datalicense',
            name='Restrict_duplication',
            field=models.BooleanField(default=False, help_text=b"The Data User shall not duplicate the Data Provider's proprietary and copyright-protected Data or attempt to do so by altering, decompiling, or disassembling the Data.", db_column=b'restrict_duplication'),
        ),
        migrations.AlterField(
            model_name='datalicense',
            name='Restrict_resell',
            field=models.BooleanField(default=False, help_text=b"The Data User shall not sell, market, rent, lease, sublicense, lend, assign, time-share, distribute, disseminate or transfer, in whole or in part, the Data, any updates, or end user's rights under this Agreement.", db_column=b'restrict_resell'),
        ),
    ]
