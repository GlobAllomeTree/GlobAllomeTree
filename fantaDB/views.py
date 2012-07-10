from django.shortcuts import render_to_response
from fantaDB.models import fantaDB
from django.http import HttpResponse
import csv
from django.template.defaultfilters import slugify

def continents_map(request):
    return render_to_response('continents_map.html',{'': '', })

def fantaDB_id(request,DB_id):
	DB_object = fantaDB.objects.get(id=DB_id)
	return render_to_response('fantaDB_id.html', {'DB_object': DB_object, }) 

def geo_map(request):
	country_list = fantaDB.objects.values_list('country__common_name',flat=True).distinct
	return render_to_response('geo_map.html', {'country_list': country_list, })

def geo_map_id(request, geo_id):
	country_DB = fantaDB.objects.filter(country__iso_3166_1_2_letter_code = geo_id )
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
    fanta_objects = fantaDB.objects.all()
    writer.writerow(['id_article', 'population', 'genus', 'species', 'ecosystem', 'temperature', 'country'])  
    for data in fanta_objects:
        writer.writerow([data.id_article, data.population, data.genus, data.species, unicode(data.ecosystem).encode("utf-8"), data.temperature, data.country_id])
    return response

def export_db_all(request,db_id):
    model = fantaDB
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







