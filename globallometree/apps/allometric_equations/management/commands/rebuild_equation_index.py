
from apps.allometric_equations.indices import AllometricEquationIndex
from apps.search_helpers.index_utils import RebuildIndexCommand

class Command(RebuildIndexCommand):
    index_cls = AllometricEquationIndex

