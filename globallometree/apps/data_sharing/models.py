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
        ('raw_yes__derivative_no', 'The Data User is not permitted to share the Raw Data with a third Party, but is allowed to share Derivative Data.'),
        ('raw_no__derivative_no', 'The Data user is not permitted to share the Raw Data or Derivative Data to a third Party.'),
        ('raw_yes__deritive_yes', 'The Data user is permitted to share the Raw Data and Derivative Data to a third Party without informing the Data Provider.'),
        )

    EXPIRE_CHOICES = (
        ('on_activity_completion', 'When Data User has completed the activities for which the Raw Data were provided.'),
        ('on_three_months_notice', 'If either Party terminates this Agreement by notifying the other by email of its intent to terminate at least three months in advance of the effective date of termination, and indicating such termination date.'),
        ('on_date', 'On the indicated date'),
        ('none', 'No expiry'),
        )


    Data_license_ID = models.AutoField(primary_key=True)

    Title = models.CharField(
        verbose_name='License Title',
        max_length=200,
        )

    Restrictive = models.BooleanField(
        default=True,
        help_text="Normally True for custom licenses, but set to false for creative commons"
        )

    Public_choice = models.BooleanField(
        default=True,
        help_text="Should all GlobAllomeTree users have the option to choose this license when uploading data?"
        )

    License_url = models.URLField(
        verbose_name='Link to License',
        help_text="This is shown in the admin only and is mostly used for creative commons licenses",
        blank=True,
        null=True
        )

    User = models.ForeignKey(
        User,
        db_column="User_ID",
        blank=True,
        null=True
        )

    Permitted_use = models.CharField(
        max_length=100,
        choices=PERMITTED_USE_CHOICES,
        default='assessment'
    )

    Permitted_use_other_value = models.TextField(
        verbose_name="Permitted Use (Other)",
        blank=True,
        null=True
    )

    Restrict_resell = models.BooleanField(
        default=False,
        help_text="The Data User shall not sell, market, rent, lease, sublicense, lend, assign, time-share, distribute, disseminate or transfer, in whole or in part, the Raw Data, any updates, or end user's rights under this Agreement." 
    )

    Restrict_duplication = models.BooleanField(
        default=False,
        help_text="The Data User shall not duplicate the Data Provider's proprietary and copyright-protected Raw Data or attempt to do so by altering, decompiling, or disassembling the Raw Data."
    )

    Restrict_reproduction = models.BooleanField(
        default=False,
        help_text="The Data User shall not reproduce certain portions of the data for sale or any other commercial purposes with written permission of the data provider."
    )

    Restrict_derivation = models.BooleanField(
        default=False,
        help_text="The Data User shall not publish the Derivative Data without acknowledging the Data Provider.")

    Restrict_association = models.BooleanField(
        default=False,
        help_text="The Data User shall not publish the Derivative Data without associating the Data Provider as a co-author.")

    Restrict_attributed_ownership = models.BooleanField(
        default=False,
        help_text="The Data Provider shall be acknowledged as the data source. If changes are made to the Raw Data, attribution should be given to the Data Provider as owner of the Raw Data."
    )

    Restrict_other_value = models.TextField(
        verbose_name="Additional restrictions",
        blank=True,
        null=True
    )

    Expires = models.CharField(
        max_length=100,
        choices=EXPIRE_CHOICES,
        default='on_activity_completion'
    )

    Expires_on_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Expiry Date"
    )

    class Meta:
        db_table = "Data_license"

    def __unicode__(self):
        return self.Title


class Dataset(BaseModel):

    Dataset_ID = models.AutoField(primary_key=True)

    User = models.ForeignKey(
        User,
        db_column='User_ID'
    )

    DATA_TYPE_CHOICES = (
        ('raw_data' , 'Raw Data'),
#        ('biomass_expansion' , 'Biomass Expansion Factors'),
        ('wood_density' , 'Wood Density Data'),
        ('allometric_equations' , 'Allometric Equations'),
    )
  
    Title = models.CharField(
        max_length = 100,
        verbose_name = 'Dataset Title'
    )

    Uploaded_data_file = models.FileField(
        upload_to = "data_sharing",
        verbose_name='Dataset File',
        help_text="In json format"
    )

    Description = models.TextField(
        blank=True,
        null=True,
        verbose_name = 'Brief description'
    )

    Data_type = models.CharField(
        choices = DATA_TYPE_CHOICES,
        max_length=100,
        verbose_name = 'Type'
    )

    Data_as_json = models.TextField(
        blank=True,
        null=True
    )

    Record_count = models.IntegerField(
        blank=True,
        null=True
        )

    Data_license = models.ForeignKey(
        DataLicense,
        db_column="Data_license_ID",
        verbose_name = 'License'
    )

    Imported = models.BooleanField(
        default=False,
        help_text="If this file has been imported into the GlobAllomeTree database yet or not"
        )

    def __unicode__(self):
        return self.Title

    class Meta:
        db_table = "Dataset"


class DataRequest(BaseModel):

    Data_request_ID = models.AutoField(primary_key=True)

    User = models.ForeignKey(
        User,
        help_text="The user requesting access to the dataset",
        db_column="User_ID"
    )

    Dataset = models.ForeignKey(
        Dataset, db_column="Dataset_ID")

    Granted = models.NullBooleanField(
        help_text="If the owner of the data has granted access or not"
        )

    Responded = models.BooleanField(
        help_text="If the owner of the data has responded"
        )

    class Meta:
        db_table = "Data_request"
