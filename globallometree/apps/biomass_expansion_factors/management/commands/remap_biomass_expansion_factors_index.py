
from globallometree.apps.biomass_expansion_factors.indices import BiomassExpansionFactorIndex
from globallometree.apps.base.index_utils import RemapIndexCommand

class Command(RemapIndexCommand):
    index_cls = BiomassExpansionFactorIndex

