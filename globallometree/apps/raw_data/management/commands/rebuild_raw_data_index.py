
from apps.raw_data.indices import RawDataIndex
from apps.search_helpers.index_utils import RebuildIndexCommand

class Command(RebuildIndexCommand):
    index_cls = RawDataIndex

