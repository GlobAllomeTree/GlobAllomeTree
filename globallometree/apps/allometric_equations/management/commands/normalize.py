from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from globallometree.apps.data.models import TreeEquation
from globallometree.apps.taxonomy.models import Species, Family, Genus, SpeciesGroup
from globallometree.apps.allometric_equations.models import AllometricEquation

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
            
            if orig_equation.Family is None:
                family = None
            else:
                family = Family.objects.get_or_create(name=orig_equation.Family)[0]
            
            if orig_equation.Genus is None:
                genus = None
            else:
                genus = Genus.objects.get_or_create(name=orig_equation.Genus, 
                                                    family=family)[0]

            if orig_equation.Species is None:
                species = None
            else:
                species = Species.objects.get_or_create(name=orig_equation.Species, 
                                                        genus=genus,
                                                        original_ID_Species=orig_equation.ID_Species)[0]

            if orig_equation.Group_Species and orig_equation.ID_Group:
                species_group = SpeciesGroup.objects.get_or_create(original_ID_Group=orig_equation.ID_Group,
                                                                   group_name="Auto Created Group for original ID_Group %s" % orig_equation.ID_Group)[0]
                
                if species:
                    #It appears some species groups may contain 'None' species
                    #which probably represents the fact that no species was available 
                    #for the equation? maybe?
                    species_group.species.add(species)


            new_equation = AllometricEquation(
                
                IDequation = models.IntegerField(null=True, blank=True) )


