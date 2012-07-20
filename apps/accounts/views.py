
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect

from . import forms

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def register(request):
    
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        
        if form.is_valid():
            form.save()
            #login user
            login_user = authenticate(username=request.POST.get('username'), password=request.POST.get('password1'))
            login(request, login_user)
            return HttpResponseRedirect('/')
    else:
        # neither POST nor GET with key
        form = forms.RegistrationForm() 
    
    return render_to_response('accounts/account_register.html',
                             {'form': form},
                               context_instance=RequestContext(request))
    


