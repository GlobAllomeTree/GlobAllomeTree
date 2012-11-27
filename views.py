from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from django.template import RequestContext


def start_page(request):
    return render_to_response('home.html', 
    	                       context_instance = RequestContext(request, 
    	                       {'is_page_home': True }))

def docs(request):
    return render_to_response('docs.html',
    					      context_instance = RequestContext(request,
    					      {'is_page_docs': True }))

def contributors(request):
    return render_to_response('contributors.html',
    					       context_instance = RequestContext(request,
    					       {'is_page_contributors': True, }))

def principles(request):
    return render_to_response('principles.html',
    						  context_instance = RequestContext(request,
    						  {'is_page_principles': True, }))

def software(request):
    return render_to_response('software.html',
    					      context_instance = RequestContext(request,
    					      {'is_page_software': True, }))

def about(request):
    return render_to_response('about.html',
    						 context_instance = RequestContext(request,
    						 {'is_page_about': True }))





