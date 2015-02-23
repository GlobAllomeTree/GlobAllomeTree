from globallometree.apps.taxonomy.models import (
	Family,
	Genus,
	Species,
	Subspecies,
	SpeciesLocalName,
	SubspeciesLocalName
	)

from apps.api.serializers import (
    SimpleAllometricEquationSerializer,
    SimpleWoodDensitySerializer,
    SimpleRawDataSerializer
)

serializers = {
                'raw_data': SimpleRawDataSerializer,
                'biomass_expansion': None,
                'wood_density': SimpleWoodDensitySerializer,
                'allometric_equations': SimpleAllometricEquationSerializer
            }

def summarize_data(data):
	"""
		Summarizes the dataset as far as which countries there are,
		what species, which new species will be created, what biomes 
		there are
	"""

	new_families = []
	new_genera = []
	new_species = []
	new_subspecies = []

	# Find out which families and species exist, or are new
	for r_i in range(0, len(data)):
		record = data[r_i]
		for sp_i in range(0, len(record['Species_group']['Species'])):
			species_def = record['Species_group']['Species'][sp_i]
			if species_def['Family'] and not species_def['Family_ID']:
				new_record = {
					"Family": species_def['Family']
				}
				if new_record not in new_families:
					new_families.append(new_record)

			if species_def['Genus'] and not species_def['Genus_ID']:
				new_record = {
					"Family": species_def['Family'],
					"Genus": species_def['Genus']
				}
				if new_record not in new_genera:
					new_genera.append(new_record)

			if species_def['Species'] and not species_def['Species_ID']: 
				new_record= {
					"Family": species_def['Family'],
					"Genus": species_def['Genus'],
					"Species": species_def['Species'],
				}	
				if new_record not in new_species:
					new_species.append(new_record)

			if species_def['Subspecies'] and not species_def['Subspecies_ID']: 
				new_record = {
					"Family": species_def['Family'],
					"Genus": species_def['Genus'],
					"Species": species_def['Species'],
					"Subspecies": species_def['Subspecies']
				}	
				if new_record not in new_subspecies:
					new_subspecies.append(new_record)

	return {
		'record_count' : len(data),
		'new_species': new_species,
		'new_genera': new_genera,
		'new_families': new_families,
		'new_subspecies': new_subspecies
	}


def match_data_to_database(data):
	"""
		Takes uploaded data from the user and makes sure 
		that the ids of species, biomes, etc correspond
		with the ids already in the database. Biomes and countries
		must correspond while species and genera that aren't yet 
		found will be left without ids to indicate that they should 
		be created by the serializer save method
	"""

	for r_i in range(0, len(data)):
		record = data[r_i]
		for sp_i in range(0, len(record['Species_group']['Species'])):
			species_def = record['Species_group']['Species'][sp_i]
			record['Species_group']['Species'][sp_i] = match_or_clean_species_ids(species_def)

		data[r_i] = record
		
	return data

def match_or_clean_species_ids(species_def):

	db_family = None
	db_genus = None
	db_species = None
	db_subspecies = None

	species_def['Family_ID'] = None
	species_def['Species_ID'] = None
	species_def['Genus_ID'] = None
	species_def['Subspecies_ID'] = None

	# Family and Genus are required by the parser
	try:
		db_family = Family.objects.get(Name=species_def['Family'])
		species_def['Family_ID'] = db_family.pk
	except Family.DoesNotExist:
		pass
		
	# If we have the family in our db, we try to find the genus id
	if db_family:
		try:
			db_genus = Genus.objects.get(
				Family=db_family,
				Name=species_def['Genus']
				)
			species_def['Genus_ID'] = db_genus.pk
		except Genus.DoesNotExist:
			pass
			
	# If we have the genus in our db, we try to find the species id
	if db_genus and 'Species' in species_def.keys():
		try:
			db_species = Species.objects.get(
				Genus=db_genus,
				Name=species_def['Species'])
			species_def['Species_ID'] = db_species.pk
		except Species.DoesNotExist:
			pass

	# If we have the species in our db, we try to find the subspecies id
	if db_species and 'Subspecies' in species_def.keys():
		try:
			db_subspecies = Subspecies.objects.get(Name=species_def['Subspecies'])
			species_def['Subpsecies_ID'] = db_species.pk
		except Subspecies.DoesNotExist:
			pass

	return species_def
