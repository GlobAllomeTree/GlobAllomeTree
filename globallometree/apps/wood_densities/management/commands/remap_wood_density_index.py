
from globallometree.apps.wood_densities.indices import WoodDensityIndex
from globallometree.apps.base.index_utils import RemapIndexCommand

class Command(RemapIndexCommand):
    index_cls = WoodDensityIndex

