from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import Journal

def journal_list(request):
 
	context =  {}
	context['journals'] = Journal.objects.all()

	return render_to_response('journals/template.list.html',  
			context_instance = RequestContext(request, context))
