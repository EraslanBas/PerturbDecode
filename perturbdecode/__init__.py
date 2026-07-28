"""PerturbDecode: an end-to-end toolkit for single-cell perturbation screen analysis.

The high-level pipeline steps are re-exported at the top level, so the common
usage is::

    import perturbdecode as pd

    pd.createTrainValData(adata, "perturbation", categories, "out/")
    pd.runTrainingComBVAE(...)
    pd.extract_model_embeddings(...)

See :mod:`perturbdecode.pertdec` for the individual steps.
"""

__version__ = "0.1.0"

# Import and expose the main API
from .pertdec import *  # noqa: F401,F403
from .pertdec import __all__ as _pertdec_all

# Make submodules accessible
from . import pertdec  # noqa: F401
from . import core  # noqa: F401
from . import data  # noqa: F401
from . import models  # noqa: F401
from . import training  # noqa: F401
from . import utils  # noqa: F401

__all__ = list(_pertdec_all) + [
    "pertdec",
    "core",
    "data",
    "models",
    "training",
    "utils",
    "__version__",
]
