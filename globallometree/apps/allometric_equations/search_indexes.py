from haystack import indexes
from .models import AllometricEquation

class AllometricEquationIndex(indexes.SearchIndex, indexes.Indexable):
    #Full Text Search
    text = indexes.CharField(document=True, use_template=True)
    
    id = indexes.IntegerField(model_attr='ID')

    Population = indexes.CharField(model_attr='population__name', null=True)
    Ecosystem = indexes.CharField(model_attr='ecosystem__name', null=True)
    Genus = indexes.CharField(model_attr='species_group__species__genus__name', null=True, faceted=True)
    Species = indexes.CharField(model_attr='species_group__species__name', null=True, faceted=True)
    Country = indexes.CharField(model_attr='location_group__locations__country__common_name', null=True)
    
    Biome_FAO = indexes.CharField(model_attr='location_group__locations__biome_fao__name', null=True)
    Biome_UDVARDY = indexes.CharField(model_attr='location_group__locations__biome_udvardy__name', null=True)
    Biome_WWF = indexes.CharField(model_attr='location_group__locations__biome_wwf__name', null=True) 
    Division_BAILEY = indexes.CharField(model_attr='location_group__locations__division_bailey__name', null=True) 
    Biome_HOLDRIDGE = indexes.CharField(model_attr='location_group__locations__biome_holdridge__name', null=True)
     
    X = indexes.CharField(model_attr='X', null=True)
    Unit_X = indexes.CharField(model_attr='Unit_X', null=True)
    Z = indexes.CharField(model_attr='Z', null=True)
    Unit_Z = indexes.CharField(model_attr='Unit_Z', null=True) 
    W = indexes.CharField(model_attr='W', null=True)
    Unit_W = indexes.CharField(model_attr='Unit_W', null=True)
    U = indexes.CharField(model_attr='U', null=True)
    Unit_U = indexes.CharField(model_attr='Unit_U', null=True) 
    V = indexes.CharField(model_attr='V', null=True)
    Unit_V = indexes.CharField(model_attr='Unit_V', null=True)
    
    Min_X = indexes.FloatField(model_attr='Min_X',null=True)
    Max_X = indexes.FloatField(model_attr='Max_X',null=True)
    Min_Z = indexes.FloatField(model_attr='Min_Z',null=True)
    Max_Z = indexes.FloatField(model_attr='Max_Z',null=True)
    
    Output = indexes.CharField(model_attr='Output', null=True)
    Unit_Y = indexes.CharField(model_attr='Unit_Y', null=True)
    
    B = indexes.BooleanField(model_attr='B')
    Bd = indexes.BooleanField(model_attr='Bd')
    Bg = indexes.BooleanField(model_attr='Bg')
    Bt = indexes.BooleanField(model_attr='Bt')
    L = indexes.BooleanField(model_attr='L')
    Rb = indexes.BooleanField(model_attr='Rb')
    Rf = indexes.BooleanField(model_attr='Rf')
    Rm = indexes.BooleanField(model_attr='Rm')
    S = indexes.BooleanField(model_attr='S')
    T = indexes.BooleanField(model_attr='T')
    F = indexes.BooleanField(model_attr='F')
    
    Equation = indexes.NgramField(model_attr='Equation', null=True)
    
    Author = indexes.CharField(model_attr='reference__author', null=True, indexed=True, faceted=True)
    Year = indexes.CharField(model_attr='reference__year', null=True)
    Reference = indexes.CharField(model_attr='reference__reference', null=True, faceted=True) 
    
    #ordering
    Author_order = indexes.CharField(model_attr='reference__author', null=True, indexed=False)
    Biome_FAO_order = indexes.CharField(model_attr='location_group__locations__biome_fao__name', null=True,  indexed=False)
    Genus_order = indexes.CharField(model_attr='species_group__species__genus__name', null=True, indexed=False)
    Species_order = indexes.CharField(model_attr='species_group__species__name', null=True, indexed=False)
    Output_order = indexes.CharField(model_attr='Output', null=True, indexed=False)
#    Country_order = indexes.CharField(model_attr='location_group__locations__country__common_name', null=True, indexed=False)

    #autocomplete lookups
    Genus_auto = indexes.EdgeNgramField(model_attr='species_group__species__genus__name', null=True)
    Species_auto = indexes.EdgeNgramField(model_attr='species_group__species__name', null=True)
    Author_auto = indexes.EdgeNgramField(model_attr='reference__author', null=True)
    Reference_auto = indexes.EdgeNgramField(model_attr='reference__reference', null=True)

    def _to_float(self, val):
        if val is None:
            return None
        #By returning a None value, the row will be excluded from the result set
        #when the value is not known and that value is included in the search
        
        elif val:
            return float(val)  
        else:
            return float(0)
    
    #Convert the decimals to floats so we can so range filters on them
    def prepare_Max_X(self, obj):
        return self._to_float(obj.Max_X)
    
    def prepare_Min_X(self, obj):
        return self._to_float(obj.Max_X)
    
    def prepare_Max_Z(self, obj):
        return self._to_float(obj.Max_X)
    
    def prepare_Min_Z(self, obj):
        return self._to_float(obj.Max_X)
      
    def get_model(self):
        """Let haystack know which model we are indexing"""
        return AllometricEquation
    
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_ecosystem_name(self, obj):
        if obj.ecosystem is None:
            return ''
        else:
            return obj.ecosystem.name

    def prepare_location_group_locations_country_common_name(self, obj):
        if obj.location_group is None:
            return ''
        else:
            return [
                ('' if location.country is None else location.country.common_name)
                for location in obj.location_group.locations.all()
            ]