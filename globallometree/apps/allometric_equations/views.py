import json

import cStringIO as StringIO
import xhtml2pdf.pisa as pisa

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.core.mail import mail_managers
from django.conf import settings
from django.db import connection
from django.views.generic.edit import FormView

#Get the elasticutils objects configured from settings.py
from elasticutils.contrib.django import get_es

from .forms import SubmissionForm
from .models import AllometricEquation

from apps.common.kill_gremlins import kill_gremlins
from apps.locations.models import Country

from apps.accounts.mixins import RestrictedPageMixin


class SubmissionView(FormView):
    template_name = 'allometric_equations/template.submit_data.html'
    form_class = SubmissionForm
    success_url = '/allometric-equations/submit/complete/'

    def form_valid(self, form):      
        ds = AllometricEquationSubmission()
        ds.submitted_file = form.cleaned_data['file']
        ds.submitted_notes = form.cleaned_data['notes']
        ds.user = self.request.user
        ds.imported = False
        ds.save()
        mail_managers('New GlobAllomeTree Allometric Equations Submission', """

A new data file has been submitted to http://www.globallometree.org/ 

It was submitted by the user %s

To review this file and import it, please go to:

http://www.globallometree.org/admin/allometric_equations/submission/%s/
            """ % (ds.user, ds.id)) 

        return super(SubmissionView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SubmissionView, self).get_context_data(**kwargs)
        context['is_page_data'] = True
        context['export_encoding'] = settings.DATA_EXPORT_ENCODING_NAME
        return context


class SubmissionCompleteView(TemplateView):
    template_name = 'allometric_equations/template.submit_data_complete.html'

    def get_context_data(self, **kwargs):
        context = super(SubmissionCompleteView, self).get_context_data(**kwargs)
        context['is_page_data'] = True

        return context


@login_required(login_url='/accounts/login/')
def allometric_equation_id(request, id):
    allometric_equation = AllometricEquation.objects.get(pk=id)
    return render_to_response(
        'allometric_equations/template.allometric_equation.html', 
        context_instance = RequestContext(
            request, {
                'allometric_equation': allometric_equation, 
                'is_page_data' : True
            }
        )
    ) 


@login_required(login_url='/accounts/login/')
def allometric_equation_id_pdf(request, id):
    allometric_equation = AllometricEquation.objects.get(pk=id)

    template = get_template('allometric_equations/template.allometric_equation.pdf.html')

   
    html = template.render(Context({
        'allometric_equation': allometric_equation
    }))

    def fetch_resources(uri, rel):
        path = 'ERROR'
        if uri[0:6] == 'static':
            path = settings.STATIC_ROOT + uri[6:]
        elif uri[0:5] == 'media':
            path = settings.MEDIA_ROOT + uri[5:]
        print uri, path
        return path

    buffer = StringIO.StringIO()
    pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
                      buffer,
                      link_callback=fetch_resources)

    pdf = buffer.getvalue()
    buffer.close()
    
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=AllometricEquation_%s.pdf' % allometric_equation.ID

    response.write(pdf)
    return response


@login_required(login_url='/accounts/login/')
def export(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    # Here we take the query that was generated client side and
    # pass it to elasicsearch on the server to facilitate an easy
    # way for the browser to download
    # We also strip it down to make the json more useful for researchers
    query = json.loads(request.POST.get('query'))
    #Try to prevent any obvious hacking attempts
    assert query.keys() == [u'query', u'from', u'size']
    assert query['size'] <= 1000
    assert query['from'] == 0
    es = get_es(urls=settings.ES_URLS)
    result = es.search(body=query)
    cleaned = []
    for hit in result['hits']['hits']:
        del hit['_source']['has_precise_location']
        cleaned.append(hit['_source'])
    json_dump = json.dumps(cleaned, indent=4)
    response = HttpResponse(json_dump)
    response['Content-Disposition'] = 'attachment; filename=allometric_equations.json'
    return response
