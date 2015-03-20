
from globallometree.apps.biomass_expansion_factors.search.indices import BiomassExpansionFactorIndex
from globallometree.apps.search_helpers.index_utils import RebuildIndexCommand

class Command(RebuildIndexCommand):
    index_cls = BiomassExpansionFactorIndex

