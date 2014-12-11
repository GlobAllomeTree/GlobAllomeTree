import os
import sys
import csv
import codecs

from django.db import transaction
from django.conf import settings
from django.core.management.base import BaseCommand
from globallometree.apps.data.models import TreeEquation, Country as OldCountry
from globallometree.apps.taxonomy.models import Species, Family, Genus, SpeciesGroup
from globallometree.apps.allometric_equations.models import AllometricEquation, Population, TreeType
from globallometree.apps.locations.models import (BiomeFAO, BiomeUdvardy, BiomeWWF, DivisionBailey, BiomeHoldridge,
                                                  Location, Country, Continent, LocationGroup, ForestType)
from globallometree.apps.common.models import Reference, Institution
from globallometree.apps.data_sharing.models import Dataset

missed_udvardy = {}
missed_wwf = {}
missed_holdridge = {}
missed_bailey = {}
missed_fao = {}


class Command(BaseCommand):
    args = '<limit (optional)>'
    help = 'Imports from the old data.TreeEquation model to the new normalized structure'


    def load_csv(self, file_name):
        #csv file with country lats/lons
        csv_file_path = os.path.join(settings.BASE_PATH, 'globallometree', 'apps', 'allometric_equations', 'resources', file_name)
        headers = []
        data = []

        def clean(row):
            fields = row.replace('\r', '').replace('\n', '').replace(u'\ufeff','').split(';')
            fields = [v.strip() for v in fields]
            return fields

        with codecs.open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            for row in csv_file:
                if not len(headers):
                    headers = clean(row)
                    continue
                data.append(dict(zip(headers, clean(row))))

        return data

    def get_mapping(self, file_name):
        file_dict = self.load_csv(file_name)
        mapping = {}
        for row in file_dict:
            mapping[row['old']] = row['new']
        return mapping

    def handle(self,*args, **options):

        if len(args) == 1:
            limit = int(args[0])
        elif len(args) > 1:
            exit('Command only takes one argument <limit>')
        else:
            limit = 0

        n = 0
        equations_insterted = 0
        species_inserted = 0
        original_species_groups_inserted = 0
        new_species_groups_inserted = 0
        locations_inserted = 0
        original_location_groups_inserted = 0
        new_location_groups_inserted = 0

        if limit:
            total = limit
        else:
            total = TreeEquation.objects.all().count()


        for orig_equation in TreeEquation.objects.all().iterator():
            if limit and n > limit: break;
            n = n + 1; 
            
######################################## TAXONOMY ################################################

            print n, 'out of', total, '\r',
            sys.stdout.flush()
            
            if orig_equation.Family is None:
                family = None
            else:
                family = Family.objects.get_or_create(Name=orig_equation.Family)[0]
            
            if orig_equation.Genus is None:
                genus = None
            else:
                genus = Genus.objects.get_or_create(Name=orig_equation.Genus, 
                                                    Family=family)[0]

            if orig_equation.ID_Species is None:
                species = None
            else:
                species, species_created = Species.objects.get_or_create(
                    Name=orig_equation.Species, 
                    Genus=genus,
                )
                if species_created:
                    species_inserted = species_inserted + 1

            if species:
                if orig_equation.Group_Species and orig_equation.ID_Group:
                    species_group, species_group_created = SpeciesGroup.objects.get_or_create(
                        Name="Auto Created Group for original ID_Group %s" % orig_equation.ID_Group
                    )
                    if species_group_created:
                        original_species_groups_inserted = original_species_groups_inserted + 1
                else:
                    species_group, species_group_created = SpeciesGroup.objects.get_or_create(
                        Name="Auto Created Group for equation ID %s" % orig_equation.IDequation
                    )
                    if species_group_created:
                        new_species_groups_inserted = new_species_groups_inserted + 1
                
                #It appears some species may contain 'None' species, which don't get explicitly added
                species_group.Species.add(species)

