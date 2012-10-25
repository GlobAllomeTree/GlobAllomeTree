# -*- coding: utf-8 -*-
import codecs
import datetime
import collections
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.conf import settings

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."

        headers = False

        TreeEquation = orm['data.TreeEquation']
        Country      = orm['data.Country']
        file = codecs.open(settings.INITIAL_DATA_DIR  + 'DB-africa.csv', 'r', 'utf-8-sig')
   
        tree_eq_fields = [field.name for field in TreeEquation._meta.fields]         
        
        decimal_fields = ['r2', 
                          'r2_adjusted',
                          'rmse',
                          'rms',
                          'see',
                          'max_X',
                          'max_H',
                          'max_Y',
                          'min_X',
                          'min_H',
                          'min_Y', 
                           'temperature',
                          'potential_evapotranspiration',
                          'precipitation',
                          'sunshine_fraction',
                          'wind',
                          'water_vapor_pressure',
                          'temp_MIN',
                          'temp_MAX']
        
        bool_fields = [
           'group_location',
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

        mapped_countries = {}

	known_missed_country_names = {
		'Democratic Republic of Congo' : 39,	
		'Cameroun' : 30,
		'cameroon' : 30,
		'Ivory Coast' :  42,
		'Guinea-bissau' : 70,
		'Congo' : 39,
		'ghana' : 65,
                'RCA'   : 33
	}

        def get_country_object(country_name):
            if country_name == 'na': return None
            if country_name in mapped_countries.keys():
                return mapped_countries[country_name]
            
            if country_name in known_missed_country_names.keys():
                country_id = known_missed_country_names[country_name]            
                country = Country.objects.get(pk=country_id)
            else:
                    try:
                        country = Country.objects.get(common_name = country_name)
                    except Country.DoesNotExist:
                                try:
                                        country = Country.objects.get(formal_name = country_name)
                                except Country.DoesNotExist:
                                        country_id = raw_input('\nPlease enter the country id for the country "%s":' % country_name)
                                        country = Country.objects.get(pk=int(country_id))

            mapped_countries[country_name] = country
            return country   

        def get_header_field(header):

            name_map = {
                    'bias_correction' : 'bias_correction_cf',
                'equation'        : 'equation_y'            
            }

            if header.lower() in name_map.keys():
                header = name_map[header.lower()]

            for field in tree_eq_fields:
                
                if field.lower() == header.lower():
                    return field
            return header

        def getitems(line, sep='\t'):
            items =  line.replace('\n','').split(sep)

            for i in range(0, len(items)):
                #Get outside quotes, and fix escpaed quotes ""
                items[i] = items[i].replace('""', 'QUOTE')
                items[i] = items[i].replace('"', '')
                items[i] = items[i].replace('QUOTE', '"')
            return items
        i = 0
        bad_rows = {}
        for line in file:
                    i += 1
                    print "\rImporting row %s" % i,
                    #if i > 50: break

                    if not headers:
                        headers = []
                        for header in getitems(line):
                            headers.append(get_header_field(header))
                        
                        ok_keys = []
                        missed_keys = []

                        for key in headers:
                            if key in tree_eq_fields:
                                ok_keys.append(key)
                            else:
                                missed_keys.append(key)
                    
                        print "CHECKING THE CSV HEADERS"
                        print "OK HEADERS"
                        print ok_keys
                        print "SKIPPED KEYS (Continent is expected to be skipped)"
                        print missed_keys
                        ans = raw_input("Press enter to continue")
                        continue

                    items = getitems(line)
                    if len(headers) != len(items):
                        bad_rows[i] = 'columns length not eq to headers length'
			continue

                    row = dict(zip(headers, items))
                    tree_equation = TreeEquation()
                               
                    row['country'] = get_country_object(row['country'])
                    if row['country'] is None:
                        bad_rows[i] = 'No Country Specified'
                        continue

                    row['id_article'] = row['id']
                 
                    for key in headers:
                        if key in tree_eq_fields:
                             if row[key] not in ['na', '']:
				 if key in decimal_fields:
                                	row[key] = row[key].replace(',', '.')
					dot_index = row[key].find('.')
                                        if dot_index != -1:
                                            row[key] = row[key][0:dot_index+8]
                                 elif key in bool_fields:
                                        row[key] = bool(int(row[key]))
                                 setattr(tree_equation, key, row[key])
                    try:
                        tree_equation.save()
                    except Exception, e:
                        bad_rows[i] = str(e)

        print "\nREPORT"
        bad_keys = bad_rows.keys()
        bad_keys.sort()
        for key in bad_keys:
                print "LINE %s: %s " % (key, bad_rows[key])

        print 'BAD ROWS COUNT: %s' % len(bad_rows.keys()) 

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'data.country': {
            'Meta': {'object_name': 'Country'},
            'capital': ('django.db.models.fields.CharField', [], {'max_length': '234', 'blank': 'True'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '159', 'blank': 'True'}),
            'formal_name': ('django.db.models.fields.CharField', [], {'max_length': '159', 'blank': 'True'}),
            'iana_country_code_tld': ('django.db.models.fields.CharField', [], {'max_length': '33', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_3166_1_2_letter_code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'iso_3166_1_3_letter_code': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'iso_3166_1_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'iso_4217_currency_code': ('django.db.models.fields.CharField', [], {'max_length': '33', 'blank': 'True'}),
            'iso_4217_currency_name': ('django.db.models.fields.CharField', [], {'max_length': '42', 'blank': 'True'}),
            'sovereignty': ('django.db.models.fields.CharField', [], {'max_length': '72', 'blank': 'True'}),
            'sub_type': ('django.db.models.fields.CharField', [], {'max_length': '102', 'blank': 'True'}),
            'telephone_code': ('django.db.models.fields.CharField', [], {'max_length': '48', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '69', 'blank': 'True'})
        },
        'data.treeequation': {
            'B': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Bd': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Bg': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Bt': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'F': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'L': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'TreeEquation'},
            'Rb': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Rf': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Rm': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'S': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'T': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'U': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'V': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'W': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'X': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'Z': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'age': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'bias_correction_cf': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'biome_FAO': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'biome_HOLDRIDGE': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'biome_UDVARDY': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'biome_WWF': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'contributor': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'corrected_for_bias': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Country']", 'null': 'True', 'blank': 'True'}),
            'division_BAILEY': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ecosystem': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'equation_y': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'family': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'group_location': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'group_species': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_article': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id_group': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id_location': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id_ref': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id_species': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '6', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '6', 'blank': 'True'}),
            'max_H': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'max_X': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'max_Z': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'min_H': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'min_X': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'min_Z': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'n': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name_operator': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'output': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'output_TR': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'population': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'potential_evapotranspiration': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'precipitation': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'r2': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '5', 'blank': 'True'}),
            'r2_adjusted': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '5', 'blank': 'True'}),
            'ratio_equation': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rms': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '9', 'blank': 'True'}),
            'rmse': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '9', 'blank': 'True'}),
            'sample_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'see': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '9', 'blank': 'True'}),
            'segmented_equation': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'stump_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sunshine_fraction': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'temp_MAX': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'temp_MIN': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'temperature': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'top_dob': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'unit_U': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'unit_V': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'unit_W': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'unit_X': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'unit_Y': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'unit_Z': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'veg_component': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'water_vapor_pressure': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'wind': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['data']
    symmetrical = True
