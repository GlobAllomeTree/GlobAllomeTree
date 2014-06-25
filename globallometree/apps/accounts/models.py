
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import mail_managers, send_mail
from django.db import models

from globallometree.apps.locations.models import Country

#Monkey patch the User class for django 1.6
def get_profile(self):
    if not hasattr(self, 'profile'):
        self.profile = self.profile_set.all()[0]
    return self.profile
User.get_profile = get_profile
class UserProfile(models.Model):
    DATA_MAY_PROVIDE_CHOICES = (('no_data',             'No data available'),
                                ('Species_data',        'Species data'),
                                ('wood_density',        'Wood Density'),
                                ('allometric_equation', 'Allometric Equation'),
                                ('reports',             'Reports and scientific literature containing new allometric equations'),
                                ('biomass_factors',     'Biomass Expansion Factors'),
                                ('volume_tables',       'Volume Tables'),
                                )


    LOCATION_PRIVACY_CHOICES = (('none', "Private - Don't share my location at all"),
                                ('anonymous', "Anonymous - Share my location anonymously"),
                                ('public', "Public - Share my location with my profile information"),)

    user        = models.ForeignKey(User)
    address     = models.CharField(max_length=200)
    country     = models.CharField(max_length=80, blank=True)
    region      = models.CharField(max_length=80, blank=True)
    subregion   = models.CharField(max_length=80, blank=True)
    
    education   = models.CharField(max_length=300, blank=True)

    institution_name      = models.CharField(max_length=200, blank=True)
    institution_address   = models.CharField(max_length=200, blank=True)
    institution_phone     = models.CharField(max_length=60, blank=True)
    institution_fax       = models.CharField(max_length=60, blank=True)
    field_subject         = models.CharField(max_length=60, blank=True)

    data_may_provide      = models.CharField(max_length=40, choices=DATA_MAY_PROVIDE_CHOICES, blank=True)

    location_latitude     = models.DecimalField(
        null=True, blank=True, max_digits=8, decimal_places=5
    )
    location_longitude     = models.DecimalField(
        null=True, blank=True, max_digits=8, decimal_places=5
    )
    location_country     = models.ForeignKey(Country, blank=True, null=True)

    location_privacy  = models.CharField(max_length=20, default='anonymous', choices=LOCATION_PRIVACY_CHOICES)

    def __unicode__(self):
        return u"User profile for %s" % self.user


# Notify a user their status has changed to active
@receiver(pre_save, sender=User)
def user_pre_save(sender, instance, signal, *args, **kwargs):

    try:
        #instance is the record about to be saved
        #compare user is the record in the db
        compare_user = User.objects.get(pk=instance.id)
    except:
        #returns if user is new or fixture is being loaded
        return
    
    if compare_user.is_active != instance.is_active and instance.is_active == True:
        #Mail the admin
        mail_managers('GlobAllomeTree New User "%s" APPROVED' % instance.username,
                      """
Dear GlobAllomeTree Admin,

A new user has been correctly approved for your website.

You can view the user's information here:
Django User
http://globallometree.org/admin/auth/user/%s/
User Profile
http://globallometree.org/admin/accounts/userprofile/%s/

""" % (instance.id, instance.get_profile().id),
                     fail_silently=False)
        
        #Mail the new user
        send_mail('GlobAllomeTree  account "%s" approved!' % instance.username,
                      """
Dear %s,

Your account has been approved at www.globallometree.org

You may login at the following link:

http://www.globallometree.org/accounts/login/

""" % instance.username, 
                    'no-reply@globallometree.org',
                     [instance.email], 
                     fail_silently=False)
            
   
    
    