######################################## LOCATIONS ################################################

            #Mappings to correct values from the old database schema to the new on
            biome_fao_mapping = self.get_mapping('conversions_fao.csv')
            biome_wwf_mapping = self.get_mapping('conversions_wwf.csv')
            division_bailey_mapping = self.get_mapping('conversions_bailey.csv')
            biome_udvardy_mapping = self.get_mapping('conversions_udvardy.csv')

            if orig_equation.Country is None or not orig_equation.Country.iso_3166_1_2_letter_code:
                country = None
            else:
                country = Country.objects.get(Iso3166a2=orig_equation.Country.iso_3166_1_2_letter_code)
        
            none_values = ['NA', None]

            if orig_equation.Biome_FAO:
                biome_fao_val = orig_equation.Biome_FAO.strip()
                if biome_fao_val in biome_fao_mapping.keys():
                    biome_fao_val = biome_fao_mapping[biome_fao_val]

                if biome_fao_val in none_values:
                    biome_fao = None
                else:
                    try:
                        biome_fao = BiomeFAO.objects.get(Name__iexact=biome_fao_val)
                    except:
                        missed_fao[biome_fao_val] = True
                        biome_fao = None

            if orig_equation.Biome_UDVARDY:
                biome_udvardy_val = orig_equation.Biome_UDVARDY.strip()

                if biome_udvardy_val in biome_udvardy_mapping.keys():
                    biome_udvardy_val = biome_udvardy_mapping[biome_udvardy_val]

                if biome_udvardy_val in none_values:
                   biome_udvardy = None
                else:
                    try:
                        biome_udvardy = BiomeUdvardy.objects.get(Name__iexact=biome_udvardy_val)
                    except:
                        missed_udvardy[biome_udvardy_val] = True
                        biome_udvardy = None

            if orig_equation.Biome_WWF:
                biome_wwf_val = orig_equation.Biome_WWF.strip()
                if biome_wwf_val in biome_wwf_mapping.keys():
                    biome_wwf_val = biome_wwf_mapping[biome_wwf_val]

                if biome_wwf_val in none_values:
                   biome_wwf = None
                else:
                    try:
                        biome_wwf = BiomeWWF.objects.get(Name__iexact=biome_wwf_val)
                    except:
                        missed_wwf[biome_wwf_val] = True
                        biome_wwf = None
                   
            if orig_equation.Biome_HOLDRIDGE:
                biome_holdridge_val = orig_equation.Biome_HOLDRIDGE.strip()
                if biome_holdridge_val in none_values:
                   biome_holdridge = None
                else:
                    try:
                        biome_holdridge = BiomeHoldridge.objects.get(Name__iexact=biome_holdridge_val)
                    except:
                        missed_holdridge[biome_holdridge_val] = True
                        biome_holdridge = None

            if orig_equation.Division_BAILEY:
                division_bailey_val = orig_equation.Division_BAILEY.strip()
                if division_bailey_val in division_bailey_mapping.keys():
                    division_bailey_val = division_bailey_mapping[division_bailey_val]

                if division_bailey_val in none_values:
                   division_bailey = None
                else:
                    try:
                        division_bailey = DivisionBailey.objects.get(Name__iexact=division_bailey_val)
                    except:
                        missed_bailey[division_bailey_val] = True
                        division_bailey = None

            if orig_equation.Latitude:
                latitude = orig_equation.Latitude
            else:
                latitude = None

            if orig_equation.Longitude:
                longitude = orig_equation.Longitude
            else:
                longitude = None

            if orig_equation.Location:
                name_val = orig_equation.Location.strip()
            else:
                name_val = None

            location, location_created = Location.objects.get_or_create(
               Name = name_val,
               Biome_FAO = biome_fao,
               Biome_WWF = biome_wwf,
               Biome_HOLDRIDGE = biome_holdridge,
               Biome_UDVARDY = biome_udvardy,
               Division_BAILEY = division_bailey,
               Country = country,
               Latitude = latitude,
               Longitude = longitude
            )

            if location_created:
                locations_inserted = locations_inserted + 1 

            if orig_equation.Group_Location:
                location_group, location_group_created = LocationGroup.objects.get_or_create(
                    Name="Auto existing for Equation Group_Location %s" % orig_equation.Group_Location
                )
                if location_group_created:
                    original_location_groups_inserted = original_location_groups_inserted + 1
            else:   
                location_group, location_group_created = LocationGroup.objects.get_or_create(
                    Name="Auto new group for Equation %s" % orig_equation.IDequation
                )
                if location_group_created:
                    new_location_groups_inserted = new_location_groups_inserted + 1

            location_group.Locations.add(location)


