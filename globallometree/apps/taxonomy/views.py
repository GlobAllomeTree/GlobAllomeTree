from django.views.generic.base import TemplateView
from globallometree.apps.accounts.mixins import RestrictedPageMixin


class SpeciesListView(RestrictedPageMixin, TemplateView):
    template_name = 'taxonomy/species_list.html'

    def get_context_data(self, **kwargs):
        context = super(SpeciesListView, self).get_context_data(**kwargs)
    
        context['query'] = self.request.GET.get('q', '')
        return context
