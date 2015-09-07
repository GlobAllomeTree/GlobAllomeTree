
from globallometree.apps.biomass_expansion_factors.indices import BiomassExpansionFactorIndex
from globallometree.apps.base.index_utils import RebuildIndexCommand

class Command(RebuildIndexCommand):
    index_cls = BiomassExpansionFactorIndex

