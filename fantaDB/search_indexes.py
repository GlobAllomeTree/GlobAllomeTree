from haystack import indexes
from .models import fantaDB

class fantaDBIndex(indexes.SearchIndex, indexes.Indexable):
    #Full Text Search
    text = indexes.CharField(document=True, use_template=True)
    
    ecosystem = indexes.CharField(model_attr='ecosystem')
    genus     = indexes.CharField(model_attr='genus')
    species   = indexes.CharField(model_attr='species')
    
    def get_model(self):
        return fantaDB
    
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()