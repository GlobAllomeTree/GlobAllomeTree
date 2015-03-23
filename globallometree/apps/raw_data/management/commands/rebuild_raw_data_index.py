
from globallometree.apps.raw_data.indices import RawDataIndex
from globallometree.apps.search_helpers.index_utils import RebuildIndexCommand

class Command(RebuildIndexCommand):
    index_cls = RawDataIndex

