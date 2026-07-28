# PerturbDecode

An end-to-end toolkit for analysing large-scale single-cell perturbation
screens: from guide-level quality control, through perturbation effect-size
estimation, to generative modelling of perturbation responses with ComBVAE.

- **Distribution name:** `PerturbDecode`
- **Import name:** `perturbdecode`

## Installation

```bash
pip install PerturbDecode            # core
pip install 'PerturbDecode[r]'       # + optional R integration (rpy2, anndata2ri)
pip install 'PerturbDecode[dev]'     # + pytest, ruff
pip install 'PerturbDecode[docs]'    # + sphinx
```

The core install has **no R dependency**. Steps that call into R raise a clear
error telling you to install the `[r]` extra.

### Development install

```bash
git clone https://github.com/EraslanBas/PerturbDecode.git
cd PerturbDecode
pip install -e '.[dev]'
```

## Quickstart

```python
import perturbdecode as pd

# 1. Split a screen into training and validation sets
pd.createTrainValData(
    adata,
    perturbationColumn="perturbation",
    pertCategories=["control", "KO_A", "KO_B"],
    dataDir="out/",
)

# 2. Train the conditional VAE
pd.runTrainingComBVAE(model_dir="out/models", ...)

# 3. Extract the learned perturbation embeddings
emb = pd.extract_model_embeddings(model_dir="out/models", ...)

# 4. Visualise them
pd.visualizePerturbationEmbeddings(emb, perturbationsList)
```

From the command line:

```bash
perturbdecode --version
perturbdecode list-steps
```

## Pipeline steps

| Step | Purpose |
|---|---|
| `createTrainValData` | Split a screen into training/validation sets |
| `selectWorkingGuides` | Select conditionally dependent guides targeting the same gene |
| `inferEffectSizes` | Per-perturbation effect sizes via regression |
| `runTrainingComBVAE` | Train the conditional VAE (`CVAE_basic` or `CVAE_Gumbel`) |
| `extract_model_embeddings` | Pull perturbation embeddings out of a fitted model |
| `visualizePerturbationEmbeddings` | Cluster and plot the embeddings |

## Models

- **`CVAE_basic`** — conditional VAE; perturbation covariates pass through a
  linear embedding and are concatenated into both encoder and decoder.
  Loss: `(MSE + α·KL) / batch_size`.
- **`CVAE_Gumbel`** — as above, with a Gumbel-sigmoid relaxation masking the
  perturbation embedding (temperature `tau`).

## Testing

```bash
pytest                       # full suite
pytest --cov=perturbdecode   # with coverage
```

R-dependent tests skip automatically when the `[r]` extra is not installed.

## Documentation

```bash
pip install '.[docs]'
python -m sphinx -b html docs/source docs/_build/html
```

Then open `docs/_build/html/index.html`.

## License

MIT
