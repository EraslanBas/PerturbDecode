"""Configuration file for the Sphinx documentation builder.

https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import os
import sys

# Make the package importable for autodoc without installing it first.
sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------

project = "PerturbDecode"
copyright = "2025, Basak Eraslan"
author = "Basak Eraslan"

try:  # keep the docs version in lockstep with the package
    from perturbdecode import __version__ as release
except Exception:  # pragma: no cover - docs can build without the deps
    release = "0.1.0"
version = release

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # NumPy/Google-style docstrings
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
# Jupyter leaves stale copies of .rst files behind; they would otherwise be
# built as duplicate (and outdated) pages.
exclude_patterns = [
    ".ipynb_checkpoints",
    "**/.ipynb_checkpoints",
    "**/.ipynb_checkpoints/**",
]

# Autodoc should not fail the build when heavy/optional deps are unavailable.
autodoc_mock_imports = ["rpy2", "anndata2ri", "torch", "scanpy", "pingouin"]
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
napoleon_numpy_docstring = True
napoleon_google_docstring = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "anndata": ("https://anndata.readthedocs.io/en/stable/", None),
}

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
