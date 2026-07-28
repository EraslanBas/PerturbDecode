# Quickstart

:::{admonition} Draft
:class: caution
The narrative is in place; the worked example needs to be run against the
public tutorial dataset once one is chosen.
:::

This page runs the whole pipeline end to end on a small dataset, so you can see
how the stages fit together before working through them individually.

## Install

```bash
pip install PerturbDecode
```

## A minimal synthetic screen

Everything below runs on synthetic data, so it works immediately after
installation with no downloads.

```python
import numpy as np
import pandas as pd
import anndata as ad

rng = np.random.default_rng(0)

n_cells, n_genes = 300, 100
categories = ["control", "KO_A", "KO_B"]

adata = ad.AnnData(
    X=rng.poisson(5.0, size=(n_cells, n_genes)).astype("float32"),
    obs=pd.DataFrame(
        {"perturbation": rng.choice(categories, n_cells)},
        index=[f"cell{i}" for i in range(n_cells)],
    ),
    var=pd.DataFrame(index=[f"gene{j}" for j in range(n_genes)]),
)
adata.uns["covariates"] = ["perturbation"]
adata
```

## Split into training and validation sets

```python
import perturbdecode as pd

pd.createTrainValData(
    adata,
    perturbationColumn="perturbation",
    pertCategories=categories,
    dataDir="out/",
    valSetPercent=0.2,
)
```

## Train ComBVAE

```python
pd.runTrainingComBVAE(model_dir="out/models", ...)
```

## Extract and visualise perturbation embeddings

```python
embeddings = pd.extract_model_embeddings(model_dir="out/models", ...)
pd.visualizePerturbationEmbeddings(embeddings, perturbationsList=categories)
```

## Where to go next

- {doc}`00_data_preparation`: what PerturbDecode expects of your `AnnData`
- {doc}`01_quality_control`: start of the full pipeline
- {doc}`../concepts/combvae`: how the model works

<!-- TODO: replace the synthetic example above with a real public Perturb-seq
     dataset (candidates: Norman 2019, a Replogle subset) so that readers see
     realistic outputs and figures. The dataset must be small enough to
     download and run in a few minutes. -->
