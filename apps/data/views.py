import csv
import json

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import slugify

from haystack.views import SearchView
from haystack.query import SearchQuerySet

from django.template import RequestContext


from .models import TreeEquation, Country


def continents_map(request):
    return render_to_response('continents_map.html',
                              context_instance = RequestContext(request,
                              {'is_page_data': True, }))

def tree_equation_id(request, id):
    tree_equation = TreeEquation.objects.get(id=id)
    return render_to_response('data/template.tree_equation.html', 
                              context_instance = RequestContext(request,
                              {'tree_equation': tree_equation, 
                               'is_page_data' : True})) 

def geo_map(request):
    country_list = TreeEquation.objects.values_list('country__common_name',flat=True).distinct
    return render_to_response('geo_map.html',
                               context_instance = RequestContext(request,
                                {'country_list': country_list,
                                 'is_page_data' : True }))

def geo_map_id(request, geo_id):
    country = Country.objects.get(iso_3166_1_2_letter_code = geo_id)
    return HttpResponseRedirect('/data/search/?country=' + country.common_name)
    
def database(request):
    return render_to_response('database.html',
                              context_instance = RequestContext(request,
                             {'is_page_data' : True}))


def species(request, selected_genus=None):
    
    #Call sorl for a faceted list of genus
    sqs = SearchQuerySet().facet('genus')
    genus_list = []
    for genus_count in sqs.facet_counts()['fields']['genus']:
        genus_list.append({
            'name'  : genus_count[0],
            'count' : genus_count[1]
        
        })
    
    #Sort the list alphabetically by name
    genus_list.sort(key=lambda x : x['name'])
    
    return render_to_response('data/template.species.html', 
                               context_instance = RequestContext(request,
                               {'genus_list': genus_list,
                               'is_page_data' : True }))




class EquationSearchView(SearchView):

    
    def __name__(self):
        return "EquationSearchView"

    def extra_context(self):
        return {'is_page_data' : True}

def autocomplete(request, field): 
    term    = request.GET.get('term') 
    sqs     = SearchQuerySet()
    
    kwargs = {field + '_auto':term} #ex) country_auto for the autocomplete index of country
    sqs    = SearchQuerySet().facet(field).filter(**kwargs)

    result_counts = sqs.facet_counts()['fields'][field]
    result_list = []

    for result_count in result_counts:

        if len(result_count[0]) > 120:
            display_value = result_count[0][0:120] + '...'
        else:
            display_value = result_count[0]

        result_list.append({
            'value'  : result_count[0],
            'display_value': display_value,
            'count'  : result_count[1]
        })

    return HttpResponse(json.dumps(result_list))

from .forms import EquationSearchForm
def export(request):
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accouts/login/')

    form = EquationSearchForm(request.GET)
    sqs = form.search()
   
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=tree_equations.csv'
    writer = csv.writer(response)
    # Write headers to CSV file
    headers = []
    for field in TreeEquation._meta.fields:
        headers.append(field.name)
    writer.writerow(headers)
    # Write data to CSV file
    
    for result in sqs:
        obj = TreeEquation.objects.get(pk=result.id)
        row = []
        for field in TreeEquation._meta.fields:
            row.append(unicode(getattr(obj, field.name)).encode("utf-8"))
        writer.writerow(row)
    return response

""" Sample code for json search
from .forms import EquationSearchForm
import json
def json_search(request):
    form = EquationSearchForm(request.GET)
    sqs = form.search()
    result_list = []
    for result in sqs:
        result_list.append({'id' : result.id,
                            'country' : result.country,
                            'species' : result.species,
                            'equation' : result.equation_y
                            })
    result_obj = {
        'results' : result_list
    }

    return HttpResponse(json.dumps(result_obj))
"""