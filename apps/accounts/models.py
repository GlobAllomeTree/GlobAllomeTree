
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail

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
        send_mail('Globallometree New User "%s" APPROVED' % instance.username,
                      """
Dear Globallometree Admin,

A new user has been correctly approved for your website.

You can view the user's information here:

http://globallometree.com/admin/auth/user/%s/


""" % instance.id, 
                    'no-reply@globallometree.com',
                     [settings.NEW_USER_NOTIFY_EMAIL], 
                     fail_silently=False)
        
        #Mail the new user
        send_mail('Globallometree  account "%s" approved!' % instance.username,
                      """
Dear %s,

Your account has been approved at globallometree.com

You may login at the following link:

http://globallometree.com/accounts/login/


""" % instance.username, 
                    'no-reply@globallometree.com',
                     [instance.email], 
                     fail_silently=False)
            
   
    
    
