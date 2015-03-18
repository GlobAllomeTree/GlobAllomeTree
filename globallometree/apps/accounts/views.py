from django.contrib.auth.models import User
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.urlresolvers import reverse

from . import forms
from . import models

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import mail_managers
from rest_framework.authtoken.models import Token
from django.views.generic import DetailView, UpdateView
from .models import UserProfile
from .forms import UserProfileForm





def register(request):
    
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], 
                                            form.cleaned_data['email'],
                                            form.cleaned_data['password1'])

            
            #To log in the user automatically uncomment the following two lines
            #login_user = authenticate(username=request.POST.get('username'), password=request.POST.get('password1'))
            #login(request, login_user)
            
            #The next lines require an admin to approve the user and add the first + last name
            user.first_name = form.cleaned_data['first_name'] 
            user.last_name = form.cleaned_data['last_name'] 
            user.is_active = False
            user.save()
            
            user_profile = models.UserProfile(user=user,
                                              address=form.cleaned_data['address'],
                                              location_country=form.cleaned_data['country'],
                                              subregion=form.cleaned_data['subregion'],
                                              region=form.cleaned_data['region'],
                                              education=form.cleaned_data['education'],
                                              institution_name=form.cleaned_data['institution_name'],
                                              institution_address=form.cleaned_data['institution_address'],
                                              institution_phone=form.cleaned_data['institution_phone'],
                                              institution_fax=form.cleaned_data['institution_fax'],
                                              field_subject=form.cleaned_data['field_subject'],
                                              data_may_provide=form.cleaned_data['data_may_provide'],
                                              privacy=form.cleaned_data['privacy']
                                              )
            user_profile.save()
             
            mail_managers('GlobAllomeTree New User "%s" requires approval' % user.username,
                      """
Dear GlobAllomeTree Admin,

A new user has registered for your website. This user needs your approval to log in.

To allow the user to log in you can follow these steps:

1) Go to the new Django User: http://www.globallometree.org/admin/auth/user/%s/
2) Click the active checkbox on the user settings
3) Click save
4) The user will be automatically notified their account has been activated


You may also view the new user's profile at:
http://www.globallometree.org/admin/accounts/userprofile/%s/
                                              

""" % (user.id, user.get_profile().id), 
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


class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'accounts/user_profile.html'
    context_object_name = 'userprofile'

    def get_absolute_url(self):
        return reverse('userprofile_detail', kwargs={'pk': self.pk})

    def dispatch(self, request, *args, **kwargs):
        """Overriding to ensure PK is present"""
        if 'pk' not in kwargs:
            self.kwargs['pk'] = self.request.user.get_profile().pk
        return super(UserProfileDetailView, self).dispatch(
            request, *args, **kwargs
        )

class MyProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'accounts/my_profile.html'
    context_object_name = 'userprofile'

    def get_absolute_url(self):
        return reverse('myprofile_detail', kwargs={'pk': self.pk})

    def dispatch(self, request, *args, **kwargs):
        """Overriding to ensure PK is present"""
        if 'pk' not in kwargs:
            self.kwargs['pk'] = self.request.user.get_profile().pk
        return super(MyProfileDetailView, self).dispatch(
            request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        context = super(MyProfileDetailView, self).get_context_data(**kwargs)
        context['token'] = Token.objects.get_or_create(
            user=context['userprofile'].user)[0]
        return context


class UserProfileUpdateView(UpdateView):
    form_class = UserProfileForm
    model = UserProfile
    template_name = 'accounts/user_profile_update.html'
    context_object_name = 'userprofile'


    def dispatch(self, request, *args, **kwargs):
        """Overriding to ensure PK is present"""
        if 'pk' not in kwargs:
            self.kwargs['pk'] = self.request.user.get_profile().pk
        return super(UserProfileUpdateView, self).dispatch(
            request, *args, **kwargs
        )

    def get_success_url(self):
        if self.request.user != self.object.user:
            url = reverse(
                'userprofile_update_admin',
                kwargs={'pk':self.object.pk}
            )
        else:
            url = reverse('userprofile_detail')

        return url

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(UserProfileUpdateView, self).get_initial()
        initial['email'] = self.request.user.email
        return initial

# def my_profile(request, user_id=0):
#     if (user_id == 0):
#         get_user = request.user
#         user_token = Token.objects.get_or_create(user=request.user)
#         return render_to_response('accounts/my_profile.html',
#                                   context_instance=RequestContext(request,
#                                   {"requested_user": get_user,
#                                   "token": user_token[0],
#                                   "profile": request.user.get_profile()}))
#     else:
#         get_user = get_object_or_404(User, id=user_id)
#         get_user_profile = User.objects.get(id=user_id).get_profile()
#         return render_to_response('accounts/my_profile.html',
#                                   context_instance=RequestContext(request,
#                                   {"requested_user": get_user,
#                                   "profile": get_user_profile}))

