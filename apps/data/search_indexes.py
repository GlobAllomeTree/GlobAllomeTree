from haystack import indexes
from .models import TreeEquation

class TreeEquationIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    #Full Text Search
    text = indexes.CharField(document=True, use_template=True)
    
    id                              = indexes.IntegerField(model_attr='id')

    population                      = indexes.CharField(model_attr='population', null=True, faceted=True, indexed=False)
    ecosystem                       = indexes.CharField(model_attr='ecosystem', null=True, faceted=True, indexed=False)
    genus                           = indexes.CharField(model_attr='genus', null=True, faceted=True, indexed=False)
    species                         = indexes.CharField(model_attr='species', null=True, faceted=True, indexed=False)
    country                         = indexes.CharField(model_attr='country__common_name', null=True, faceted=True, indexed=False)
    
    biome_FAO                       = indexes.CharField(model_attr='biome_FAO', null=True, faceted=True, indexed=False)
    biome_UDVARDY                   = indexes.CharField(model_attr='biome_UDVARDY', null=True, faceted=True, indexed=False)
    biome_WWF                       = indexes.CharField(model_attr='biome_WWF', null=True, faceted=True, indexed=False) 
    division_BAILEY                 = indexes.CharField(model_attr='division_BAILEY', null=True, faceted=True, indexed=False) 
    biome_HOLDRIDGE                 = indexes.CharField(model_attr='biome_HOLDRIDGE', null=True, faceted=True, indexed=False)
     
    X                               = indexes.CharField(model_attr='X', null=True)
    unit_X                          = indexes.CharField(model_attr='unit_X', null=True)
    Z                               = indexes.CharField(model_attr='Z', null=True)
    unit_Z                          = indexes.CharField(model_attr='unit_Z', null=True) 
    W                               = indexes.CharField(model_attr='W', null=True)
    unit_W                          = indexes.CharField(model_attr='unit_W', null=True)
    U                               = indexes.CharField(model_attr='U', null=True)
    unit_U                          = indexes.CharField(model_attr='unit_U', null=True) 
    V                               = indexes.CharField(model_attr='V', null=True)
    unit_V                          = indexes.CharField(model_attr='unit_V', null=True)
    
    min_X                           = indexes.FloatField(model_attr='min_X',null=True)
    max_X                           = indexes.FloatField(model_attr='max_X',null=True)
    min_H                           = indexes.FloatField(model_attr='min_H',null=True)
    max_H                           = indexes.FloatField(model_attr='max_H',null=True)
    
    output                          = indexes.CharField(model_attr='output', null=True, faceted=True)
    unit_Y                          = indexes.CharField(model_attr='unit_Y', null=True)
    
    B                               = indexes.BooleanField(model_attr='B', null=True)
    Bd                              = indexes.BooleanField(model_attr='Bd', null=True)
    Bg                              = indexes.BooleanField(model_attr='Bg', null=True)
    Bt                              = indexes.BooleanField(model_attr='Bt', null=True)
    L                               = indexes.BooleanField(model_attr='L', null=True)
    Rb                              = indexes.BooleanField(model_attr='Rb', null=True)
    Rf                              = indexes.BooleanField(model_attr='Rf', null=True)
    Rm                              = indexes.BooleanField(model_attr='Rm', null=True)
    S                               = indexes.BooleanField(model_attr='S', null=True)
    T                               = indexes.BooleanField(model_attr='T', null=True)
    F                               = indexes.BooleanField(model_attr='F', null=True)
    
    equation_y                      = indexes.NgramField(model_attr='equation_y', null=True)
    
    author                          = indexes.CharField(model_attr='author', null=True, faceted=True, indexed=True)
    author_order                    = indexes.CharField(model_attr='author', null=True, faceted=True, indexed=False)
   
    year                            = indexes.IntegerField(model_attr='year', null=True)
    reference                       = indexes.CharField(model_attr='reference', null=True, faceted=True) 
    
      
    # We add these for autocomplete lookups
    population_auto                 = indexes.EdgeNgramField(model_attr='population')
    ecosystem_auto                  = indexes.EdgeNgramField(model_attr='ecosystem') 
    genus_auto                      = indexes.EdgeNgramField(model_attr='genus')
    species_auto                    = indexes.EdgeNgramField(model_attr='species')
    country_auto                    = indexes.EdgeNgramField(model_attr='country')
    biome_FAO_auto                  = indexes.EdgeNgramField(model_attr='biome_FAO')
    biome_UDVARDY_auto              = indexes.EdgeNgramField(model_attr='biome_UDVARDY')
    biome_WWF_auto                  = indexes.EdgeNgramField(model_attr='biome_WWF')
    division_BAILEY_auto            = indexes.EdgeNgramField(model_attr='division_BAILEY')
    biome_HOLDRIDGE_auto            = indexes.EdgeNgramField(model_attr='biome_HOLDRIDGE')
    author_auto                     = indexes.EdgeNgramField(model_attr='author')
    reference_auto                  = indexes.EdgeNgramField(model_attr='reference') 
    output_auto                     = indexes.EdgeNgramField(model_attr='output') 


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
    def prepare_max_X(self, obj):
        return self._to_float(obj.max_X)
    
    def prepare_min_X(self, obj):
        return self._to_float(obj.max_X)
    
    def prepare_max_H(self, obj):
        return self._to_float(obj.max_X)
    
    def prepare_min_H(self, obj):
        return self._to_float(obj.max_X)
      
    def get_model(self):
        """Let haystack know which model we are indexing"""
        return TreeEquation
    
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()