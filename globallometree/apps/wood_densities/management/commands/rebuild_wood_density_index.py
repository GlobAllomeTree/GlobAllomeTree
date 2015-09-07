
from globallometree.apps.wood_densities.indices import WoodDensityIndex
from globallometree.apps.base.index_utils import RebuildIndexCommand

class Command(RebuildIndexCommand):
    index_cls = WoodDensityIndex

