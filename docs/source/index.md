---
sd_hide_title: true
---

# PerturbDecode

::::{grid} 1
:::{grid-item}
:class: sd-text-center sd-fs-1 sd-font-weight-bold

PerturbDecode
:::
:::{grid-item}
:class: sd-text-center sd-fs-5 sd-text-secondary

An end-to-end toolkit for analysing large-scale single-cell perturbation screens
:::
::::

---

PerturbDecode takes a Perturb-seq experiment from raw count matrices through to
interpretable biology: guide assignment and quality control, per-perturbation
effect sizes, gene and knockout modules, and a conditional variational
autoencoder (**ComBVAE**) that learns a continuous embedding of perturbation
responses and predicts unseen combinations.

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} {octicon}`rocket;1.5em;sd-mr-1` Getting started
:link: installation
:link-type: doc

Install the package and run your first analysis in a few minutes.
:::

:::{grid-item-card} {octicon}`book;1.5em;sd-mr-1` Tutorials
:link: tutorials/index
:link-type: doc

A step-by-step walkthrough of a complete Perturb-seq screen analysis.
:::

:::{grid-item-card} {octicon}`beaker;1.5em;sd-mr-1` Concepts
:link: concepts/index
:link-type: doc

The models and statistics behind each step, and how to interpret them.
:::

:::{grid-item-card} {octicon}`code;1.5em;sd-mr-1` API reference
:link: api/index
:link-type: doc

Every public function and class, with parameters and return values.
:::

::::

## The pipeline

Each stage is an independent, importable function that takes and returns an
{class}`~anndata.AnnData` object, so you can enter the pipeline at any point.

| Stage | What it does | Tutorial |
|---|---|---|
| Quality control | Filter cells and genes; remove empty droplets and low-quality cells | [01](tutorials/01_quality_control.md) |
| Guide assignment | Merge hashing and CRISPR libraries; assign guides to cells | [02](tutorials/02_guide_assignment.md) |
| Guide QC | Identify depleted guides, select control guides, filter targets | [03](tutorials/03_guide_qc.md) |
| Effect sizes | Estimate per-perturbation transcriptional effects | [04](tutorials/04_effect_sizes.md) |
| Modules | Group genes and knockouts into co-regulated programmes | [05](tutorials/05_modules.md) |
| ComBVAE | Train a conditional VAE; extract perturbation embeddings | [06](tutorials/06_combvae.md) |
| Prediction | Predict and evaluate unseen perturbation combinations | [07](tutorials/07_prediction.md) |
| Enrichment | Protein complexes, transcription factors, pathway enrichment | [08](tutorials/08_enrichment.md) |

## Installation

```bash
pip install PerturbDecode
```

See {doc}`installation` for the optional R integration and development setup.

## Quick example

```python
import perturbdecode as pd

pd.createTrainValData(
    adata,
    perturbationColumn="perturbation",
    pertCategories=["control", "KO_A", "KO_B"],
    dataDir="out/",
)
pd.runTrainingComBVAE(model_dir="out/models", ...)
embeddings = pd.extract_model_embeddings(model_dir="out/models", ...)
```

## Citation

If you use PerturbDecode in your research, please cite the accompanying
manuscript. See {doc}`about/citation` for the full reference.

```{toctree}
:hidden:
:maxdepth: 2

installation
tutorials/index
concepts/index
api/index
```

```{toctree}
:hidden:
:caption: Development

contributing
changelog
about/citation
```
