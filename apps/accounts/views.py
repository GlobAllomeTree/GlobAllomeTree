
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect

from . import forms

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail

def register(request):
    
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            #To log in the user automatically uncomment the following two lines
            #login_user = authenticate(username=request.POST.get('username'), password=request.POST.get('password1'))
            #login(request, login_user)
            
            #The next lines require an admin to approve the user
            user.is_active = False
            user.save()
            
            
            
            send_mail('Globallometree New User "%s" requires approval' % user.username,
                      """
Dear Globallometree Admin,

A new user has registered for your website. This user needs your approval to log in.

To allow the user to log in you can follow these steps:

1) Go to the link: http://globallometree.com/admin/auth/user/%s/
2) Click the active checkbox on the user settings
3) Click save
4) The user will be automatically notified their account has been activated
                                              

""" % user.id, 
                    'no-reply@globallometree.com',
                     [settings.NEW_USER_NOTIFY_EMAIL], 
                     fail_silently=False)
            
            return HttpResponseRedirect('/accounts/approval-pending/')
    else:
        
        # neither POST nor GET with key
        form = forms.RegistrationForm() 
    
    return render_to_response('accounts/account_register.html',
                             {'form': form},
                               context_instance=RequestContext(request))
    

def approval_pending(request):
    
    return render_to_response('accounts/account_approval_pending.html',
                               context_instance=RequestContext(request))
    

