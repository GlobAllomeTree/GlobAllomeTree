
from apps.biomass_expansion_factors.indices import BiomassExpansionFactorIndex
from apps.search_helpers.index_utils import RebuildIndexCommand

class Command(RebuildIndexCommand):
    index_cls = BiomassExpansionFactorIndex

