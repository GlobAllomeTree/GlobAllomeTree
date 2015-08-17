
from apps.wood_densities.indices import WoodDensityIndex
from apps.search_helpers.index_utils import RebuildIndexCommand

class Command(RebuildIndexCommand):
    index_cls = WoodDensityIndex

