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

A PROBABILISTIC FRAMEWORK FOR LARGE SINGLE CELL PERTURBATION SCREENS
:::
::::

---

Pooled CRISPR screens read out by single-cell sequencing promise a causal map of
gene function. Getting there means confronting a specific set of problems, most
of which are usually handled with disconnected heuristics applied after the fact.

PerturbDecode approaches them with a single generative model, **ComBVAE**, used
first to decide *which measurements are real* and then to *predict measurements
that were never made*.

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} {octicon}`rocket;1.5em;sd-mr-1` Getting started
:link: installation
:link-type: doc

Install the package and run your first analysis.
:::

:::{grid-item-card} {octicon}`book;1.5em;sd-mr-1` Walkthrough
:link: tutorials/index
:link-type: doc

A complete Perturb-seq analysis, one stage at a time, on real screen data.
:::

:::{grid-item-card} {octicon}`beaker;1.5em;sd-mr-1` Concepts
:link: concepts/index
:link-type: doc

The models and statistics behind each stage.
:::

:::{grid-item-card} {octicon}`code;1.5em;sd-mr-1` API reference
:link: api/index
:link-type: doc

Every public function and class.
:::

::::

## The pipeline

Stages 01 onwards are importable functions operating on
{class}`~anndata.AnnData`, so you can enter the pipeline at any point. Stage 00
comes before the package: it assembles the object everything else starts from,
and is provided as example notebooks to adapt rather than as API.

| | Stage | Status | What it produces |
|---|---|---|---|
| 00 | [Generating the AnnData object](tutorials/00_data_preparation.md) | {bdg-info}`Example notebooks` | The assembled screen: called cells with their channel, sample and guide annotation |
| 01 | [Quality control](tutorials/01_quality_control.md) | {bdg-warning}`Partial` | A filtered object of properly perturbed cells, with working guides pooled to their target genes |
| 02 | [Effect sizes](tutorials/02_effect_sizes.md) | {bdg-warning}`Partial` | Coefficient and FDR matrices, the beta matrix |
| 03 | [Modules](tutorials/03_modules.md) | {bdg-secondary}`Planned` | Gene programmes and perturbation groups |
| 04 | [Combination prediction](tutorials/04_prediction.md) | {bdg-secondary}`Planned` | Predicted responses to unmeasured combinations |
| 05 | [Enrichment](tutorials/05_enrichment.md) | {bdg-secondary}`Planned` | Complexes, transcription factors, pathways |

:::{note}
PerturbDecode is under active development, and each stage above carries its
current state. Stages marked *v1 notebooks* were performed for the manuscript
using [PerturbDecode_v1](https://github.com/EraslanBas/PerturbDecode_v1) and are
documented here as a methods record rather than as package API.
:::

## Installation

```bash
pip install PerturbDecode
```

See {doc}`installation` for the optional R integration and development setup.

## Example data

The walkthrough uses the genome-scale Perturb-seq screen of E3 ligases in
primary mouse dendritic cells from
[Geiger-Schuller, Eraslan et al., bioRxiv 2023](https://doi.org/10.1101/2023.01.23.525198),
available from
[GEO GSE327057](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE327057).

## Citation

If you use PerturbDecode in your research, please cite the accompanying
manuscript. See {doc}`about/citation`. The analysis code used for the manuscript
is archived at
[PerturbDecode_v1](https://github.com/EraslanBas/PerturbDecode_v1); it predates
this package and does not reflect the current API.

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
