from django.db import models

class country(models.Model):
	common_name = models.CharField(max_length=159, blank=True)
	formal_name = models.CharField(max_length=159, blank=True)
	type = models.CharField(max_length=69, blank=True)
	sub_type = models.CharField(max_length=102, blank=True)
	sovereignty = models.CharField(max_length=72, blank=True)
	capital = models.CharField(max_length=234, blank=True)
	iso_4217_currency_code = models.CharField(max_length=33, blank=True)
	iso_4217_currency_name = models.CharField(max_length=42, blank=True)
	telephone_code = models.CharField(max_length=48, blank=True)
	iso_3166_1_2_letter_code = models.CharField(max_length=6, blank=True)
	iso_3166_1_3_letter_code = models.CharField(max_length=9,blank=True)
	iso_3166_1_number = models.IntegerField(null=True, blank=True)
	iana_country_code_tld = models.CharField(max_length=33, blank=True)

	def __unicode__(self):
		return self.common_name



