from django.db import models
from django.contrib.auth.models import User
from globallometree.apps.common.models import DataReference, Institution


class Population(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Ecosystem(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Submission(models.Model):
    submitted_file = models.FileField(upload_to='data_submissions') # TODO: check if is better a more specific folder
    submitted_notes = models.TextField(blank=True, null=True)
    date_uploaded = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User)
    imported = models.BooleanField()

    def __unicode__(self):
        return u"%s by %s" % (self.submitted_file, self.user)


class AllometricEquation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, verbose_name="Last modified")
    
    ID = models.IntegerField(primary_key=True)
    IDequation = models.IntegerField(null=True, blank=True) 

    X = models.CharField(max_length=20, null=True, blank=True)
    Unit_X = models.CharField(max_length=20, null=True, blank=True)
    Z = models.CharField(max_length=20, null=True, blank=True)
    Unit_Z = models.CharField(max_length=20, null=True, blank=True)
    W = models.CharField(max_length=20, null=True, blank=True)
    Unit_W = models.CharField(max_length=20, null=True, blank=True)
    U = models.CharField(max_length=20, null=True, blank=True)
    Unit_U = models.CharField(max_length=20, null=True, blank=True)
    V = models.CharField(max_length=20, null=True, blank=True)
    Unit_V = models.CharField(max_length=20, blank=True)
    Min_X = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    Max_X = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    Min_Z = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    Max_Z = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    Output = models.CharField(max_length=30, null=True, blank=True)
    Output_TR = models.CharField(max_length=30, null=True, blank=True)
    Unit_Y = models.CharField(max_length=50, null=True, blank=True)
    Age = models.CharField(max_length=50, null=True, blank=True)
    Veg_Component = models.CharField(max_length=150, null=True, blank=True)
    B = models.NullBooleanField()
    Bd = models.NullBooleanField()
    Bg = models.NullBooleanField()
    Bt = models.NullBooleanField()
    L = models.NullBooleanField()
    Rb = models.NullBooleanField()
    Rf = models.NullBooleanField()
    Rm = models.NullBooleanField()
    S = models.NullBooleanField()
    T = models.NullBooleanField()
    F = models.NullBooleanField()
    Equation = models.CharField(max_length=500, null=True, blank=True) 
    Substitute_equation = models.CharField(
        max_length=500, null=True, blank=True
    ) 
    Top_dob = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    Stump_height = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    R2 = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    R2_Adjusted = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    RMSE = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    SEE = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    Corrected_for_bias = models.NullBooleanField()
    Bias_correction = models.DecimalField(
        null=True, blank=True, max_digits=16, decimal_places=10
    )
    Ratio_equation = models.NullBooleanField()
    Segmented_equation = models.NullBooleanField()
    Sample_size = models.CharField(max_length=150, null=True, blank=True)
    
    population = models.ForeignKey(
        Population, blank=True, null=True
    )
    ecosystem = models.ForeignKey(
        Ecosystem, blank=True, null=True
    )

    species_group = models.ForeignKey('taxonomy.SpeciesGroup',null=True, blank=True)
    location_group = models.ForeignKey('locations.LocationGroup',null=True, blank=True)

    ID_REF = models.IntegerField(null=True, blank=True) 
    reference = models.ForeignKey(
        DataReference, blank=True, null=True
    )

    contributor = models.ForeignKey(
        Institution, blank=True, null=True
    )

    Name_operator = models.CharField(max_length=150, null=True, blank=True)
    data_submission = models.ForeignKey(
        Submission, blank=True, null=True
    )

    def components_string(self):
        c_string = ''
        for field in ['B', 'Bd', 'Bg', 'Bt', 'L', 'Rb', 'Rf', 'Rm', 'S', 'T', 'F']:
            if getattr(self, field):
                c_string += field + ' '
        return c_string

    def get_absolute_url(self):
        return '/data/equation/%s' % self.ID


    def unicode(self):
        return 'Equation %s' % self.ID

    class Meta:
        verbose_name ='Allometric Equation'
        verbose_name_plural = 'Allometric Equations'
