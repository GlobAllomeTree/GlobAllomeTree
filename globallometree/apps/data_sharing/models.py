from django.db import models
from django.contrib.auth.models import User
from globallometree.apps.common.models import BaseModel

class DataSharingAgreement(BaseModel):

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
		('on_three_months_notice', 'If either Party terminates this Agreement by notifying the other by email of its intent to terminate at least three months in advance of the effective date of termination, and indicating suchtermination date.'),
		('on_date', 'On the indicated date'),
	)

	User = models.ForeignKey(
		User
	)

	Permitted_use = models.CharField(
		max_length=100,
		choices=PERMITTED_USE_CHOICES
	)

	Permitted_use_other_value = models.TextField(
		blank=True,
		null=True
	)

	Restrict_other_value = models.TextField(
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

	Restrict_attribution = models.BooleanField(
		default=False,
		help_text="The Data User shall not publish the Derivative Data without associating the Data Provider as a co-author.")

	Restrict_attributed_ownership = models.BooleanField(
		default=False,
		help_text="The Data Provider shall be acknowledged as the data source. If changes are made to the Raw Data, attribution should be given to the Data Provider as owner of the Raw Data."
	)

	Expires = models.CharField(
		max_length=100,
		choices=EXPIRE_CHOICES
	)

	Expires_on_date = models.DateField(
		blank=True,
		null=True
	)


class DataSet(BaseModel):

	User = models.ForeignKey(
		User
	)

	DATA_TYPE_CHOICES = (
		('biomass' , 'Biomass Data'),
		('biomass_expansion' , 'Biomass Expansion Factors'),
		('wood_density' , 'Wood Density Data'),
	)

	Title = models.CharField(
		max_length = 100
	)

	Description = models.TextField(
		blank=True,
		null=True
	)

	Uploaded_data_file = models.FileField(
		upload_to = "data_sharing",
		blank=True,
		null=True
	)

	Data_type = models.CharField(
		choices = DATA_TYPE_CHOICES,
		max_length=100
	)

	Is_restricted = models.BooleanField(
		default=False
	)

	Agreement = models.ForeignKey(
		DataSharingAgreement,
		blank=True,
		null=True
	)

	Imported = models.BooleanField(
		default=False,
		help_text="If this file has been imported into the GlobAllomeTree database yet or not"
		)


class DataAccessRequest(BaseModel):

	User = models.ForeignKey(
		User,
		help_text="The user requesting access to the dataset"
	)

	Data_set = models.ForeignKey(
		DataSet)

	Granted = models.NullBooleanField(
		help_text="If the owner of the data has granted access or not"
		)

	Responded = models.BooleanField(
		help_text="If the owner of the data has responded"
		)

