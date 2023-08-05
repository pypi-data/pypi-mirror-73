from pyinstrument_patch.profiler import Profiler
import warnings

__version__ = '0.0.2'

# enable deprecation warnings
warnings.filterwarnings("once", ".*", DeprecationWarning, r"pyinstrument_patch\..*")
