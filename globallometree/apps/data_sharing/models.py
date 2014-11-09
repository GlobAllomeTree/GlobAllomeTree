from django.db import models
from django.contrib.auth.models import User


class DataSharingAgreement(models.Model):

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

	user = models.ForeignKey(
		User
	)

	permitted_use = models.CharField(
		max_length=100,
		choices=PERMITTED_USE_CHOICES
	)

	permitted_use_other_value = models.TextField(
		blank=True,
		null=True
	)

	restrict_other_value = models.TextField(
		blank=True,
		null=True
	)

	restrict_resell = models.BooleanField(
		default=False,
		help_text="The Data User shall not sell, market, rent, lease, sublicense, lend, assign, time-share, distribute, disseminate or transfer, in whole or in part, the Raw Data, any updates, or end user's rights under this Agreement." 
	)

	restrict_duplication = models.BooleanField(
		default=False,
		help_text="The Data User shall not duplicate the Data Provider's proprietary and copyright-protected Raw Data or attempt to do so by altering, decompiling, or disassembling the Raw Data."
	)

	restrict_reproduction = models.BooleanField(
		default=False,
		help_text="The Data User shall not reproduce certain portions of the data for sale or any other commercial purposes with written permission of the data provider."
	)

	restrict_derivation = models.BooleanField(
		default=False,
		help_text="The Data User shall not publish the Derivative Data without acknowledging the Data Provider.")

	restrict_attribution = models.BooleanField(
		default=False,
		help_text="The Data User shall not publish the Derivative Data without associating the Data Provider as a co-author.")

	restrict_attributed_ownership = models.BooleanField(
		default=False,
		help_text="The Data Provider shall be acknowledged as the data source. If changes are made to the Raw Data, attribution should be given to the Data Provider as owner of the Raw Data."
	)

	expires = models.CharField(
		max_length=100,
		choices=EXPIRE_CHOICES
	)

	expire_on_date = models.DateField(
		blank=True,
		null=True
	)


class DataSet(models.Model):

	user = models.ForeignKey(
		User
	)

	DATA_TYPE_CHOICES = (
		('biomass' , 'Biomass Data'),
		('biomass_expansion' , 'Biomass Expansion Factors'),
		('wood_density' , 'Wood Density Data'),
	)

	title = models.CharField(
		max_length = 100
	)

	description = models.TextField(
		blank=True,
		null=True
	)

	uploaded_data_file = models.FileField(
		upload_to = "data_sharing"
	)

	data_type = models.CharField(
		choices = DATA_TYPE_CHOICES,
		max_length=100
	)

	is_restricted = models.BooleanField(
		default=False
	)

	agreement = models.ForeignKey(
		DataSharingAgreement,
		blank=True,
		null=True
	)


