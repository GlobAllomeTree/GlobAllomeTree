import os
import json

from django.contrib import messages

from globallometree.apps.taxonomy.models import (
    Family,
    Genus,
    Species,
    Subspecies,
    SpeciesLocalName,
    SubspeciesLocalName
    )

from globallometree.apps.api import (
    Serializers,
    Parsers
    )

from globallometree.apps.data_sharing.models import DataSharingAgreement, Dataset

restricted_keys = {
    'allometricequation' : ['Equation', 'Substitute_equation',],
    'wooddensity' : ['Density_g_cm3',],
    'rawdata': [],
    'biomassexpansionfactor' : []
}


def restrict_access(record, index_name, user):

    if not index_name in restricted_keys.keys():
        return record

    if not record['Dataset']:
        return record

    license = record['Dataset']['Data_license']

    if license['Available_to_registered_users']:
        record['Dataset']['User_has_access'] = True
        return record
    else:
        try:
            data_sharing_agreement = DataSharingAgreement.objects.get(
                User=user,
                Dataset_id = record['Dataset']['Dataset_ID']
                )
            if data_sharing_agreement.Agreement_status == 'granted':
                record['Dataset']['User_has_access'] = True
                return record
        except DataSharingAgreement.DoesNotExist:
            pass

        try:
            # If the dataset belongs to the user, then return true
            dataset = Dataset.objects.get(
                User=user,
                pk=record['Dataset']['Dataset_ID']
                )
            record['Dataset']['User_has_access'] = True
            return record
        except Dataset.DoesNotExist:
            pass
        
    record['Dataset']['User_has_access'] = False

    for key in restricted_keys[index_name]:
        record[key] = 'access restricted'

    return record


def summarize_data(data):
    """
        Summarizes the dataset as far as which countries there are,
        what species, which new species will be created, future - swhat biomes 
        there are
    """

    new_families = []
    new_genera = []
    new_species = []
    new_subspecies = []

    # Find out which families and species exist, or are new
    for r_i in range(0, len(data)):
        record = data[r_i]
        for sp_i in range(0, len(record['Species_group']['Group'])):
            species_def = record['Species_group']['Group'][sp_i]
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



def get_sub_errors(sub_errors):
    sub_error_list = []
    if isinstance(sub_errors, dict):
        sub_errors = [sub_errors]

    for sub_error_item in sub_errors:
        # if isinstance(sub_error_item, list):
        #     # possibly never a list?
        #      val = {
        #         'field' : None,
        #         'error' : ', '.sub_error_item
        #         } 
        # elif
        if isinstance(sub_error_item, dict):
            for sub_key in sub_error_item.keys():
                val = {
                    'field' : sub_key,
                    'error' : ', '.join(sub_error_item[sub_key])
                    }
                if val not in sub_error_list:
                    sub_error_list.append(val)
        elif isinstance(sub_error_item, unicode):
            val = {
                'field' : None,
                'error' : sub_error_item
                }
        if val not in sub_error_list:
            sub_error_list.append(val)
    return sub_error_list


def validate_records(data, SerializerClass):
    """
        Takes parsed data and checks each record one at a time,
        which makes showing the source of errors a bit easier
    """

    data_errors = []

    for en in enumerate(data):
        record_number = en[0] + 1
        record_data = en[1]
        record_serializer = SerializerClass(data=record_data)
        record_errors = []
        if not record_serializer.is_valid():
            error_dict = dict(record_serializer.errors)

            for key in error_dict.keys():
                # Nested objects
                if key == 'Location_group':
                    record_errors.append({
                        'field' : 'Location_group / Group',
                        'sub_errors' : get_sub_errors(error_dict['Location_group']['Group'])
                    })
                elif key == 'Species_group':
                    record_errors.append({
                        'field' : 'Species_group / Group',
                        'sub_errors' : get_sub_errors(error_dict['Species_group']['Group'])
                    })
                elif key == 'Reference':
                    record_errors.append({
                        'field' : key,
                        'sub_errors' : get_sub_errors(error_dict['Reference'])
                    })
                else:    
                    record_errors.append({
                        'field' : key,
                        'error' : ', '.join(error_dict[key])
                        })

            data_errors.append({
                'record_number': record_number,
                'errors' : record_errors,
                'source' : json.dumps(record_data, indent=4)
                })
    return data_errors


def validate_data_file(data_file, data_type):
    """
        Processes an uploaded file with validation, returns data and errors
        The file may me in xml, csv, or json format
        It could contain allometric equations, wood densities
        raw_data or biomass expansion factors
    """
    
    extension = os.path.splitext(data_file.name.lower())[1]
    ParserClass = Parsers[extension]
    SerializerClass = Serializers[data_type]
    parser = ParserClass()
    data = parser.parse(data_file)
    data_errors = validate_records(data, SerializerClass)
    
    return data, data_errors


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
        for sp_i in range(0, len(record['Species_group']['Group'])):
            species_def = record['Species_group']['Group'][sp_i]
            record['Species_group']['Group'][sp_i] = match_or_clean_species_ids(species_def)
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


def import_dataset_to_db(dataset, data):
    SerializerClass = Serializers[dataset.Data_type] 
    serializer = SerializerClass(data=data, many=True, context={'dataset': dataset})
    if serializer.is_valid(): # Must call id valid
        serializer.save()
        dataset.Imported = True
        dataset.save()
    else:
        raise Exception("The dataset could not be validated and was not imported.") 
