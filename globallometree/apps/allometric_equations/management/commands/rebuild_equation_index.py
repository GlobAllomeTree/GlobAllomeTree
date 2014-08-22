
from globallometree.apps.allometric_equations.search.indices import AllometricEquationIndex
from globallometree.apps.search_helpers.index_utils import RebuildIndexCommand

class Command(RebuildIndexCommand):
    index_cls = AllometricEquationIndex

