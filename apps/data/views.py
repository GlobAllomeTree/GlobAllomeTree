import csv

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.defaultfilters import slugify

from haystack.views import SearchView
from haystack.query import SearchQuerySet

from .models import TreeEquation


def continents_map(request):
    return render_to_response('continents_map.html',{'': '', })

def TreeEquation_id(request,DB_id):
    DB_object = TreeEquation.objects.get(id=DB_id)
    return render_to_response('TreeEquation_id.html', {'DB_object': DB_object, }) 

def geo_map(request):
    country_list = TreeEquation.objects.values_list('country__common_name',flat=True).distinct
    return render_to_response('geo_map.html', {'country_list': country_list, })

def geo_map_id(request, geo_id):
    country_DB = TreeEquation.objects.filter(country__iso_3166_1_2_letter_code = geo_id )
    return render_to_response('country_DB.html', {'country_DB': country_DB, })

def database(request):
    return render_to_response('database.html',{'': '', })

def export_db(request):
    # get the response object, this can be used as a stream.
    response = HttpResponse(mimetype='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename = "export.csv"'
    # the csv writer
    writer = csv.writer(response)
    fanta_objects = TreeEquation.objects.all()
    writer.writerow(['id_article', 'population', 'genus', 'species', 'ecosystem', 'temperature', 'country'])  
    for data in fanta_objects:
        writer.writerow([data.id_article, data.population, data.genus, data.species, unicode(data.ecosystem).encode("utf-8"), data.temperature, data.country_id])
    return response

def export_db_all(request,db_id):
    model = TreeEquation
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % slugify(model.__name__)
    writer = csv.writer(response)
    # Write headers to CSV file
    headers = []
    for field in model._meta.fields:
        headers.append(field.name)
    writer.writerow(headers)
    # Write data to CSV file
    print model.objects.all()
    for obj in model.objects.all().order_by("id"):
        row = []
        for field in model._meta.fields:
            row.append(unicode(getattr(obj, field.name)).encode("utf-8"))
        writer.writerow(row)
    # Return CSV file to browser as download
    return response











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
    
    
    
    
    
    return render_to_response('data/template.species.html', {'genus_list': genus_list }) 




class EquationSearchView(SearchView):

    
    def __name__(self):
        return "EquationSearchView"

    def extra_context(self):
        extra = super(EquationSearchView, self).extra_context()

        #Add stuff to extra as a dict to include in template context

        return extra
