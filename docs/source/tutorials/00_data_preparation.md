# Preparing your data

:::{admonition} Draft
:class: caution
The data contract below reflects the current code. Expand with worked examples
of converting common upstream formats.
:::

PerturbDecode operates on {class}`~anndata.AnnData` objects. This page
describes what each stage expects to find.

## The data contract

| Location | Field | Type | Required by |
|---|---|---|---|
| `.X` | expression matrix | `float32`, cells × genes | all stages |
| `.obs` | perturbation column | categorical | all stages |
| `.uns` | `"covariates"` | list of `.obs` column names | {class}`~perturbdecode.data.ScreenDataset` |
| `.var` | gene identifiers | index | effect sizes, modules |

## The perturbation column

Perturbation labels must be an **ordered categorical**, and the **first
category is the reference level**, normally your non-targeting controls.
Effect sizes and the model's embedding are both defined relative to it.

```python
import pandas as pd

categories = ["control", "KO_A", "KO_B"]   # control first
adata.obs["perturbation"] = pd.Categorical(
    adata.obs["perturbation"], categories=categories, ordered=True
)
```

:::{warning}
Getting the reference level wrong silently changes the meaning of every
downstream effect size. Check `adata.obs["perturbation"].cat.categories[0]`
before proceeding.
:::

## Covariates

`ScreenDataset` reads the covariate columns it should one-hot encode from
`.uns["covariates"]`:

```python
adata.uns["covariates"] = ["perturbation"]
```

The reference level is dropped from the one-hot encoding, so a screen with
*k* perturbation levels contributes *k − 1* covariate columns.

## Normalisation

<!-- TODO: state the expected normalisation. The ComBVAE reconstruction loss is
     MSE, which implies log-normalised (not raw count) input. Confirm against
     the E3Ligase preprocessing notebooks and document the exact recipe. -->

## Checking your object

```python
import perturbdecode as pd

assert adata.uns.get("covariates"), "set adata.uns['covariates']"
assert adata.obs["perturbation"].dtype.name == "category"
print("reference level:", adata.obs["perturbation"].cat.categories[0])
```

## Converting from common formats

<!-- TODO: short recipes for CellRanger output, a Seurat object via
     anndata2ri, and a plain counts matrix + metadata table. -->
