
from globallometree.apps.allometric_equations.indices import AllometricEquationIndex
from globallometree.apps.base.index_utils import RebuildIndexCommand

class Command(RebuildIndexCommand):
    index_cls = AllometricEquationIndex

