# Tutorials

A complete walkthrough of a Perturb-seq screen analysis, one stage at a time.
Each tutorial is self-contained: it states what it takes as input, what it
produces, and which parameters matter, so you can start from the beginning or
jump to the stage you need.

:::{note}
Start with the {doc}`quickstart` if you want to see the whole pipeline end to
end on a small dataset before working through the individual stages.
:::

## Start here

::::{grid} 1
:gutter: 3

:::{grid-item-card} {octicon}`zap;1.5em;sd-mr-1` Quickstart
:link: quickstart
:link-type: doc

The whole pipeline on a small public dataset, in one page.
:::

::::

## The pipeline, stage by stage

::::{grid} 1 2 3 3
:gutter: 3

:::{grid-item-card} 00 · Generating the AnnData object
:link: 00_data_preparation
:link-type: doc

Assembling the screen from per-channel output. Precedes the package.
:::

:::{grid-item-card} 01 · Quality control
:link: 01_quality_control
:link-type: doc

Cell states, guide-level ComBVAE, guide and cell filtering.
:::

:::{grid-item-card} 02 · Effect sizes
:link: 02_effect_sizes
:link-type: doc

Per-perturbation transcriptional effects and the beta matrix.
:::

:::{grid-item-card} 03 · Modules
:link: 03_modules
:link-type: doc

Grouping genes and perturbations into co-regulated programmes.
:::

:::{grid-item-card} 04 · Combination prediction
:link: 04_prediction
:link-type: doc

Predicting and evaluating unmeasured perturbation combinations.
:::

:::{grid-item-card} 05 · Enrichment
:link: 05_enrichment
:link-type: doc

Protein complexes, transcription factors and pathway enrichment.
:::

::::

```{toctree}
:hidden:
:caption: Getting started

quickstart
```

```{toctree}
:hidden:
:caption: Pipeline stages

00_data_preparation
01_quality_control
02_effect_sizes
03_modules
04_prediction
05_enrichment
```