######################################## COMMON ##################################################

            if orig_equation.Contributor is None:
                Contributor = None
            else:
                Contributor = Institution.objects.get_or_create(Name=orig_equation.Contributor)[0]

            if orig_equation.Reference is None:
                reference = None
            else:
                reference = Reference.objects.get_or_create(
                    Label=orig_equation.Label,
                    Author=orig_equation.Author,
                    Year=orig_equation.Year,
                    Reference=orig_equation.Reference,
            )[0]

######################################## SUBMISSION ##############################################

            if orig_equation.data_submission is None:
                dataset = None
            else:
                ods = orig_equation.data_submission
                dataset = Dataset.objects.get_or_create(
                    Title = 'Allometric Equations %s' % ods.pk,
                    Uploaded_data_file = orig_equation.data_submission.submitted_file,
                    Description = orig_equation.data_submission.submitted_notes,
                    User = orig_equation.data_submission.user,
                    Data_type = 'allometric_equations',
                    Imported = orig_equation.data_submission.imported,
                    Is_restricted = False,
                )[0]


######################################## EQUATION ################################################

        
            if orig_equation.Population is None:
                population = None
            else:
                population = Population.objects.get_or_create(Name=orig_equation.Population)[0]

            new_equation = AllometricEquation(
                Allometric_equation_ID=orig_equation.ID,
                Allometric_equation_ID_original=orig_equation.ID,
                Dataset = dataset,
                X=orig_equation.X,
                Unit_X=orig_equation.Unit_X, 
                Z=orig_equation.Z,
                Unit_Z=orig_equation.Unit_Z, 
                W=orig_equation.W, 
                Unit_W=orig_equation.Unit_W,
                U=orig_equation.U,
                Unit_U=orig_equation.Unit_U,
                V=orig_equation.V,
                Unit_V=orig_equation.Unit_V,
                Min_X=orig_equation.Min_X,
                Max_X=orig_equation.Max_X, 
                Min_Z=orig_equation.Min_Z, 
                Max_Z=orig_equation.Max_Z,
                Output=orig_equation.Output,
                Output_TR=orig_equation.Output_TR,
                Unit_Y=orig_equation.Unit_Y,
                Age=orig_equation.Age,
                Veg_Component=orig_equation.Veg_Component,
                B=orig_equation.B,
                Bd=orig_equation.Bd,
                Bg=orig_equation.Bg,
                Bt=orig_equation.Bt,
                L=orig_equation.L,
                Rb=orig_equation.Rb,
                Rf=orig_equation.Rf,
                Rm=orig_equation.Rm,
                S=orig_equation.S,
                T=orig_equation.T,
                F=orig_equation.F,
                Equation=orig_equation.Equation,
                Substitute_equation=orig_equation.Substitute_equation,
                Top_dob=orig_equation.Top_dob,
                Stump_height=orig_equation.Stump_height,
                R2=orig_equation.R2,
                R2_Adjusted=orig_equation.R2_Adjusted,
                RMSE=orig_equation.RMSE,
                SEE=orig_equation.SEE,
                Corrected_for_bias=orig_equation.Corrected_for_bias,
                Bias_correction=orig_equation.Bias_correction,
                Ratio_equation=orig_equation.Ratio_equation,
                Segmented_equation=orig_equation.Segmented_equation,
                Sample_size=orig_equation.Sample_size,
                Contributor=Contributor,
                Reference=reference,
                Species_group=species_group,
                Location_group=location_group,
                Population=population
            )
            new_equation.save()
            equations_insterted = equations_insterted + 1

        print 
        self.stdout.write(
            'Inserted: {0} AllometricEquation, {1} Species, '
            '{2} original SpeciesGroup, {3} new SpeciesGroup, {4} Locations, '
            '{5} original LocationGroup, {6} new LocationGroup\n' 
            .format(
                equations_insterted, species_inserted,
                original_species_groups_inserted, new_species_groups_inserted,
                locations_inserted, original_location_groups_inserted,
                new_location_groups_inserted
            )
        )

        print "-------------- Errors ---------------"
        print 

        for key in missed_holdridge.keys():
            print 'HOLDRDIGE: ' + key 

        for key in missed_wwf.keys():
            print 'WWF: ' + key 

        for key in missed_bailey.keys():
            print 'BAILEY: ' + key 

        for key in missed_udvardy.keys():
            print 'UDVARDY: ' + key

        for key in missed_fao.keys():
            print 'FAO: ' + key









