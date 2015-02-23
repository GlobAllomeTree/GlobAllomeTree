from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from .models import Journal

def list(request):
    journals = Journal.objects.all()

    return render_to_response(
        'list.html',  
        context_instance = RequestContext(request,{
            'journals': journals,
            'is_page_community' : True
        })
    )

def detail(request, journal_id):
    try:
        journal = Journal.objects.get(pk=journal_id)

    except Journal.DoesNotExist:
        raise Http404
    return render_to_response(
        'detail.html',
        context_instance = RequestContext(request,{
            'journal': journal,
            'is_page_community': True
        })
    )
