
from globallometree.apps.raw_data.indices import RawDataIndex
from globallometree.apps.base.index_utils import RemapIndexCommand

class Command(RemapIndexCommand):
    index_cls = RawDataIndex

