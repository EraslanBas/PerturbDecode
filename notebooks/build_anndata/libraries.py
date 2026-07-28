import scanpy as sc
import os as os

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


# R integration
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import pandas2ri, numpy2ri
from rpy2.robjects.vectors import StrVector, FloatVector, ListVector
from rpy2.robjects import r
import rpy2.robjects as ro
import anndata2ri # scipy.sparse + AnnData support



numpy2ri.activate()
pandas2ri.activate()
anndata2ri.activate()

from pathlib import Path
import math
from tqdm.auto import tqdm
import warnings
import shelve
import pickle
from urllib.request import urlopen
import itertools as itrT

sc.set_figure_params(dpi=100, fontsize=12)
matplotlib.rcParams['font.sans-serif'] = matplotlib.rcParamsDefault['font.sans-serif']

sc.settings.verbosity = 'hint'

