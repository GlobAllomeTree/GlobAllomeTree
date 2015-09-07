from django.db import models
from django.contrib.auth.models import User
from globallometree.apps.search_helpers.models import BaseModel

class DataLicense(BaseModel):

    PERMITTED_USE_CHOICES = (
        ('assessment', 'Support tree and forest volume and biomass assessment'),
        ('unrestricted', 'No restrictions on the purpose of use of the data'),
        ('other', 'Other'),
        )

    SHARING_CHOICES = (
        ('raw_yes__derivative_no', 'The Data User is not permitted to share the Data with a third Party, but is allowed to share Derivative Data.'),
        ('raw_no__derivative_no', 'The Data user is not permitted to share the Data or Derivative Data to a third Party.'),
        ('raw_yes__deritive_yes', 'The Data user is permitted to share the Data and Derivative Data to a third Party without informing the Data Provider.'),
        )

    EXPIRE_CHOICES = (
        ('on_activity_completion', 'When Data User has completed the activities for which the Data was provided.'),
        ('on_three_months_notice', 'If either Party terminates this Agreement by notifying the other by email of its intent to terminate at least three months in advance of the effective date of termination, and indicating such termination date.'),
        ('on_date', 'On the indicated date'),
        ('none', 'No expiry'),
        )

    ID_Data_license = models.AutoField(primary_key=True, db_column="id_data_license")

    Title = models.CharField(
        verbose_name='License Title',
        max_length=200,
        db_column="title"
        )

    Requires_provider_approval = models.BooleanField(
        verbose_name='Require my approval of each license grant',
        help_text="Do you as the data provider wish to individually review and approve each license grant? \
                   If you check the box, an email will be sent each time a user requests access to your data. \
                   If the box is not checked, then users will be able to agree to the license themselves online before \
                   bieing granted access to the data.",
        default=True,
        db_column="requires_provider_approval"
        )

    Available_to_registered_users = models.BooleanField(
        help_text="Is this license automatically granted to all registered globallometree users?",
        default=False,
        db_column="available_to_registered_users",
        verbose_name="Automatically granted"
        )

    Public_choice = models.BooleanField(
        default=True,
        help_text="Should all GlobAllomeTree users have the option to choose this license when uploading data?",
        db_column="public_choice"
        )

    License_url = models.URLField(
        verbose_name='Link to License',
        help_text="This is shown in the admin only and is mostly used for creative commons licenses",
        blank=True,
        null=True,
        db_column="license_url"
        )

    User = models.ForeignKey(
        User,
        db_column="user_id",
        blank=True,
        null=True
        )

    Permitted_use = models.CharField(
        max_length=100,
        choices=PERMITTED_USE_CHOICES,
        default='assessment',
        db_column="permitted_use"
    )

    Permitted_use_other_value = models.TextField(
        verbose_name="Permitted Use (Other)",
        blank=True,
        null=True,
        db_column="permitted_use_other_value"
    )

    Restrict_resell = models.BooleanField(
        default=False,
        help_text="The Data User shall not sell, market, rent, lease, sublicense, lend, assign, time-share, distribute, disseminate or transfer, in whole or in part, the Data, any updates, or end user's rights under this Agreement.",
        db_column="restrict_resell"
    )

    Restrict_duplication = models.BooleanField(
        default=False,
        help_text="The Data User shall not duplicate the Data Provider's proprietary and copyright-protected Data or attempt to do so by altering, decompiling, or disassembling the Data.",
        db_column="restrict_duplication"
    )

    Restrict_reproduction = models.BooleanField(
        default=False,
        help_text="The Data User shall not reproduce certain portions of the data for sale or any other commercial purposes with written permission of the data provider.",
        db_column="restrict_reproduction"
    )

    Restrict_derivation = models.BooleanField(
        default=False,
        help_text="The Data User shall not publish the Derivative Data without acknowledging the Data Provider.",
        db_column="restrict_derivation"
        )

    Restrict_association = models.BooleanField(
        default=False,
        help_text="The Data User shall not publish the Derivative Data without associating the Data Provider as a co-author.",
        db_column="restrict_association"
        )

    Restrict_attributed_ownership = models.BooleanField(
        default=False,
        help_text="The Data Provider shall be acknowledged as the data source. If changes are made to the Data, attribution should be given to the Data Provider as owner of the Data.",
        db_column="restrict_attributed_ownership"
    )

    Restrict_other_value = models.TextField(
        verbose_name="Additional restrictions",
        blank=True,
        null=True,
        db_column="restrict_other_value"
    )

    Expires = models.CharField(
        max_length=100,
        choices=EXPIRE_CHOICES,
        default='on_activity_completion',
        db_column="expires"
    )

    Expires_on_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Expiry Date",
        db_column="expires_on_date"
    )

    def get_Permitted_use_text(self):
        if self.Permitted_use == 'other':
            return self.Permitted_use_other_value
        else:
            return self.get_Permitted_use_display()

    class Meta:
        db_table = "data_license"

    def __unicode__(self):
        return self.Title


