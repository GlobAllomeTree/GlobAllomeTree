from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from optparse import make_option
from globallometree.apps.data.models import TreeEquation
from globallometree.apps.taxonomy.models import Species, Family, Genus, SpeciesGroup
from globallometree.apps.allometric_equations.models import AllometricEquation
from globallometree.apps.locations.models import BiomeFAO, BiomeUdvardy, BiomeWWF, DivisionBailey, BiomeHoldridge
from globallometree.apps.locations.models import Location, Country, Continent, LocationGroup
from globallometree.apps.allometric_equations.models import AllometricEquationPopulation, AllometricEquationEcosystem
from globallometree.apps.common.models import DataReference, Institution

class Command(BaseCommand):
    args = '<limit (optional)>'
    help = 'Imports from the old data.TreeEquation model to the new normalized structure'

    def handle(self,*args, **options):
        if len(args) == 1:
            limit = int(args[0])
        elif len(args) > 1:
            exit('Command only takes one argument <limit>')
        else:
            limit = 0

        n = 0
        equationsInsterted = 0
        speciesGroupsInserted = 0
        locationGroupsInserted = 0
        for orig_equation in TreeEquation.objects.all().iterator():
            if limit and n > limit: break;
            n = n + 1; 
            
######################################## TAXONOMY ################################################

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
                species = Species.objects.get_or_create(
                    name=orig_equation.Species, 
                    genus=genus,
                    original_ID_Species=orig_equation.ID_Species
                )[0]

            if orig_equation.Group_Species and orig_equation.ID_Group:
                species_group = SpeciesGroup.objects.get_or_create(
                    original_ID_Group=orig_equation.ID_Group,
                    name="Auto Created Group for original ID_Group %s" % orig_equation.ID_Group
                )[0]
                
                if species:
                    #It appears some species may contain 'None' species, which don't get explicitly added
                    species_group.species.add(species)
            else:
                if species:
                    species_group = SpeciesGroup(name="Auto Created Group for equation ID %s" % orig_equation.ID)
                    species_group.save()
                    species_group.species.add(species)
                    speciesGroupsInserted = speciesGroupsInserted + 1

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

            if orig_equation.Country is None:
                country = None
            else:
                country = Country.objects.get_or_create(
                    common_name=orig_equation.Country.common_name,
                    formal_name=orig_equation.Country.formal_name,
                    type=orig_equation.Country.type,
                    sub_type=orig_equation.Country.sub_type,
                    sovereignty=orig_equation.Country.sovereignty,
                    capital=orig_equation.Country.capital,
                    iso_4217_currency_code=orig_equation.Country.iso_4217_currency_code,
                    iso_4217_currency_name=orig_equation.Country.iso_4217_currency_name,
                    telephone_code=orig_equation.Country.telephone_code,
                    iso_3166_1_2_letter_code=orig_equation.Country.iso_3166_1_2_letter_code,
                    iso_3166_1_3_letter_code=orig_equation.Country.iso_3166_1_3_letter_code,
                    iso_3166_1_number=orig_equation.Country.iso_3166_1_number,
                    iana_country_code_tld=orig_equation.Country.iana_country_code_tld,
                    continent=continent
                )[0]

            location = Location.objects.get_or_create(
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
            )[0]

            if orig_equation.Group_Location:
                location_group = LocationGroup.objects.get_or_create(
                    original_Group_Location=orig_equation.Group_Location,
                    name="Auto Created Group for original Group_Location %s" % orig_equation.Group_Location
                )[0]
            else:   
                location_group = LocationGroup(name="Auto Created Group for Equation %s" % orig_equation.ID)
                location_group.save()
                locationGroupsInserted = locationGroupsInserted + 1

            location_group.locations.add(location)

######################################## COMMON ##################################################

            if orig_equation.Contributor is None:
                contributor = None
            else:
                contributor = Institution.objects.get_or_create(name=orig_equation.Population)[0]

            if orig_equation.Reference is None:
                reference = None
            else:
                reference = DataReference.objects.get_or_create(
                    label=orig_equation.Label,
                    author=orig_equation.Author,
                    year=orig_equation.Year,
                    reference=orig_equation.Reference
            )[0]

######################################## EQUATION ################################################

            if orig_equation.Population is None:
                population = None
            else:
                population = AllometricEquationPopulation.objects.get_or_create(name=orig_equation.Population)[0]

            if orig_equation.Ecosystem is None:
                ecosystem = None
            else:
                ecosystem = AllometricEquationEcosystem.objects.get_or_create(name=orig_equation.Ecosystem)[0]

            try: 
                new_equation = AllometricEquation.objects.get(IDequation=orig_equation.IDequation)
            except ObjectDoesNotExist:
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
                    location_group=location_group
                )
                new_equation.save()
                equationsInsterted = equationsInsterted + 1
                # self.stdout.write(
                #     'Created a new AllometricEquation record: ID = {0}, IDequation = {1}\n'
                #     .format(orig_equation.ID, orig_equation.IDequation)
                # )
        self.stdout.write(
            'Inserted {0} AllometricEquation, {1} SpeciesGroup, {2} LocationGroup\n'
            .format(equationsInsterted, speciesGroupsInserted, locationGroupsInserted)
        )

