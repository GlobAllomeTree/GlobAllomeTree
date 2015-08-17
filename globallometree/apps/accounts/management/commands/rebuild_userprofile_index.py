
from apps.accounts.search.indices import UserProfileIndex
from apps.search_helpers.index_utils import RebuildIndexCommand

class Command(RebuildIndexCommand):
    index_cls = UserProfileIndex

