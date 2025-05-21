# PerturbDecodeMulti package

"""
PerturbDecodeMulti: A toolkit for large scale single cell perturbation screen analysis.
"""

__version__ = "0.1.0"

# Import and expose the main API
from .pertdec import *

# Make submodules accessible
from . import pertdec
from . import core
from . import data
from . import models
from . import training
from . import utils