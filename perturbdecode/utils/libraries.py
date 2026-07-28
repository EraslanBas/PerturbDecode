import scanpy as sc
import os as os
import gc


# Plotting
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# numpy et al.
import numpy as np
import scipy.sparse as sp
import scipy
import pandas as pd


# R integration (optional: install with the ``[r]`` extra).
# Steps that call into R raise a clear error if these are missing, but the rest
# of the package imports and runs without an R installation.
try:
    from rpy2.robjects.packages import importr
    from rpy2.robjects.conversion import localconverter
    from rpy2.robjects import pandas2ri, numpy2ri
    from rpy2.robjects.vectors import StrVector, FloatVector, ListVector
    from rpy2.robjects import r
    import rpy2.robjects as ro
    import anndata2ri  # scipy.sparse + AnnData support

    numpy2ri.activate()
    pandas2ri.activate()
    anndata2ri.activate()

    HAS_R = True
except ImportError:  # pragma: no cover - depends on the environment
    HAS_R = False
    importr = localconverter = pandas2ri = numpy2ri = None
    StrVector = FloatVector = ListVector = None
    r = ro = anndata2ri = None


def require_r():
    """Raise a helpful error if the optional R dependencies are unavailable.

    Raises
    ------
    ImportError
        If ``rpy2`` and ``anndata2ri`` are not installed.
    """
    if not HAS_R:
        raise ImportError(
            "This step requires the optional R dependencies. "
            "Install them with:  pip install 'PerturbDecode[r]'"
        )

from pathlib import Path
import math
from tqdm.auto import tqdm
import warnings
import shelve
import pickle
from urllib.request import urlopen
import itertools as itrT
import random 

sc.set_figure_params(dpi=100, fontsize=12)
matplotlib.rcParams['font.sans-serif'] = matplotlib.rcParamsDefault['font.sans-serif']

sc.settings.verbosity = 'hint'


import torch
from torch.utils.data import Dataset, DataLoader

import bisect
from itertools import accumulate
import argparse

import sys
import os

import torch.nn as nn

import torch
from torch import optim

