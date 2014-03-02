from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from globallometree.apps.data.models import TreeEquation
from globallometree.apps.taxonomy.models import Species, Family, Genus, SpeciesGroup
from globallometree.apps.allometric_equations.models import AllometricEquation
from globallometree.apps.locations.models import BiomeFAO, BiomeUdvardy, BiomeWWF, DivisionBailey, BiomeHoldridge
from globallometree.apps.locations.models import Location, Country, Continent, LocationGroup

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
        for orig_equation in TreeEquation.objects.all().iterator():
            n = n + 1; 
            if limit and n > limit: break;
            

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
                species = Species.objects.get_or_create(name=orig_equation.Species, 
                                                        genus=genus,
                                                        original_ID_Species=orig_equation.ID_Species)[0]

            if orig_equation.Group_Species and orig_equation.ID_Group:
                species_group = SpeciesGroup.objects.get_or_create(original_ID_Group=orig_equation.ID_Group,
                                                                   group_name="Auto Created Group for original ID_Group %s" % orig_equation.ID_Group)[0]
                
                if species:
                    #It appears some species may contain 'None' species, which don't get explicitly added
                    species_group.species.add(species)
            else:
                if species:
                    species_group = SpeciesGroup(group_name="Auto Created Group for equation ID %s" % orig_equation.ID)
                    species_group.save()
                    species_group.species.add(species)

           
           
######################################## LOCATIONS ################################################       


            #Biomes
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


             #Location now tracks Biomes, etc.. not just lat and lon... so we need unique locations per combination
            location = Location.objects.get_or_create(original_ID_Location=orig_equation.ID_Location,
                                                      name = orig_equation.Location,
                                                      Latitude = orig_equation.Latitude,
                                                      Longitude = orig_equation.Longitude,
                                                      biome_fao = biome_fao,
                                                      biome_udvardy = biome_udvardy,
                                                      biome_wwf = biome_wwf, 
                                                      division_bailey = division_bailey,
                                                      biome_holdridge = biome_holdridge,
                                                      #country=
                                                      )[0]

            if orig_equation.Group_Location:
                location_group = LocationGroup.objects.get_or_create(original_Group_Location=orig_equation.Group_Location,
                                                                     group_name="Auto Created Group for original Group_Location %s" % orig_equation.Group_Location)[0]
            else:   
                location_group = LocationGroup(group_name="Auto Created Group for Equation %s" % orig_equation.ID)
           

######################################## EQUATION ################################################       



            new_equation = AllometricEquation(
                ID = orig_equation.ID,
                IDequation = orig_equation.IDequation,
                X = orig_equation.X,
                Unit_X = orig_equation.Unit_X, 
                Z = orig_equation.Z,
                Unit_Z = orig_equation.Unit_Z, 
                W = orig_equation.W, 
                Unit_W = orig_equation.Unit_W,
                U = orig_equation.U,
                Unit_U = orig_equation.Unit_U,
                V = orig_equation.V,
                Unit_V = orig_equation.Unit_V,
                Min_X = orig_equation.Min_X,
                Max_X = orig_equation.Max_X, 
                Min_Z = orig_equation.Min_Z, 
                Max_Z = orig_equation.Max_Z,
                Output = orig_equation.Output,
                Output_TR = orig_equation.Output_TR,
                Unit_Y = orig_equation.Unit_Y,
                Age = orig_equation.Age,
                Veg_Component = orig_equation.Veg_Component,
                B = orig_equation.B,
                Bd = orig_equation.Bd,
                Bg = orig_equation.Bg,
                Bt = orig_equation.Bt,
                L = orig_equation.L,
                Rb = orig_equation.Rb,
                Rf = orig_equation.Rf,
                Rm = orig_equation.Rm,
                S = orig_equation.S,
                T = orig_equation.T,
                F = orig_equation.F,
                Equation = orig_equation.Equation,
                Substitute_equation = orig_equation.Substitute_equation,
                Top_dob = orig_equation.Top_dob,
                Stump_height = orig_equation.Stump_height,
                R2 = orig_equation.R2,
                R2_Adjusted = orig_equation.R2_Adjusted,
                RMSE = orig_equation.RMSE,
                SEE = orig_equation.SEE,
                Corrected_for_bias = orig_equation.Corrected_for_bias,
                Bias_correction = orig_equation.Bias_correction,
                Ratio_equation = orig_equation.Ratio_equation,
                Segmented_equation = orig_equation.Segmented_equation,
                Sample_size = orig_equation.Sample_size,
                species_group = species_group,
                location_group = location_group)
            
            new_equation.save()

