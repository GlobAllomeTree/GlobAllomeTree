
from globallometree.apps.wood_densities.search.indices import WoodDensityIndex
from globallometree.apps.search_helpers.index_utils import RebuildIndexCommand

class Command(RebuildIndexCommand):
    index_cls = WoodDensityIndex

