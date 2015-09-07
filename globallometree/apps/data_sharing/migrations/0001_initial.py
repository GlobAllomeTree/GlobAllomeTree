# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DataLicense',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('ID_Data_license', models.AutoField(serialize=False, primary_key=True, db_column=b'id_data_license')),
                ('Title', models.CharField(max_length=200, verbose_name=b'License Title', db_column=b'title')),
                ('Requires_provider_approval', models.BooleanField(default=True, help_text=b'Do you as the data provider wish to individually review and approve each license grant?                    If you check the box, an email will be sent each time a user requests access to your data.                    If the box is not checked, then users will be able to agree to the license themselves online before                    bieing granted access to the data.', verbose_name=b'Require my approval of each license grant', db_column=b'requires_provider_approval')),
                ('Available_to_registered_users', models.BooleanField(default=False, help_text=b'Is this license automatically granted to all registered globallometree users?', verbose_name=b'Automatically granted', db_column=b'available_to_registered_users')),
                ('Public_choice', models.BooleanField(default=True, help_text=b'Should all GlobAllomeTree users have the option to choose this license when uploading data?', db_column=b'public_choice')),
                ('License_url', models.URLField(db_column=b'license_url', blank=True, help_text=b'This is shown in the admin only and is mostly used for creative commons licenses', null=True, verbose_name=b'Link to License')),
                ('Permitted_use', models.CharField(default=b'assessment', max_length=100, db_column=b'permitted_use', choices=[(b'assessment', b'Support tree and forest volume and biomass assessment'), (b'unrestricted', b'No restrictions on the purpose of use of the data'), (b'other', b'Other')])),
                ('Permitted_use_other_value', models.TextField(null=True, verbose_name=b'Permitted Use (Other)', db_column=b'permitted_use_other_value', blank=True)),
                ('Restrict_resell', models.BooleanField(default=False, help_text=b"The Data User shall not sell, market, rent, lease, sublicense, lend, assign, time-share, distribute, disseminate or transfer, in whole or in part, the Data, any updates, or end user's rights under this Agreement.", db_column=b'restrict_resell')),
                ('Restrict_duplication', models.BooleanField(default=False, help_text=b"The Data User shall not duplicate the Data Provider's proprietary and copyright-protected Data or attempt to do so by altering, decompiling, or disassembling the Data.", db_column=b'restrict_duplication')),
                ('Restrict_reproduction', models.BooleanField(default=False, help_text=b'The Data User shall not reproduce certain portions of the data for sale or any other commercial purposes with written permission of the data provider.', db_column=b'restrict_reproduction')),
                ('Restrict_derivation', models.BooleanField(default=False, help_text=b'The Data User shall not publish the Derivative Data without acknowledging the Data Provider.', db_column=b'restrict_derivation')),
                ('Restrict_association', models.BooleanField(default=False, help_text=b'The Data User shall not publish the Derivative Data without associating the Data Provider as a co-author.', db_column=b'restrict_association')),
                ('Restrict_attributed_ownership', models.BooleanField(default=False, help_text=b'The Data Provider shall be acknowledged as the data source. If changes are made to the Data, attribution should be given to the Data Provider as owner of the Data.', db_column=b'restrict_attributed_ownership')),
                ('Restrict_other_value', models.TextField(null=True, verbose_name=b'Additional restrictions', db_column=b'restrict_other_value', blank=True)),
                ('Expires', models.CharField(default=b'on_activity_completion', max_length=100, db_column=b'expires', choices=[(b'on_activity_completion', b'When Data User has completed the activities for which the Data was provided.'), (b'on_three_months_notice', b'If either Party terminates this Agreement by notifying the other by email of its intent to terminate at least three months in advance of the effective date of termination, and indicating such termination date.'), (b'on_date', b'On the indicated date'), (b'none', b'No expiry')])),
                ('Expires_on_date', models.DateField(null=True, verbose_name=b'Expiry Date', db_column=b'expires_on_date', blank=True)),
                ('User', models.ForeignKey(db_column=b'user_id', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'data_license',
            },
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('ID_Dataset', models.AutoField(serialize=False, primary_key=True, db_column=b'id_dataset')),
                ('Title', models.CharField(max_length=100, verbose_name=b'Dataset Title', db_column=b'title')),
                ('Uploaded_dataset_file', models.FileField(db_column=b'uploaded_dataset_file', upload_to=b'data_sharing', blank=True, help_text=b'The structure must match the GlobAllomeTree API structure. Samples may be found on the right.', null=True, verbose_name=b'Structured dataset file (csv, json, xml)')),
                ('Uploaded_source_document', models.FileField(db_column=b'uploaded_source_document', upload_to=b'data_sharing', blank=True, help_text=b'The source document can be a pdf, excel file, word document or other with data in any format.', null=True, verbose_name=b'Source document with data in any format')),
                ('Description', models.TextField(null=True, verbose_name=b'Brief description', db_column=b'description', blank=True)),
                ('Data_type', models.CharField(max_length=100, verbose_name=b'Type', db_column=b'data_type', choices=[(b'raw_data', b'Raw Data'), (b'biomass_expansion', b'Biomass Expansion Factors'), (b'wood_density', b'Wood Density Data'), (b'allometric_equations', b'Allometric Equations')])),
                ('Data_as_json', models.TextField(null=True, db_column=b'data_as_json', blank=True)),
                ('Record_count', models.IntegerField(null=True, db_column=b'record_count', blank=True)),
                ('Imported', models.BooleanField(default=False, help_text=b'If this file has been imported into the GlobAllomeTree database yet or not', db_column=b'imported')),
                ('Marked_for_import', models.BooleanField(default=False, db_column=b'marked_for_import')),
                ('Locked', models.BooleanField(default=False, db_column=b'locked')),
                ('Records_imported', models.IntegerField(default=0, db_column=b'records_imported')),
                ('Import_error', models.BooleanField(default=False, db_column=b'import_error')),
                ('Import_error_details', models.TextField(null=True, db_column=b'import_error_details', blank=True)),
                ('Data_license', models.ForeignKey(db_column=b'id_data_license', verbose_name=b'License', to='data_sharing.DataLicense')),
                ('User', models.ForeignKey(to=settings.AUTH_USER_MODEL, db_column=b'user_id')),
            ],
            options={
                'db_table': 'data_dataset',
            },
        ),
        migrations.CreateModel(
            name='DataSharingAgreement',
            fields=[
                ('Created', models.DateTimeField(auto_now_add=True, db_column=b'created')),
                ('Modified', models.DateTimeField(auto_now=True, verbose_name=b'Last modified', db_column=b'modified')),
                ('ID_Data_sharing_agreement', models.AutoField(serialize=False, primary_key=True, db_column=b'id_data_sharing_agreement')),
                ('Agreement_status', models.CharField(max_length=15, db_column=b'agreement_status', choices=[(b'pending', b'Pending provider response'), (b'granted', b'Granted'), (b'denied', b'Denied')])),
                ('Dataset', models.ForeignKey(to='data_sharing.Dataset', db_column=b'id_dataset')),
                ('User', models.ForeignKey(db_column=b'user_id', to=settings.AUTH_USER_MODEL, help_text=b'The user requesting access to the dataset')),
            ],
            options={
                'db_table': 'data_sharing_agreement',
            },
        ),
    ]
