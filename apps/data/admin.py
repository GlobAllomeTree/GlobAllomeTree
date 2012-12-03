import codecs
import difflib
from time import sleep
from decimal import Decimal
from decimal import getcontext
getcontext().prec = 10

from django.contrib import admin
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from . import models


class TreeEquationAdmin(admin.ModelAdmin):
    list_display = ('ID', 'data_submission', 'Country', 'Species', 'Genus',  'Equation')
    ordering = ("ID",)
    search_fields  = ('ID',)
    list_filter = ('data_submission', 'Country')




class DataSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'submitted_file', 'submitted_notes', 'imported')
    list_filter = ['user', 'imported']

    actions = ['run_import']

    none_fields = ['na', 'None', 'none', '-']


    def getitems(self, line, sep='\t'):
        items =  line.replace('\n','').split(sep)

        for i in range(0, len(items)):
            #Get outside quotes, and fix escpaed quotes ""
            items[i] = items[i].replace('""', 'QUOTE')
            items[i] = items[i].replace('"', '')
            items[i] = items[i].replace('QUOTE', '"')

        return items

    def get_country_object(self, country_name):
            
        best_match_score = 0
        best_match_object = None

        if country_name in self.country_mappings.keys():
            return self.country_mappings[country_name]
        for country in self.countries:
            common_score = difflib.SequenceMatcher(None, country_name, country.common_name).ratio()
            formal_score = difflib.SequenceMatcher(None, country_name, country.formal_name).ratio()
            if common_score > best_match_score:
                best_match_score = common_score
                best_match_object = country

            if formal_score > best_match_score:
                best_match_score = formal_score
                best_match_object = country

        if best_match_score > .9:
            obj = best_match_object
        else:
            obj = None

        self.country_mappings[country_name] = obj
        return obj

    def run_import(self, request, queryset):
        


        #Make sure that there are some selected rows 
        n = queryset.count()
        if not n:
            self.message_user(request, "Please select a file to import")
            return None
  

        #Make sure multiple objects were not selected
        if n > 1:
            self.message_user(request, "Please select onle ONE file to import at a time")
            return None

        #Now that we have one row, we get the data submission from the query set
        
        data_submission = queryset[0]

        context = { 'data_submission' : data_submission,
                    'queryset' : queryset }

        tree_eq_fields = [field.name for field in models.TreeEquation._meta.fields]         
        
        decimal_fields = ['R2', 
                          'R2_Adjusted',
                          'RMSE',
                          'SEE',
                          'Min_X',
                          'Max_X',
                          'Min_Y',
                          'Max_Y']
        
        bool_fields = [
           'Segmented_equation',
           'Ratio_equation',
           'Corrected_for_bias',
           'B',                             
           'Bd',                        
           'Bg',                   
           'Bt',                     
           'L',                  
           'Rb',              
           'Rf',                 
           'Rm',                 
           'S',        
           'T',         
           'F'
        ]


        dont_import_fields = [
            'data_submission'
        ]

        missed_countries = []
        missed_rows = []
        headers = None

        errors = []

        self.countries = []
        for country in models.Country.objects.all():
            self.countries.append(country)
        self.country_mappings = {}
        line_number = 0
        total_rows_imported = 0
        run_verified = request.POST.get('run', False)

        try:
            submitted_file = codecs.open(settings.MEDIA_ROOT + '/' + str(data_submission.submitted_file), 'r', encoding='utf-8-sig', errors='strict')
        
            for line in submitted_file:
                line_number += 1

                if not headers:
                    headers = self.getitems(line)
                    
                    #Headers that match in import file and model
                    ok_headers = []

                    #Headers that exist in the imort file but not the model
                    unknown_headers = []

                    #Headers that exist in the model file but not the import file
                    missing_headers = []

                    for key in headers:
                        if key in tree_eq_fields:
                            ok_headers.append(key)
                        else:
                            unknown_headers.append(key)

                    for key in tree_eq_fields:
                        if key not in headers and key not in dont_import_fields:
                            missing_headers.append(key)
                
                    context['ok_headers'] = ok_headers
                    context['missing_headers'] = missing_headers
                    context['unknown_headers'] = unknown_headers
                    continue
                else:
                    
                    items = self.getitems(line)

                row = dict(zip(headers, items))

                country_name = row['Country']

                if country_name in self.none_fields:
                    country = None
                else:
                    country = self.get_country_object(country_name)
                    if country is None:
                        if country_name not in missed_countries:
                            missed_countries.append(country_name)
                        continue

                #actually run the import
                if run_verified:
                    

                    try:
                        tree_equation = models.TreeEquation(Country=country, 
                                                            data_submission=data_submission)
                        for key in headers:
                            if key == 'Country':
                                continue
                            if key in tree_eq_fields:
                                if row[key] not in self.none_fields:

                                    if key in decimal_fields:

                                        try:
                                            val = Decimal(row[key].replace(',', '.').upper())    
                                        except Exception, e:
                                            raise Exception('Could not convert value "%s" to decimal for field %s, exception was %s' % (row[key], key, e))
                                    elif key in bool_fields:
                                        val = None
                                        if row[key] in ['true', 1, '1', 'True', 'TRUE', 'yes', 'Yes', 'YES']:
                                            val = True
                                        if row[key] in ['false', 0, '0', 'False', 'FALSE', 'no', 'No', 'NO']:
                                            val = False
                                        if val is None:
                                            raise Exception('Could not convert value "%s" to boolean for field %s ' % (row[key], key))
                                    else:
                                        val = row[key]

                                    setattr(tree_equation, key, val)
                    
                        tree_equation.save()
                        #Give elasticsearch 1/10th of a second to index the record on save
                        #tring not to overload the server
                        sleep(0.1)
                        total_rows_imported += 1
                    except Exception, e:
                        missed_rows.append({'line_number' : line_number,
                                            'exception'   : str(e)})

            if run_verified and len(missed_rows) == 0:
                data_submission.imported = True
                data_submission.save()
            elif run_verified and len(missed_rows) > 0:
                if request.POST.get('import_good_rows_anyway', False):
                    data_submission.imported = True
                    data_submission.save()
                else:
                    context['import_reset'] = True
                    #We missed some rows... so reset everything
                    for eq in models.TreeEquation.objects.filter(data_submission = data_submission):
                        eq.delete()                

        except UnicodeDecodeError:
            errors.append("The submitted file is not in the encoding utf-8 (utf-8-sig). Please convert and re-upload the file in utf-8 encoding and try again")

        if len(missed_countries):
            errors.append('The following country names in the csv file could not be matched to the country database: %s' %\
                            ', '.join(missed_countries)
                          )

        context['errors'] = errors
        context['country_mappings'] = self.country_mappings
        context['rows_to_import'] = line_number -1
        context['show_import_summary'] = run_verified
        context['missed_rows'] = missed_rows
        context['total_rows_imported'] = total_rows_imported
        context['action_checkbox_name'] =  admin.helpers.ACTION_CHECKBOX_NAME

        
        return render_to_response('data/template.admin.run_import_confirm.html', context,
                                        context_instance=RequestContext(request))

admin.site.register(models.Country)
admin.site.register(models.DataSubmission, DataSubmissionAdmin)
admin.site.register(models.TreeEquation, TreeEquationAdmin)