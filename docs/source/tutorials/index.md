# Tutorials

A complete walkthrough of a Perturb-seq screen analysis, one stage at a time.
Each tutorial is self-contained: it states what it takes as input, what it
produces, and which parameters matter — so you can start from the beginning or
jump to the stage you need.

:::{note}
Start with the {doc}`quickstart` if you want to see the whole pipeline end to
end on a small dataset before working through the individual stages.
:::

## Start here

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} {octicon}`zap;1.5em;sd-mr-1` Quickstart
:link: quickstart
:link-type: doc

The whole pipeline on a small public dataset, in one page.
:::

:::{grid-item-card} {octicon}`database;1.5em;sd-mr-1` Preparing your data
:link: 00_data_preparation
:link-type: doc

What PerturbDecode expects in `.X`, `.obs` and `.uns`.
:::

::::

## The pipeline, stage by stage

::::{grid} 1 2 3 3
:gutter: 3

:::{grid-item-card} 01 · Quality control
:link: 01_quality_control
:link-type: doc

Empty droplets, UMI and gene thresholds, mitochondrial fraction.
:::

:::{grid-item-card} 02 · Guide assignment
:link: 02_guide_assignment
:link-type: doc

Merging hashing and CRISPR libraries; assigning guides to cells.
:::

:::{grid-item-card} 03 · Guide QC
:link: 03_guide_qc
:link-type: doc

Depleted guides, control-guide selection, target filtering.
:::

:::{grid-item-card} 04 · Effect sizes
:link: 04_effect_sizes
:link-type: doc

Per-perturbation transcriptional effects and the beta matrix.
:::

:::{grid-item-card} 05 · Modules
:link: 05_modules
:link-type: doc

Grouping genes and knockouts into co-regulated programmes.
:::

:::{grid-item-card} 06 · ComBVAE
:link: 06_combvae
:link-type: doc

Training the conditional VAE; extracting perturbation embeddings.
:::

:::{grid-item-card} 07 · Prediction
:link: 07_prediction
:link-type: doc

Predicting and evaluating unseen perturbation combinations.
:::

:::{grid-item-card} 08 · Enrichment
:link: 08_enrichment
:link-type: doc

Protein complexes, transcription factors and pathway enrichment.
:::

::::

```{toctree}
:hidden:
:caption: Getting started

quickstart
00_data_preparation
```

```{toctree}
:hidden:
:caption: Pipeline stages

01_quality_control
02_guide_assignment
03_guide_qc
04_effect_sizes
05_modules
06_combvae
07_prediction
08_enrichment
```
