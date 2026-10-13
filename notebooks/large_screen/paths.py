"""Where this screen's data lives.

Nothing in this repository points at another project's directories. Every path
below is either committed here, or written into ``SCREEN_DATA`` by the
notebooks in ``build_anndata/``.

``SCREEN_DATA`` defaults to ``<repo>/data/large_screen``. Set the environment
variable ``PERTURBDECODE_DATA`` to put it somewhere else, or make
``<repo>/data/large_screen`` a symlink to the tree you already have::

    export PERTURBDECODE_DATA=/mnt/somewhere/large_screen
"""

import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", ".."))

SCREEN_DATA = os.environ.get("PERTURBDECODE_DATA",
                             os.path.join(_REPO, "data", "large_screen"))

# Committed reference tables, small enough to live in the repository.
REFERENCE = os.path.join(_HERE, "reference")

# Reference tables that build_anndata both reads and writes.
TEXTFILES = os.path.join(_HERE, "build_anndata", "TextFiles")


def screen_path(*parts):
    """Join onto the screen's data root."""
    return os.path.join(SCREEN_DATA, *parts)


def reference_path(*parts):
    """Join onto the committed reference tables."""
    return os.path.join(REFERENCE, *parts)


def textfiles_path(*parts):
    """Join onto build_anndata's committed reference tables."""
    return os.path.join(TEXTFILES, *parts)
