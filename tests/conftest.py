"""Shared pytest fixtures.

Provides a small synthetic perturbation screen so that every test runs in
seconds and needs no access to real screen data.
"""

import numpy as np
import pandas as pd
import pytest


N_CELLS = 120
N_GENES = 40
PERT_CATEGORIES = ["control", "KO_A", "KO_B"]


@pytest.fixture(scope="session")
def rng():
    """Deterministic random number generator."""
    return np.random.default_rng(0)


@pytest.fixture
def screen_adata(rng):
    """A tiny synthetic screen: 120 cells x 40 genes, 3 perturbation levels."""
    import anndata as ad

    X = rng.poisson(5.0, size=(N_CELLS, N_GENES)).astype("float32")
    obs = pd.DataFrame(
        {
            "perturbation": np.tile(PERT_CATEGORIES, N_CELLS // len(PERT_CATEGORIES)),
            "batch": rng.choice(["b1", "b2"], size=N_CELLS),
        },
        index=[f"cell{i}" for i in range(N_CELLS)],
    )
    var = pd.DataFrame(index=[f"gene{j}" for j in range(N_GENES)])
    adata = ad.AnnData(X=X, obs=obs, var=var)
    adata.uns["covariates"] = ["perturbation"]
    return adata


@pytest.fixture
def screen_h5ad(tmp_path, screen_adata):
    """The synthetic screen written to a temporary .h5ad file."""
    path = tmp_path / "screen.h5ad"
    screen_adata.write_h5ad(path)
    return str(path)
