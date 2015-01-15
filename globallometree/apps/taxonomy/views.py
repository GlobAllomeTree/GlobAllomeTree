from django.views.generic.list import ListView
from django.db.models import Q
from .models import Species, Genus, Family

class SpeciesListView(ListView):
    model = Species
    template = 'taxonomy/species_list.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(SpeciesListView, self).get_context_data(**kwargs)
        context['species_count'] = Species.objects.all().count()
        context['family_count'] = Family.objects.all().count()
        context['genus_count'] = Genus.objects.all().count()
        context['query'] = self.request.GET.get('q', '')
        return context

    def get_queryset(self, *args, **kwargs):
    	qs = Species.objects.all().order_by('Genus__Family__Name', 'Genus__Name')
    	q = self.request.GET.get('q', None)
    	if q is not None and q != '':
    		qs = qs.filter(Q(Genus__Family__Name=q) | Q(Genus__Name=q) | Q(Name=q))
    	return qs
