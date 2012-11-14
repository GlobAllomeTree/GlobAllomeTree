from haystack import indexes
from .models import TreeEquation

class TreeEquationIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    #Full Text Search
    text = indexes.CharField(document=True, use_template=True)
    
    id                              = indexes.IntegerField(model_attr='id')

    Population                      = indexes.CharField(model_attr='Population', null=True, faceted=True)
    Ecosystem                       = indexes.CharField(model_attr='Ecosystem', null=True, faceted=True)
    Genus                           = indexes.CharField(model_attr='Genus', null=True, faceted=True)
    Species                         = indexes.CharField(model_attr='Species', null=True, faceted=True)
    country                         = indexes.CharField(model_attr='country__common_name', null=True, faceted=True)
    
    Biome_FAO                       = indexes.CharField(model_attr='Biome_FAO', null=True, faceted=True)
    Biome_UDVARDY                   = indexes.CharField(model_attr='Biome_UDVARDY', null=True, faceted=True)
    Biome_WWF                       = indexes.CharField(model_attr='Biome_WWF', null=True, faceted=True) 
    Division_BAILEY                 = indexes.CharField(model_attr='Division_BAILEY', null=True, faceted=True) 
    Biome_HOLDRIDGE                 = indexes.CharField(model_attr='Biome_HOLDRIDGE', null=True, faceted=True)
     
    X                               = indexes.CharField(model_attr='X', null=True)
    Unit_X                          = indexes.CharField(model_attr='Unit_X', null=True)
    Z                               = indexes.CharField(model_attr='Z', null=True)
    Unit_Z                          = indexes.CharField(model_attr='Unit_Z', null=True) 
    W                               = indexes.CharField(model_attr='W', null=True)
    Unit_W                          = indexes.CharField(model_attr='Unit_W', null=True)
    U                               = indexes.CharField(model_attr='U', null=True)
    Unit_U                          = indexes.CharField(model_attr='Unit_U', null=True) 
    V                               = indexes.CharField(model_attr='V', null=True)
    Unit_V                          = indexes.CharField(model_attr='Unit_V', null=True)
    
    Min_X                           = indexes.FloatField(model_attr='Min_X',null=True)
    Max_X                           = indexes.FloatField(model_attr='Max_X',null=True)
    Min_Z                           = indexes.FloatField(model_attr='Min_Z',null=True)
    Max_Z                           = indexes.FloatField(model_attr='Max_Z',null=True)
    
    Output                          = indexes.CharField(model_attr='Output', null=True, faceted=True)
    Unit_Y                          = indexes.CharField(model_attr='Unit_Y', null=True)
    
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
    
    Equation                      = indexes.NgramField(model_attr='Equation', null=True)
    
    Author                          = indexes.CharField(model_attr='author', null=True, faceted=True, indexed=True)
    
   
    Year                            = indexes.IntegerField(model_attr='year', null=True)
    Reference                       = indexes.CharField(model_attr='reference', null=True, faceted=True) 
    

    #ordering
    Author_order                    = indexes.CharField(model_attr='author', null=True, indexed=False)
    Biome_FAO_order                 = indexes.CharField(model_attr='Biome_FAO', null=True,  indexed=False)
    Genus_order                     = indexes.CharField(model_attr='Genus', null=True, indexed=False)
    Species_order                   = indexes.CharField(model_attr='Species', null=True, indexed=False)
    Output_order                    = indexes.CharField(model_attr='Output', null=True, indexed=False)
    Country_order                   = indexes.CharField(model_attr='country__common_name', null=True, indexed=False)


    #autocomplete lookups
    Population_auto                 = indexes.EdgeNgramField(model_attr='Population')
    Ecosystem_auto                  = indexes.EdgeNgramField(model_attr='Ecosystem') 
    Genus_auto                      = indexes.EdgeNgramField(model_attr='Genus')
    Species_auto                    = indexes.EdgeNgramField(model_attr='Species')
    Country_auto                    = indexes.EdgeNgramField(model_attr='country')
    Biome_FAO_auto                  = indexes.EdgeNgramField(model_attr='Biome_FAO')
    Biome_UDVARDY_auto              = indexes.EdgeNgramField(model_attr='Biome_UDVARDY')
    Biome_WWF_auto                  = indexes.EdgeNgramField(model_attr='Biome_WWF')
    Division_BAILEY_auto            = indexes.EdgeNgramField(model_attr='Division_BAILEY')
    Biome_HOLDRIDGE_auto            = indexes.EdgeNgramField(model_attr='Biome_HOLDRIDGE')
    Author_auto                     = indexes.EdgeNgramField(model_attr='author')
    Reference_auto                  = indexes.EdgeNgramField(model_attr='reference') 
    Output_auto                     = indexes.EdgeNgramField(model_attr='Output') 


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
        return TreeEquation
    
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()