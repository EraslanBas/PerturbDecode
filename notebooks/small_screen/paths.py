"""Where this screen's data lives.

Nothing in this repository points at another project's directories. Every path
is either committed here, or written into ``SCREEN_DATA`` by the notebooks in
this folder.

``SCREEN_DATA`` defaults to ``<repo>/data/small_screen``. Set the environment
variable ``PERTURBDECODE_SMALL_DATA`` to put it somewhere else, or make
``<repo>/data/small_screen`` a symlink to the tree you already have.

The large screen is a separate root: notebooks 04 and 05 read its objects to
transfer cell-state labels and to build the combined training set. It resolves
the same way, through ``large_screen/paths.py``.
"""

import importlib.util
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", ".."))

SCREEN_DATA = os.environ.get("PERTURBDECODE_SMALL_DATA",
                             os.path.join(_REPO, "data", "small_screen"))

# The large screen's root and its committed reference tables, reused rather
# than duplicated: the module definitions are the same ones. Loaded by path
# because that file is also called paths.py, so a plain import finds this one.
_LARGE = os.path.join(_REPO, "notebooks", "large_screen", "paths.py")
_spec = importlib.util.spec_from_file_location("_large_screen_paths", _LARGE)
_large = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_large)

LARGE_SCREEN_DATA = _large.SCREEN_DATA
REFERENCE = _large.REFERENCE


def screen_path(*parts):
    """Join onto this screen's data root."""
    return os.path.join(SCREEN_DATA, *parts)


def large_screen_path(*parts):
    """Join onto the large screen's data root."""
    return os.path.join(LARGE_SCREEN_DATA, *parts)


def reference_path(*parts):
    """Join onto the committed reference tables, which both screens share."""
    return os.path.join(REFERENCE, *parts)
