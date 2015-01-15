
from globallometree.apps.taxonomy.models import (
    Family, Genus, Species, SpeciesGroup
)
from globallometree.apps.locations.models import (
    Country, Location, LocationGroup, BiomeFAO, BiomeUdvardy, 
    BiomeWWF, DivisionBailey, BiomeHoldridge
)
from globallometree.apps.source.models import Reference, Institution


country_mappings = {}
countries = []
for country in Country.objects.all():
    countries.append(country)

def getitems(line, sep='\t'):
    items =  line.replace('\n','').split(sep)

    for i in range(0, len(items)):
        # Get outside quotes, and fix escpaed quotes ""
        items[i] = items[i].replace('""', '_QUOTE_')
        items[i] = items[i].replace('"', '')
        items[i] = items[i].replace('_QUOTE_', '"')

    return items

def get_country_object(country_name):
        
    best_match_score = 0
    best_match_object = None

    if country_name in country_mappings.keys():
        return country_mappings[country_name]
    for country in countries:
        common_score = difflib.SequenceMatcher(
            None, country_name, country.common_name
        ).ratio()
        formal_score = difflib.SequenceMatcher(
            None, country_name, country.formal_name
        ).ratio()
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

    country_mappings[country_name] = obj
    return obj


#Imports a data submission into the new denormalized db structure
def run_submission_import(data_submission,  
						  run_verified,  
						  import_good_rows_anyway):

	expected_headers = [
	    'ID', 'IDequation', 'Population', 'Ecosystem', 'Continent',
	    'Country', 'ID_Location', 'Group_Location', 'Location', 'Latitude',
	    'Longitude', 'Biome_FAO', 'Biome_UDVARDY', 'Biome_WWF',
	    'Division_BAILEY', 'Biome_HOLDRIDGE', 'X', 'Unit_X', 'Z', 'Unit_Z',
	    'W', 'Unit_W', 'U', 'Unit_U', 'V', 'Unit_V', 'Min_X', 'Max_X',
	    'Min_Z', 'Max_Z', 'Output', 'Output_TR', 'Unit_Y', 'Age',
	    'Veg_Component', 'B', 'Bd', 'Bg', 'Bt', 'L', 'Rb', 'Rf', 'Rm', 'S',
	    'T', 'F', 'ID_Species', 'Family', 'Genus', 'Species',
	    'Group_Species', 'ID_Group', 'Equation', 'Substitute_equation',
	    'Top_dob', 'Stump_height', 'ID_REF', 'Label', 'Author', 'Year',
	    'Reference', 'R2', 'R2_Adjusted', 'RMSE', 'SEE',
	    'Corrected_for_bias', 'Bias_correction', 'Ratio_equation',
	    'Segmented_equation', 'Sample_size', 'Contributor', 'Name_operator'
	]
	eq_fields = [field.name for field in AllometricEquation._meta.fields]
	foreign_key_fields = [
	    'species_group', 'location_group', 'population',
	    'ecosystem', 'Contributor', 'reference'
	]                   
	decimal_fields = [
	    'R2', 'R2_Adjusted', 'RMSE', 'SEE',
	    'Min_X', 'Max_X', 'Min_Y', 'Max_Y'
	]
	bool_fields = [
	   'Segmented_equation', 'Ratio_equation', 'Corrected_for_bias',
	   'B', 'Bd', 'Bg', 'Bt', 'L', 'Rb', 'Rf', 'Rm', 'S', 'T', 'F'
	]
	dont_import_fields = [
	    'data_submission'
	]
	none_values = ['na', 'None', 'none', '-']
	true_values = ['true', 1, '1', 'True', 'TRUE', 'yes', 'Yes', 'YES']
	false_values = ['false', 0, '0', 'False', 'FALSE', 'no', 'No', 'NO']

	species_inserted = 0
	species_groups_inserted = 0
	locations_inserted = 0
	location_groups_inserted = 0
	missed_countries = []
	missed_rows = []
	headers = None
	errors = []
	

	line_number = 0
	total_rows_imported = 0
	output = {}

	try:
	    submitted_file = codecs.open(
	        settings.MEDIA_ROOT + '/' + str(data_submission.submitted_file),
	        'r', encoding=settings.DATA_EXPORT_ENCODING, errors='strict'
	    )

	    for line in submitted_file:
	        line_number += 1

	        if not headers:
	            headers = getitems(line)
	            
	            # Headers that match in import file and model
	            ok_headers = []

	            # Headers that exist in the imort file but not the model
	            unknown_headers = []

	            # Headers that exist in the model file but not the import file
	            missing_headers = []

	            for key in headers:
	                if key in expected_headers:
	                    ok_headers.append(key)
	                else:
	                    unknown_headers.append(key)

	            for key in expected_headers:
	                if key not in headers and key not in dont_import_fields:
	                    missing_headers.append(key)
	        
	            output['ok_headers'] = ok_headers
	            output['missing_headers'] = missing_headers
	            output['unknown_headers'] = unknown_headers
	            continue
	        else:
	            items = getitems(line)

	        row = dict(zip(headers, items))

	        # species_group
	        if row['Family'] in none_values:
	            family = None
	        else:
	            family = Family.objects.get_or_create(name=row['Family'])[0]
	        
	        if row['Genus'] in none_values:
	            genus = None
	        else:
	            genus = Genus.objects.get_or_create(name=row['Genus'], 
	                                                family=family)[0]

	        if row['ID_Species'] in none_values:
	            species = None
	        else:
	            species, species_created = Species.objects.get_or_create(
	                name=row['Species'], 
	                genus=genus,
	                original_ID_Species=row['ID_Species']
	            )
	            if species_created:
	                species_inserted = species_inserted + 1

	        if species:
	            if row['Group_Species'] and row['ID_Group'] and row['ID_Group'] not in none_values:
	                species_group, species_group_created = SpeciesGroup.objects.get_or_create(
	                    original_ID_Group=row['ID_Group'],
	                    name="Auto Created Group for original ID_Group %s" % row['ID_Group']
	                )
	            else:
	                species_group, species_group_created = SpeciesGroup.objects.get_or_create(
	                    name="Auto Created Group for equation ID %s" % row['IDequation']
	                )
	            if species_group_created:
	                species_groups_inserted = species_groups_inserted + 1

	            species_group.species.add(species)

	        # location_group
	        country_name = row['Country']

	        if country_name in none_values:
	            country = None
	        else:
	            country = get_country_object(country_name)
	            if country is None:
	                if country_name not in missed_countries:
	                    missed_countries.append(country_name)
	                continue

	        if row['Biome_FAO'] in none_values:
	            biome_fao = None
	        else:
	            biome_fao = BiomeFAO.objects.get_or_create(
	                name=row['Biome_FAO']
	            )[0]

	        if row['Biome_UDVARDY'] in none_values:
	            biome_udvardy = None
	        else:
	            biome_udvardy = BiomeUdvardy.objects.get_or_create(
	                name=row['Biome_UDVARDY']
	            )[0]

	        if row['Biome_WWF'] in none_values:
	            biome_wwf = None
	        else:
	            biome_wwf = BiomeWWF.objects.get_or_create(
	                name=row['Biome_WWF']
	            )[0]

	        if row['Division_BAILEY'] in none_values:
	            division_bailey = None
	        else:
	            division_bailey = DivisionBailey.objects.get_or_create(
	                name=row['Division_BAILEY']
	            )[0]

	        if row['Biome_HOLDRIDGE'] in none_values:
	            biome_holdridge = None
	        else:
	            biome_holdridge = BiomeHoldridge.objects.get_or_create(
	                name=row['Biome_HOLDRIDGE']
	            )[0]

	        # note: The Continent column is ignored

	        location, location_created = Location.objects.get_or_create(
	            original_ID_Location=row['ID_Location'],
	            name=row['Location'],
	            Latitude=row['Latitude'],
	            Longitude=row['Longitude'],
	            biome_fao=biome_fao,
	            biome_udvardy=biome_udvardy,
	            biome_wwf=biome_wwf, 
	            division_bailey=division_bailey,
	            biome_holdridge=biome_holdridge,
	            country=country
	        )
	        if location_created:
	            locations_inserted = locations_inserted + 1

	        if row['Group_Location'] and row['Group_Location'] not in none_values:
	            location_group, location_group_created = LocationGroup.objects.get_or_create(
	                original_Group_Location=row['Group_Location'],
	                name="Auto Created Group for original Group_Location %s" % row['Group_Location']
	            )
	            if location_group_created:
	                location_groups_inserted = location_groups_inserted + 1
	        else:   
	            location_group, location_group_created = LocationGroup.objects.get_or_create(
	                name="Auto Created Group for Equation %s" % row['IDequation']
	            )
	            if location_group_created:
	                location_groups_inserted = location_groups_inserted + 1

	        location_group.locations.add(location)

	        # Contributor and reference
	        if row['Contributor'] in none_values:
	            Contributor = None
	        else:
	            Contributor = Institution.objects.get_or_create(
	                name=row['Contributor']
	            )[0]

	        if row['Reference'] in none_values:
	            reference = None
	        else:
	            reference = Reference.objects.get_or_create(
	                label=row['Label'],
	                author=row['Author'],
	                year=row['Year'],
	                reference=row['Reference'],
	            )[0]

	        # population and ecosystem
	        if row['Population'] in none_values:
	            population = None
	        else:
	            population = Population.objects.get_or_create(
	                name=row['Population']
	            )[0]

	        if row['Ecosystem'] in none_values:
	            ecosystem = None
	        else:
	            ecosystem = Ecosystem.objects.get_or_create(
	                name=row['Ecosystem']
	            )[0]

	        # actually run the import
	        if run_verified:
	            try:
	                allometric_equation = AllometricEquation(
	                    population=population,
	                    ecosystem=ecosystem,
	                    Contributor=Contributor,
	                    reference=reference,
	                    species_group=species_group,
	                    location_group=location_group,
	                    data_submission=self
	                )
	                for key in headers:
	                    if key in foreign_key_fields:
	                        continue
	                    if key in eq_fields:
	                        if row[key] not in none_values:
	                            if key in decimal_fields:
	                                try:
	                                    val = Decimal(row[key].replace(',', '.').upper())    
	                                except Exception, e:
	                                    raise Exception('Could not convert value "%s" to decimal for field %s, exception was %s' % (row[key], key, e))
	                            elif key in bool_fields:
	                                val = None
	                                if row[key] in true_values:
	                                    val = True
	                                if row[key] in false_values:
	                                    val = False
	                                if val is None:
	                                    raise Exception('Could not convert value "%s" to boolean for field %s ' % (row[key], key))
	                            else:
	                                val = row[key]
	                            setattr(allometric_equation, key, val)
	            
	                allometric_equation.clean_fields() # Triggers Validation error for fields that are not correct
	                allometric_equation.save()
	                # Give elasticsearch 1/10th of a second to index the record on save
	                # tring not to overload the server
	                # sleep(0.1)
	                total_rows_imported += 1
	            except ValidationError as e:
	                missed_rows.append({'line_number' : line_number,
	                                    'exception'   : str(e)})

	    if run_verified and len(missed_rows) == 0:
	        data_submission.imported = True
	        self.save()
	    elif run_verified and len(missed_rows) > 0:
	        if import_good_rows_anyway:
	            data_submission.imported = True
	            data_submission.save()
	        else:
	            output['import_reset'] = True
	            # We missed some rows... so reset everything
	            for eq in AllometricEquation.objects.filter(
	                data_submission = self
	            ):
	                eq.delete()                

	except UnicodeDecodeError:
	    errors.append(
	        'The submitted file is not in the encoding {0}.'
	        'Please convert and re-upload the file then try again.'
	        .format(settings.DATA_EXPORT_ENCODING)
	    )

	if len(missed_countries):
	    errors.append(
	        'The following country names in the csv file could not be'
	        'matched to the country database: {0}'
	        .format(', '.join(missed_countries))
	    )

	output['errors'] = errors
	output['country_mappings'] = country_mappings
	output['rows_to_import'] = line_number -1
	output['show_import_summary'] = run_verified
	output['species_inserted'] = species_inserted
	output['species_groups_inserted'] = species_groups_inserted
	output['locations_inserted'] = locations_inserted
	output['location_groups_inserted'] = location_groups_inserted
	output['missed_rows'] = missed_rows
    output['total_rows_imported'] = total_rows_imported

    return output