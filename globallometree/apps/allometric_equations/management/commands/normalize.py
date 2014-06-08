import os
import sys
import csv
import codecs

from django.db import transaction
from django.conf import settings
from django.core.management.base import BaseCommand
from globallometree.apps.data.models import TreeEquation, Country as OldCountry
from globallometree.apps.taxonomy.models import Species, Family, Genus, SpeciesGroup
from globallometree.apps.allometric_equations.models import AllometricEquation, Submission
from globallometree.apps.locations.models import BiomeFAO, BiomeUdvardy, BiomeWWF, DivisionBailey, BiomeHoldridge
from globallometree.apps.locations.models import Location, Country, Continent, LocationGroup
from globallometree.apps.allometric_equations.models import Population, Ecosystem
from globallometree.apps.common.models import DataReference, Institution

class Command(BaseCommand):
    args = '<limit (optional)>'
    help = 'Imports from the old data.TreeEquation model to the new normalized structure'

    def handle(self,*args, **options):

        #First make sure we import all of the countries
        country_data = self.load_countries_csv()

        continents = {
            'AF' : 'Africa',
            'AN' : 'Antatica',
            'AS' : 'Asia',
            'EU' : 'Europe',
            'NA' : 'North America',
            'OC' : 'Oceania',
            'SA' : 'South America'
        }

        for key in continents.keys():
            name = continents[key]
            continents[key] = Continent.objects.create(code=key, name=name)

        for cd_row in country_data:
            Country.objects.create(
                common_name=cd_row['ISOen_name'],
                formal_name=cd_row['ISOen_proper'],
                common_name_fr=cd_row['ISOfr_name'],
                formal_name_fr=cd_row['ISOfr_proper'],
                continent=continents[cd_row['continent']],
                iso3166a2=cd_row['ISO3166A2'],
                iso3166a3=cd_row['ISO3166A3'],
                iso3166n3=cd_row['ISO3166N3'],
                centroid_latitude = cd_row['latitude'],
                centroid_longitude = cd_row['longitude'] 
            )

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
                family = Family.objects.get_or_create(name=orig_equation.Family)[0]
            
            if orig_equation.Genus is None:
                genus = None
            else:
                genus = Genus.objects.get_or_create(name=orig_equation.Genus, 
                                                    family=family)[0]

            if orig_equation.ID_Species is None:
                species = None
            else:
                species, species_created = Species.objects.get_or_create(
                    name=orig_equation.Species, 
                    genus=genus,
                    original_ID_Species=orig_equation.ID_Species
                )
                if species_created:
                    species_inserted = species_inserted + 1

            if species:
                if orig_equation.Group_Species and orig_equation.ID_Group:
                    species_group, species_group_created = SpeciesGroup.objects.get_or_create(
                        original_ID_Group=orig_equation.ID_Group,
                        name="Auto Created Group for original ID_Group %s" % orig_equation.ID_Group
                    )
                    if species_group_created:
                        original_species_groups_inserted = original_species_groups_inserted + 1
                else:
                    species_group, species_group_created = SpeciesGroup.objects.get_or_create(
                        name="Auto Created Group for equation ID %s" % orig_equation.IDequation
                    )
                    if species_group_created:
                        new_species_groups_inserted = new_species_groups_inserted + 1
                
                #It appears some species may contain 'None' species, which don't get explicitly added
                species_group.species.add(species)

