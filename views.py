from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from django.template import RequestContext


def start_page(request):
    return render_to_response('home.html', context_instance = RequestContext(request, {'': '', }))

def docs(request):
    return render_to_response('docs.html',context_instance = RequestContext(request,{'': '', }))

def links(request):
    return render_to_response('links.html',context_instance = RequestContext(request,{'': '', }))

def principles(request):
    return render_to_response('principles.html',context_instance = RequestContext(request,{'': '', }))

def software(request):
    return render_to_response('software.html',context_instance = RequestContext(request,{'': '', }))
