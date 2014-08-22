
from globallometree.apps.accounts.search.indices import UserProfileIndex
from globallometree.apps.search_helpers.index_utils import RebuildIndexCommand

class Command(RebuildIndexCommand):
    index_cls = UserProfileIndex

