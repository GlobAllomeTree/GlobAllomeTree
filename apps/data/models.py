from django.db import models

class Country(models.Model):
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
	
	class Meta:
		verbose_name ='Country'
		verbose_name_plural = 'Countries'


class TreeEquation(models.Model):
	
    POPULATION_CHOICES = (
    		('Tree', 'Tree'),
      		('Sprout', 'Sprout'),
 		    ('Stand', 'Stand'),
 	)

    id_article                      = models.IntegerField(null=True, blank=True)
    id_xls_deleted_when_ready       = models.IntegerField(null=True, blank=True)
    population                      = models.CharField(max_length=50, null=True, blank=True, choices=POPULATION_CHOICES)
    ecosystem                       = models.CharField(max_length=50, null=True, blank=True)    
    country                         = models.ForeignKey(Country, blank=True, null=True)
    id_location                     = models.IntegerField(null=True, blank=True)
    group_location                  = models.NullBooleanField()
    location                        = models.CharField(max_length=50, null=True, blank=True) 
    latitude                        = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=6)
    longitude                       = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=6)
    biome_FAO                       = models.CharField(max_length=50, null=True, blank=True) 
    biome_UDVARDY                   = models.CharField(max_length=50, null=True, blank=True) 
    biome_WWF                       = models.CharField(max_length=50, null=True, blank=True) 
    division_BAILEY                 = models.CharField(max_length=50, null=True, blank=True) 
    biome_HOLDRIDGE                 = models.CharField(max_length=50, null=True, blank=True) 
    temperature                     = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=8)
    potential_evapotranspiration    = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=8)
    precipitation                   = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=8)
    sunshine_fraction               = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=8)
    wind                            = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=8)
    water_vapor_pressure            = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=8) 
    temp_MIN                        = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=8)
    temp_MAX                        = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=8)
    X                               = models.CharField(max_length=10, null=True, blank=True)
    unit_X                          = models.CharField(max_length=10, null=True, blank=True) 
    Z                               = models.CharField(max_length=10, null=True, blank=True)
    unit_Z                          = models.CharField(max_length=10, null=True, blank=True) 
    W                               = models.CharField(max_length=10, null=True, blank=True)
    unit_W                          = models.CharField(max_length=10, null=True, blank=True) 
    U                               = models.CharField(max_length=10, null=True, blank=True)
    unit_U                          = models.CharField(max_length=10, null=True, blank=True) 
    V                               = models.CharField(max_length=10, null=True, blank=True)
    unit_V                          = models.CharField(max_length=10, blank=True)
    min_X                           = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=8)
    max_X                           = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=8)
    min_H                           = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=8)
    max_H                           = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=8)
    output                          = models.CharField(max_length=20, null=True, blank=True)
    output_TR                       = models.CharField(max_length=20, null=True, blank=True)
    unit_Y                          = models.CharField(max_length=20, null=True, blank=True)
    age                             = models.CharField(max_length=20, null=True, blank=True)
    veg_component                   = models.CharField(max_length=20, null=True, blank=True)
    B                               = models.NullBooleanField()
    Bd                              = models.NullBooleanField()
    Bg                              = models.NullBooleanField()
    Bt                              = models.NullBooleanField()
    L                               = models.NullBooleanField()
    Rb                              = models.NullBooleanField()
    Rf                              = models.NullBooleanField()
    Rm                              = models.NullBooleanField()
    S                               = models.NullBooleanField()
    T                               = models.NullBooleanField()
    F                               = models.NullBooleanField()
    id_species                      = models.IntegerField(null=True, blank=True)
    genus                           = models.CharField(max_length=25, null=True, blank=True) 
    species                         = models.CharField(max_length=25, null=True, blank=True)
    group_species                   = models.IntegerField(null=True, blank=True)
    id_group                        = models.IntegerField(null=True, blank=True)
    equation_y                      = models.CharField(max_length=100, null=True, blank=True) 
    n                               = models.IntegerField(null=True, blank=True)
    top_dob                         = models.IntegerField(null=True, blank=True)
    stump_height                    = models.IntegerField(null=True, blank=True)
    id_ref                          = models.IntegerField(null=True, blank=True)
    label                           = models.CharField(max_length=10, null=True, blank=True) 
    author                          = models.CharField(max_length=100, null=True, blank=True) 
    year                            = models.IntegerField(null=True, blank=True)
    reference                       = models.TextField(null=True, blank=True) 
    r2                              = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=5)
    r_adjusted                      = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=5)
    rmse                            = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=9)
    rms                             = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=9)
    see                             = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=9)
    corrected_for_bias              = models.NullBooleanField()
    bias_correction_cf              = models.IntegerField(null=True, blank=True)
    ratio_equation                  = models.NullBooleanField()
    segmented_equation              = models.NullBooleanField()

    class Meta:
		verbose_name ='Allometric Equation'
		verbose_name_plural = 'Allometric Equations'

