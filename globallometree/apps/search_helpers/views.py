import json
import re
from decimal import Decimal
import cStringIO as StringIO
import xhtml2pdf.pisa as pisa

from django.conf import settings
from django.views.generic import TemplateView

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

from apps.locations.models import Country
from apps.accounts.mixins import RestrictedPageMixin


class LinkedModelSearchView(RestrictedPageMixin, TemplateView):
    template_name = 'search_helpers/template.search.html'

    def get_context_data(self, **kwargs):
        context = super(LinkedModelSearchView, self).get_context_data(**kwargs)

        self.form = self.form_class(self.request.GET)
    	
        context['form'] = self.form

        #This is for the menu
        context['is_page_data'] =  True
        context['search_title'] = self.search_title
        context['form_template'] = self.form_template
        context['configuration_js_file'] = self.configuration_js_file

        if self.form.is_valid():
            context['form_is_valid'] = True
            context['current_search_summary'] = self.current_search_summary()
            context['search_dict'] = json.dumps(self.get_search_dict());
            context['country_centroids'] = json.dumps(self.get_country_centroids());
        else:
            context['form_is_valid'] = False
            
        return context

    def get_country_centroids(self):
        countries = {}
        for country in Country.objects.all():
            if country.Iso3166a3:
                countries[country.Iso3166a3] = {
                    'latitude' : str(country.Centroid_latitude),
                    'longitude' : str(country.Centroid_longitude),
                    'common_name' : str(country.Common_name)
                }
            else:
                print "MISSING COUNTRY 3166 3 for Country %s!" % country.common_name
        return countries

    def create_response(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        return super(SearchView, self).create_response( *args, **kwargs)

    def get_search_dict(self, safe=False):
        search_dict = {}
        if self.form.is_valid():
            for field in self.form.cleaned_data:
                if self.form.cleaned_data.get(field, None) not in [None, '']:
                    value = self.form.cleaned_data.get(field)
                    #Handle decimal types which don't have unicode casting
                    #and instead use string
                    if hasattr(value, '__unicode__'):
                        value = unicode(value)
                    elif type(value) == Decimal:
                        value = str(value)
                    search_dict[field] = value;
        return search_dict

    def current_search_summary(self):
        current_search = []
        if not self.form.is_valid():
            return []
        #Send search fields to the the sqs.filter
        for field in self.form.cleaned_data:
        
            if field in ['order_by','Point_Latitude', 'Point_Longitude']:
                continue

            if self.form.cleaned_data.get(field, None) not in [None, '']:
                if field == 'Point_Distance':
                    latitude = self.form.cleaned_data.get('Point_Latitude')
                    longitude = self.form.cleaned_data.get('Point_Longitude')
                    distance = self.form.cleaned_data.get('Point_Distance')
                    summary = "%s km from %s and %s " % (distance, latitude, longitude)

                    current_search.append( {'field' : 'Distance From Point',
                                            'search_value' :  summary,
                                            'clear_link'   :  self.get_query_string({ 'Point_Latitude' : None,
                                                                                      'Point_Longitude' : None,
                                                                                      'Point_Distance' : None,
                                                                                     })
                                        })
                else: 
                    current_search.append( {'field' : self.form.fields[field].label,
                                            'search_value' :  self.form.cleaned_data.get(field),
                                            'clear_link'   :  self.get_query_string({ field : None})
                                        })
        return current_search     
 
    def export_link(self):
        return self.get_query_string(export=True)

    def get_query_string(self, using_values = {}, export=False):
    
        query_dict = self.get_search_dict()
        query_string = ''
        first = True
       
        for field in using_values.keys():
            if using_values[field] is None:
                del query_dict[field]
            else:
                query_dict[field] = using_values[field]
            
        if export and 'page' in query_dict.keys():
            del query_dict['page']
        
        for field in query_dict.keys():
            if first:
                c = '?'
                first = False
            else:
                c = '&'
                
            query_string += '%s%s=%s' % (c, field, query_dict[field])
          
        if not len(query_string):
            query_string = '?'

        return query_string


def record_by_id_view(request, id, model_class, template_path):
    record = model_class.objects.get(pk=id)
    return render_to_response(
        '%s/template.record.html' % template_path, 
        context_instance = RequestContext(
            request, {
                'record': record, 
                'is_page_data' : True
            }
        )
    ) 

def record_by_id_pdf_view(request, id, model_class, template_path):
    record = model_class.objects.get(pk=id)

    template = get_template('%s/template.record.pdf.html' % template_path)

   
    html = template.render(Context({
        'record': record
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


def export_view(request, filename):
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
    response['Content-Disposition'] = 'attachment; filename=%s.json' % filename
    return response
