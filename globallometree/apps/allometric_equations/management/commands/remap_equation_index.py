
from globallometree.apps.allometric_equations.indices import AllometricEquationIndex
from globallometree.apps.base.index_utils import RemapIndexCommand

class Command(RemapIndexCommand):
    index_cls = AllometricEquationIndex