######################################## LOCATIONS ################################################

            if orig_equation.Biome_FAO is None:
                biome_fao = None
            else:
                biome_fao = BiomeFAO.objects.get_or_create(name=orig_equation.Biome_FAO)[0]

            if orig_equation.Biome_UDVARDY is None:
                biome_udvardy = None
            else:
                biome_udvardy = BiomeUdvardy.objects.get_or_create(name=orig_equation.Biome_UDVARDY)[0]

            if orig_equation.Biome_WWF is None:
                biome_wwf = None
            else:
                biome_wwf = BiomeWWF.objects.get_or_create(name=orig_equation.Biome_WWF)[0]

            if orig_equation.Division_BAILEY is None:
                division_bailey = None
            else:
                division_bailey = DivisionBailey.objects.get_or_create(name=orig_equation.Division_BAILEY)[0]

            if orig_equation.Biome_HOLDRIDGE is None:
                biome_holdridge = None
            else:
                biome_holdridge = BiomeHoldridge.objects.get_or_create(name=orig_equation.Biome_HOLDRIDGE)[0]

            if orig_equation.Continent is None:
                continent = None
            else:
                continent = Continent.objects.get_or_create(name=orig_equation.Continent)[0]

            if orig_equation.Country is None or not orig_equation.Country.iso_3166_1_2_letter_code:
                country = None
            else:
                country = Country.objects.get(iso3166a2=orig_equation.Country.iso_3166_1_2_letter_code)
                if not country.continent and continent is not None:
                    country.continent = continent
                    country.save()
                        

            location, location_created = Location.objects.get_or_create(
                original_ID_Location=orig_equation.ID_Location,
                name=orig_equation.Location,
                Latitude=orig_equation.Latitude,
                Longitude=orig_equation.Longitude,
                biome_fao=biome_fao,
                biome_udvardy=biome_udvardy,
                biome_wwf=biome_wwf, 
                division_bailey=division_bailey,
                biome_holdridge=biome_holdridge,
                country=country
            )
            if location_created:
                locations_inserted = locations_inserted + 1

            if orig_equation.Group_Location:
                location_group, location_group_created = LocationGroup.objects.get_or_create(
                    original_Group_Location=orig_equation.Group_Location,
                    name="Auto Created Group for original Group_Location %s" % orig_equation.Group_Location
                )
                if location_group_created:
                    original_location_groups_inserted = original_location_groups_inserted + 1
            else:   
                location_group, location_group_created = LocationGroup.objects.get_or_create(
                    name="Auto Created Group for Equation %s" % orig_equation.IDequation
                )
                if location_group_created:
                    new_location_groups_inserted = new_location_groups_inserted + 1

            location_group.locations.add(location)

######################################## COMMON ##################################################

            if orig_equation.Contributor is None:
                contributor = None
            else:
                contributor = Institution.objects.get_or_create(name=orig_equation.Contributor)[0]

            if orig_equation.Reference is None:
                reference = None
            else:
                reference = DataReference.objects.get_or_create(
                    label=orig_equation.Label,
                    author=orig_equation.Author,
                    year=orig_equation.Year,
                    reference=orig_equation.Reference,
                    original_ID_REF=orig_equation.ID_REF
            )[0]

######################################## SUBMISSION ##############################################

            if orig_equation.data_submission is None:
                data_submission = None
            else:
                ods = orig_equation.data_submission
                data_submission = Submission.objects.get_or_create(
                    submitted_file=orig_equation.data_submission.submitted_file,
                    submitted_notes=orig_equation.data_submission.submitted_notes,
                    user=orig_equation.data_submission.user,
                    imported=orig_equation.data_submission.imported
                )[0]
                #Fix the upload date
                Submission.objects.filter(pk=data_submission.pk).update(date_uploaded=ods.date_uploaded)

######################################## EQUATION ################################################

            if orig_equation.Population is None:
                population = None
            else:
                population = Population.objects.get_or_create(name=orig_equation.Population)[0]

            if orig_equation.Ecosystem is None:
                ecosystem = None
            else:
                ecosystem = Ecosystem.objects.get_or_create(name=orig_equation.Ecosystem)[0]

            try: 
                new_equation = AllometricEquation.objects.get(IDequation=orig_equation.IDequation)
            except AllometricEquation.DoesNotExist:
                new_equation = AllometricEquation(
                    ID=orig_equation.ID,
                    IDequation=orig_equation.IDequation,
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
                    population=population,
                    ecosystem=ecosystem,
                    contributor=contributor,
                    reference=reference,
                    species_group=species_group,
                    location_group=location_group,
                    data_submission=data_submission
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

    def load_countries_csv(self):
        #csv file with country lats/lons
        csv_file_path = os.path.join(settings.BASE_PATH, 'globallometree', 'apps', 'locations', 'resources', 'cow.txt')
        headers = []
        countries = []

        def clean(row):
            fields = row.replace('\r', '').replace(u'\ufeff','').split(';')
            fields = [v.strip() for v in fields]
            return fields

        with codecs.open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            for row in csv_file:
                if not len(headers):
                    headers = clean(row)
                    continue
                countries.append(dict(zip(headers, clean(row))))

        return countries