class Dataset(BaseModel):

    ID_Dataset = models.AutoField(primary_key=True, db_column="id_dataset")

    User = models.ForeignKey(
        User,
        db_column='user_id',
    )

    DATA_TYPE_CHOICES = (
        ('raw_data' , 'Raw Data'),
        ('biomass_expansion' , 'Biomass Expansion Factors'),
        ('wood_density' , 'Wood Density Data'),
        ('allometric_equations' , 'Allometric Equations'),
    )

    Title = models.CharField(
        max_length = 100,
        verbose_name = 'Dataset Title', 
        db_column="title"
    )

    Uploaded_dataset_file = models.FileField(
        upload_to = "data_sharing",
        verbose_name='Structured dataset file (csv, json, xml)',
        blank=True,
        null=True,
        help_text="The structure must match the GlobAllomeTree API structure. Samples may be found on the right.",
        db_column="uploaded_dataset_file"
    )

    Uploaded_source_document = models.FileField(
        upload_to = "data_sharing",
        verbose_name='Source document with data in any format',
        blank=True,
        null=True,
        help_text="The source document can be a pdf, excel file, word document or other with data in any format.",
        db_column="uploaded_source_document"
    )

    Description = models.TextField(
        blank=True,
        null=True,
        verbose_name = 'Brief description',
        db_column="description"
    )

    Data_type = models.CharField(
        choices = DATA_TYPE_CHOICES,
        max_length=100,
        verbose_name = 'Type',
        db_column="data_type"
    )

    Data_as_json = models.TextField(
        blank=True,
        null=True,
        db_column="data_as_json"
    )

    Record_count = models.IntegerField(
        blank=True,
        null=True,
        db_column="record_count"
        )

    Data_license = models.ForeignKey(
        DataLicense,
        db_column="id_data_license",
        verbose_name = 'License',
    )

    Imported = models.BooleanField(
        default=False,
        help_text="If this file has been imported into the GlobAllomeTree database yet or not",
        db_column="imported"
        )

    Marked_for_import = models.BooleanField(
        default=False,
        db_column="marked_for_import"
        )

    Locked = models.BooleanField(
        default=False,
        db_column="locked"
        )

    Records_imported = models.IntegerField(
        default=0,
        db_column="records_imported"
        )

    Import_error = models.BooleanField(
        default=False,
        db_column="import_error"
        )

    Import_error_details = models.TextField(
        db_column="import_error_details",
        blank=True,
        null=True
    )

    def is_editable(self):
        if self.Data_type == 'allometric_equations' and not self.Imported:
            return True
        return False

    def get_absolute_url(self):
        return '/data/sharing/datasets/%s/' % self.pk

    def __unicode__(self):
        return self.Title

    class Meta:
        db_table = "data_dataset"


class DataSharingAgreement(BaseModel):

    AGREEMENT_STATUS_CHOICES = (
        ('pending', "Pending provider response"),
        ('granted', "Granted"),
        ('denied', "Denied")
        )

    ID_Data_sharing_agreement = models.AutoField(primary_key=True, db_column="id_data_sharing_agreement")

    User = models.ForeignKey(
        User,
        help_text="The user requesting access to the dataset",
        db_column="user_id"
    )

    Dataset = models.ForeignKey(
        Dataset, db_column="id_dataset")

    Agreement_status = models.CharField(
        max_length=15,
        choices = AGREEMENT_STATUS_CHOICES,
        db_column="agreement_status"
        )

    class Meta:
        db_table = "data_sharing_agreement"
