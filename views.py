from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

def start_page(request):
    return render_to_response('home.html',{'': '', })

def docs(request):
    return render_to_response('docs.html',{'': '', })

def links(request):
    return render_to_response('links.html',{'': '', })

def principles(request):
    return render_to_response('principles.html',{'': '', })

def software(request):
    return render_to_response('software.html',{'': '', })
