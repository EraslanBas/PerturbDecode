"""Paths for the revision analyses.

`projectDir` is this folder, not the screen's data root: notebooks 01 and 03
`os.chdir` into it so that what they write lands in `outputs/` here. The screen
data itself is reached with `screen_path`, and the committed tables with
`reference_path` and `textfiles_path`.
"""
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from paths import (  # noqa: F401,E402
    SCREEN_DATA,
    REFERENCE,
    TEXTFILES,
    screen_path,
    reference_path,
    textfiles_path,
)

projectDir = _os.path.dirname(_os.path.abspath(__file__))

# The combined knockout object, written by build_anndata/18_BuildCombinedKOObject.
# It sits under OriginalFiles/, not outputs/anndata/ as the notebooks assumed.
ANNDATA_ALL_KO = screen_path("outputs", "anndata", "OriginalFiles",
                             "adata-hash-features_ALLKO_ForSCVI_09072021.h5ad")
