from django.shortcuts import render_to_response
from haystack.views import SearchView
from haystack.query import SearchQuerySet


def species(request, selected_genus=None):
    
    #Call sorl for a faceted list of genus
    sqs = SearchQuerySet().facet('genus')
    genus_list = []
    for genus_count in sqs.facet_counts()['fields']['genus']:
        genus_list.append({
            'name'  : genus_count[0],
            'count' : genus_count[1]
        
        })
    
    #Sort the list alphabetically by name
    genus_list.sort(key=lambda x : x['name'])
    
    
    
    
    
    return render_to_response('data/template.species.html', {'genus_list': genus_list }) 




class EquationSearchView(SearchView):
    def __name__(self):
        return "EquationSearchView"

    def extra_context(self):
        extra = super(EquationSearchView, self).extra_context()

        #Add stuff to extra as a dict

        return extra
