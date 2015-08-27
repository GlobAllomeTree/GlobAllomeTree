from rest_framework import serializers, fields
from globallometree.apps.taxonomy import models


class SpeciesLocalNameSerializer(serializers.ModelSerializer):
    Language_iso_639 = fields.CharField(source="Language_iso_639_3")
    Local_name_ID = fields.CharField(source="Species_local_name_ID")
    class Meta:
        model = models.SpeciesLocalName
        fields = ('Local_name', 'Language_iso_639', 'Local_name_latin', 'Local_name_ID')


class FamilySerializer(serializers.ModelSerializer):
    Family = fields.CharField(source="Name")

    class Meta:
        model = models.Family
        fields = ('Family', 'Family_ID', )


class GenusSerializer(serializers.ModelSerializer):
    Genus = fields.CharField(source="Name")
    Family = fields.CharField(source="Family.Name")

    Genus_ID = fields.IntegerField()
    Family_ID = fields.IntegerField(source="Family.Family_ID")
    
    class Meta:
        model = models.Genus
        fields = ('Family', 'Genus', 'Family_ID', 'Genus_ID')


class SpeciesSerializer(serializers.ModelSerializer):
   
    Family = fields.CharField(source="Genus.Family.Name")
    Genus = fields.CharField(source="Genus.Name")
    Species = fields.CharField(source="Name")
    Species_local_names = SpeciesLocalNameSerializer(
        many = True,
        source = 'Local_names'
        )
    Genus_ID = fields.IntegerField(source="Genus.Genus_ID")
    Family_ID = fields.IntegerField(source="Genus.Family.Family_ID")
    Species_author = fields.CharField(source="Author")

    class Meta:
        model = models.Species
        fields = ('Family', 
                  'Genus',
                  'Species',
                  'Species_author',
                  'Species_local_names',
                  'Family_ID',
                  'Genus_ID',
                  'Species_ID',
                  'Species_author'
                  )

class SubspeciesSerializer(serializers.ModelSerializer):
    
    Family = fields.CharField(source="Species.Genus.Family.Name")
    Genus = fields.CharField(source="Species.Genus.Name")
    Species = fields.CharField(source="Species.Name")
    Species_local_names = SpeciesLocalNameSerializer(
        many = True,
        required=False,
        source = 'Species.Local_names'
        )
    Species_ID = fields.IntegerField(source="Species.Species_ID")
    Family_ID = fields.IntegerField(source="Species.Genus.Family.Family_ID")
    Genus_ID = fields.IntegerField(source="Species.Genus.Genus_ID")

    Subspecies = fields.CharField(source="Name")
  
    Species_author = fields.SerializerMethodField()

    def get_Species_author(self, obj):
        if obj.Author:
            return obj.Author
        elif obj.Species.Author:
            return obj.Species.Author
        else:
            return None

    class Meta:
        model = models.Subspecies
        fields = ('Family', 
                  'Genus',
                  'Species',
                  'Subspecies',
                  'Species_author',
                  'Species_local_names',
                  'Family_ID',
                  'Genus_ID',
                  'Species_ID',
                  'Subspecies_ID',
                  )


class SpeciesDefinitionSerializer((serializers.ModelSerializer)):
    """
    This is basically trying to flatten out all of the species, families, local names,
    etc into a  single record
    """
   
    Family = fields.CharField(required=False, allow_null=True, source='Family.Name')
    Genus = fields.CharField(required=False,allow_null=True, source='Genus.Name')
    Species = fields.CharField(required=False,allow_null=True, source='Species.Name')
    Species_local_names = SpeciesLocalNameSerializer(
        many=True,
        required=False,
        source='Species.Local_names'
        )
    
    Subspecies = fields.CharField(required=False, allow_null=True, source='Subspecies.Name')
    Scientific_name = fields.CharField(read_only=True, allow_null=True)

    Family_ID = fields.IntegerField(required=False,allow_null=True, source='Family.pk')
    Genus_ID = fields.IntegerField(required=False,allow_null=True, source='Genus.pk')
    Species_ID = fields.IntegerField(required=False,allow_null=True, source='Species.pk')
    Subspecies_ID = fields.IntegerField(required=False,allow_null=True, source='Subspecies.pk')
    Species_author = fields.SerializerMethodField()

    def get_Species_author(self, obj):
        if obj.Subspecies and obj.Subspecies.Author:
            return obj.Subspecies.Author
        elif obj.Species and obj.Species.Author:
            return obj.Species.Author
        else:
            return None


    class Meta:
         model = models.SpeciesDefinition
         fields = (
            'Family',
            'Genus',
            'Species',
            'Subspecies',
            'Species_author',
            'Species_local_names',
            'Scientific_name',
            'Family_ID',
            'Genus_ID',
            'Species_ID',
            'Subspecies_ID'
            )


class SpeciesGroupSerializer(serializers.ModelSerializer):
    # Note that the Group is returned from a method on 
    # the SpeciesGroup model
    Group = SpeciesDefinitionSerializer(many=True, source='Species_definitions')
    Species_group_ID = fields.IntegerField()
    
    class Meta: 
        model = models.SpeciesGroup
        fields = ('Species_group_ID', 'Group')

  
    @staticmethod       
    def match_species_def_to_db(species_def):
        # Don't trust the ids we were given
        species_def['Family_ID'] = None
        species_def['Species_ID'] = None
        species_def['Genus_ID'] = None
        species_def['Subspecies_ID'] = None

        species_def['db_family'] = None
        species_def['db_genus'] = None
        species_def['db_species'] = None
        species_def['db_subspecies'] = None

        # Family and Genus are required by the parser
        try:
            species_def['db_family'] = models.Family.objects.get(Name=species_def['Family']['Name'])
            species_def['Family_ID'] = species_def['db_family'].pk
        except models.Family.DoesNotExist:
            pass
            
        # If we have the family in our db, we try to find the genus id
        if species_def['db_family']:
            try:
                species_def['db_genus'] = models.Genus.objects.get(
                    Family=species_def['db_family'],
                    Name=species_def['Genus']['Name']
                    )
                species_def['Genus_ID'] = species_def['db_genus'].pk
            except models.Genus.DoesNotExist:
                pass
                
        # If we have the genus in our db, we try to find the species id
        if species_def['db_genus'] and species_def['Species']['Name']:
            try:
                species_def['db_species'] = models.Species.objects.get(
                    Genus=species_def['db_genus'],
                    Name=species_def['Species']['Name'])
                species_def['Species_ID'] = species_def['db_species'].pk
            except models.Species.DoesNotExist:
                pass

        # If we have the species in our db, we try to find the subspecies id
        if species_def['db_species'] and species_def['Subspecies']['Name']:
            try:
                species_def['db_subspecies'] = models.Subspecies.objects.get(
                    Species=species_def['db_species'], 
                    Name=species_def['Subspecies']['Name']
                    )
                species_def['Subpsecies_ID'] = species_def['db_subspecies'].pk
            except models.Subspecies.DoesNotExist:
                pass

        return species_def

