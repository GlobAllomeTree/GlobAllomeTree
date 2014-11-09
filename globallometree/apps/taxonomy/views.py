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
        context['query'] = self.request.GET.get('q', None)
        return context

    def get_queryset(self, *args, **kwargs):
    	qs = Species.objects.all().order_by('genus__family__name', 'genus__name')
    	q = self.request.GET.get('q', None)
    	if q is not None and q != '':
    		qs = qs.filter(Q(genus__family__name=q) | Q(genus__name=q) | Q(name=q))
    	return qs
