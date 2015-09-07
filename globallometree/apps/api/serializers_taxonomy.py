from rest_framework import serializers, fields
from globallometree.apps.taxonomy import models


class SpeciesLocalNameSerializer(serializers.ModelSerializer):
    Language_iso_639 = fields.CharField(source="Language_iso_639_3", required=False)
    Local_name_ID = fields.CharField(source="ID_Local_name", read_only=True, required=False)
    class Meta:
        model = models.SpeciesLocalName
        fields = ('Local_name', 'Language_iso_639', 'Local_name_latin', 'Local_name_ID')



class FamilySerializer(serializers.ModelSerializer):
    Family = fields.CharField(source="Name")

    class Meta:
        model = models.Family
        fields = ('Family', 'ID_Family', )


class GenusSerializer(serializers.ModelSerializer):
    Genus = fields.CharField(source="Name")
    Family = fields.CharField(source="Family.Name")

    ID_Genus = fields.IntegerField()
    ID_Family = fields.IntegerField(source="Family.ID_Family")
    
    class Meta:
        model = models.Genus
        fields = ('Family', 'Genus', 'ID_Family', 'ID_Genus')


class SpeciesSerializer(serializers.ModelSerializer):
   
    Family = fields.CharField(source="Genus.Family.Name")
    Genus = fields.CharField(source="Genus.Name")
    Species = fields.CharField(source="Name")
    Species_local_names = SpeciesLocalNameSerializer(
        many = True,
        source = 'Local_names'
        )
    ID_Genus = fields.IntegerField(source="Genus.ID_Genus")
    ID_Family = fields.IntegerField(source="Genus.Family.ID_Family")
    Species_author = fields.CharField(source="Author")

    class Meta:
        model = models.Species
        fields = ('Family', 
                  'Genus',
                  'Species',
                  'Species_author',
                  'Species_local_names',
                  'ID_Family',
                  'ID_Genus',
                  'ID_Species',
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
    ID_Species = fields.IntegerField(source="Species.ID_Species")
    ID_Family = fields.IntegerField(source="Species.Genus.Family.ID_Family")
    ID_Genus = fields.IntegerField(source="Species.Genus.ID_Genus")

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
                  'ID_Family',
                  'ID_Genus',
                  'ID_Species',
                  'ID_Subspecies',
                  )


class SpeciesDefinitionSerializer((serializers.ModelSerializer)):
    """
    This is basically trying to flatten out all of the species, families, local names,
    etc into a  single record
    """
   
    Family = fields.CharField(required=False, allow_null=True, source='Family.Name', max_length=120)
    Genus = fields.CharField(required=False,allow_null=True, source='Genus.Name', max_length=120)
    Species = fields.CharField(required=False,allow_null=True, source='Species.Name', max_length=120)
    Species_local_names = SpeciesLocalNameSerializer(
        many=True,
        required=False,
        source='Species.Local_names'
        )
    
    Subspecies = fields.CharField(required=False, allow_null=True, source='Subspecies.Name', max_length=120)
    Species_author = fields.CharField(required=False,allow_null=True, max_length=120)

    Scientific_name = fields.CharField(read_only=True, allow_null=True)

    ID_Family = fields.IntegerField(required=False,allow_null=True, source='Family.pk')
    ID_Genus = fields.IntegerField(required=False,allow_null=True, source='Genus.pk')
    ID_Species = fields.IntegerField(required=False,allow_null=True, source='Species.pk')
    ID_Subspecies = fields.IntegerField(required=False,allow_null=True, source='Subspecies.pk')
   

    def get_Species_author(self, obj):
        if self.Subspecies and self.Subspecies.Species_author:
            return self.Subspecies.Species_author
        elif self.Species and self.Species.Species_author:
            return self.Species_author
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
            'ID_Family',
            'ID_Genus',
            'ID_Species',
            'ID_Subspecies'
            )


class SpeciesGroupSerializer(serializers.ModelSerializer):
    # Note that the Group is returned from a method on 
    # the SpeciesGroup model
    Group = SpeciesDefinitionSerializer(many=True, source='Species_definitions')
    ID_Species_group = fields.IntegerField()
    
    class Meta: 
        model = models.SpeciesGroup
        fields = ('ID_Species_group', 'Group')

  
    @staticmethod       
    def match_species_def_to_db(species_def):
        # Don't trust the ids we were given
        species_def['ID_Family'] = None
        species_def['ID_Species'] = None
        species_def['ID_Genus'] = None
        species_def['ID_Subspecies'] = None

        species_def['db_family'] = None
        species_def['db_genus'] = None
        species_def['db_species'] = None
        species_def['db_subspecies'] = None

        # Family and Genus are required by the parser
        try:
            species_def['db_family'] = models.Family.objects.get(Name=species_def['Family']['Name'])
            species_def['ID_Family'] = species_def['db_family'].pk
        except models.Family.DoesNotExist:
            pass
            
        # If we have the family in our db, we try to find the genus id
        if species_def['db_family']:
            try:
                species_def['db_genus'] = models.Genus.objects.get(
                    Family=species_def['db_family'],
                    Name=species_def['Genus']['Name']
                    )
                species_def['ID_Genus'] = species_def['db_genus'].pk
            except models.Genus.DoesNotExist:
                pass
                
        # If we have the genus in our db, we try to find the species id
        if species_def['db_genus'] and species_def['Species']['Name']:
            try:
                species_def['db_species'] = models.Species.objects.get(
                    Genus=species_def['db_genus'],
                    Name=species_def['Species']['Name'])
                species_def['ID_Species'] = species_def['db_species'].pk

                if len(species_def['Species']['Local_names']):
                    for index, sln in enumerate(species_def['Species']['Local_names']):
                        species_def['Species']['Local_names'][index]['db_local_name'] = None
                        try:
                            species_def['Species']['Local_names'][index]['db_local_name'] = \
                                models.SpeciesLocalName.objects.get(
                                    Species=species_def['db_species'],
                                    Local_name=sln['Local_name'],
                                    Local_name_latin=sln['Local_name_latin'],
                                    Language_iso_639_3=sln['Language_iso_639_3'])
                        except:
                            pass

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

        import pdb; pdb.set_trace()

        return species_def
