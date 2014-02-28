from django.db import models
from django.contrib.auth.models import User

class AllometricEquation(models.Model):
    ID = models.IntegerField(primary_key=True)
    data_submission = models.ForeignKey(DataSubmission, blank=True, null=True)
    IDequation = models.IntegerField(null=True, blank=True)
    Population = models.CharField(max_length=255, null=True, blank=True)
    Ecosystem = models.CharField(max_length=255, null=True, blank=True)
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
    ID_REF = models.IntegerField(null=True, blank=True)
    Label = models.CharField(max_length=20, null=True, blank=True) 
    Author = models.CharField(max_length=200, null=True, blank=True) 
    Year = models.CharField(max_length=12, null=True, blank=True) 
    Reference = models.TextField(null=True, blank=True) 
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
    Contributor = models.CharField(max_length=150, null=True, blank=True) 
    Name_operator = models.CharField(max_length=150, null=True, blank=True)
    species = models.ManyToManyField(Species)
    ID_Group = models.IntegerField(null=True, blank=True)
    locations = models.ManyToManyField(Location)

    def components_string(self):
        c_string = ''
        for field in ['B', 'Bd', 'Bg', 'Bt', 'L', 'Rb', 'Rf', 'Rm', 'S', 'T', 'F']:
            if getattr(self, field):
                c_string += field + ' '
        return c_string

    def get_absolute_url(self):
        return '/data/equation/%s' % self.ID

    class Meta:
        verbose_name ='Allometric Equation'
        verbose_name_plural = 'Allometric Equations'

class DataSubmission(models.Model):
    submitted_file = models.FileField(upload_to='data_submissions')
    submitted_notes = models.TextField(blank=True, null=True)
    date_uploaded = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User)
    imported = models.BooleanField()

    def __unicode__(self):
        return u"%s by %s" % (self.submitted_file, self.user)
