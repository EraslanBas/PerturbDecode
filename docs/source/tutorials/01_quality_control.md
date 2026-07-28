# 01 · Quality control

:::{admonition} Step 1 of 8: the pipeline walkthrough
:class: tip, dropdown
You are on **step 1**, *Quality control*. See the [full stage list](index.md), or start from the [quickstart](quickstart.md) for the whole pipeline on one page.
:::

:::{admonition} Draft
:class: caution
This page is a scaffold. Content to be written.
:::

Filter empty droplets and low-quality cells, and set gene-level thresholds, before any perturbation-specific analysis.

## What this stage does

<!-- TODO: 2-3 paragraphs of narrative. What biological/technical problem does
     this stage solve, and why is it done at this point in the pipeline? -->

## Inputs

- Raw count matrix (`AnnData`) with cells x genes

## Outputs

- Filtered `AnnData` with QC metrics in `.obs`

## Walkthrough

<!-- TODO: executable example. Keep it runnable on the public tutorial dataset
     so the page can be executed end to end by a reader. -->

```python
import perturbdecode as pd

# ...
```

## Parameters that matter

<!-- TODO: table of the key parameters, sensible defaults, and how to choose
     them for a new screen. This is where hard-won judgement belongs. -->

| Parameter | Default | How to choose it |
|---|---|---|
| | | |

## Diagnostics

<!-- TODO: what to plot / check before moving on, and what a healthy result
     looks like versus a warning sign. -->

## Common problems

<!-- TODO: failure modes and what they indicate. -->

## API

<!-- TODO: {func}`~perturbdecode...` once the stage is implemented -->

## Next step

::::{grid} 1
:::{grid-item-card} 02 · Guide assignment
:link: 02_guide_assignment
:link-type: doc

Continue the walkthrough.
:::
::::

## Source material

<!-- Provenance: the analyses this stage is derived from. Remove once the page
     is written. -->

`E3LigasePerturbSeq`: `01-upstream-qc.ipynb`, `02-downstream-qc.ipynb`
