"""Sphinx configuration for the PerturbDecode documentation site.

https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import os
import sys
from datetime import datetime

# Make the package importable for autodoc without installing it first.
sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------

project = "PerturbDecode"
author = "Basak Eraslan"
copyright = f"{datetime.now():%Y}, {author}"

try:  # keep the docs version in lockstep with the package
    from perturbdecode import __version__ as release
except Exception:  # pragma: no cover - docs can build without the deps
    release = "0.1.0"
version = release

# -- General configuration ---------------------------------------------------

extensions = [
    # API documentation
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",  # NumPy/Google-style docstrings
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    # Authoring
    "myst_nb",  # Markdown + executable/rendered notebooks
    "sphinx_copybutton",  # copy button on code blocks
    "sphinx_design",  # grids, cards, tabs
]

templates_path = ["_templates"]
exclude_patterns = [
    ".ipynb_checkpoints",
    "**/.ipynb_checkpoints",
    "**/.ipynb_checkpoints/**",
    "**.ipynb_checkpoints",
    "_build",
    "Thumbs.db",
    ".DS_Store",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "myst-nb",
    ".ipynb": "myst-nb",
}

# -- MyST / notebook handling ------------------------------------------------

myst_enable_extensions = [
    "colon_fence",  # ::: fenced directives
    "deflist",
    "dollarmath",  # $inline$ and $$block$$ maths
    "linkify",
    "substitution",
    "tasklist",
]
myst_heading_anchors = 3

# Notebooks are committed with their outputs and rendered as-is. Building the
# docs must never require the 700 GB of screen data the tutorials describe.
nb_execution_mode = "off"
nb_merge_streams = True

# -- Autodoc -----------------------------------------------------------------

autosummary_generate = True
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
# Heavy/optional dependencies are mocked so the docs build anywhere.
autodoc_mock_imports = ["rpy2", "anndata2ri", "torch", "scanpy", "pingouin"]

napoleon_numpy_docstring = True
napoleon_google_docstring = True
napoleon_use_rtype = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "sklearn": ("https://scikit-learn.org/stable/", None),
    "anndata": ("https://anndata.readthedocs.io/en/stable/", None),
    "scanpy": ("https://scanpy.readthedocs.io/en/stable/", None),
    "torch": ("https://pytorch.org/docs/stable/", None),
}

# -- HTML output -------------------------------------------------------------

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = f"{project} {version}"
html_show_sourcelink = False

html_theme_options = {
    "github_url": "https://github.com/EraslanBas/PerturbDecode",
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "navbar_align": "left",
    "show_toc_level": 2,
    "show_nav_level": 1,
    "header_links_before_dropdown": 5,
    "icon_links": [
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/PerturbDecode/",
            "icon": "fa-solid fa-box",
        },
    ],
    "footer_start": ["copyright"],
    "footer_end": ["sphinx-version"],
}

html_context = {
    "github_user": "EraslanBas",
    "github_repo": "PerturbDecode",
    "github_version": "main",
    "doc_path": "docs/source",
    "default_mode": "auto",
}

# Sidebars: the landing page gets none, everything else gets the section nav.
html_sidebars = {
    "index": [],
    "installation": [],
}
