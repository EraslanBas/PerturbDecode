# 05 · Effect sizes

:::{admonition} Step 5 of 8: the pipeline walkthrough
:class: tip, dropdown
You are on **step 5**, *Effect sizes*. See the [full stage list](index.md), or start from the [quickstart](quickstart.md) for the whole pipeline on one page.
:::

:::{admonition} Draft
:class: caution
This page is a scaffold. Content to be written.
:::

Estimate the transcriptional effect of each perturbation relative to controls, producing the beta matrix that downstream stages consume.

## The problem this step addresses

<!-- TODO: write this section. Points to cover:
     - Why computation becomes the limiting factor at screen scale, and how estimation is batched.
     - How multiplicity is handled across the full perturbation-by-gene matrix.
-->

## What this stage does

<!-- TODO: 2-3 paragraphs of narrative. What biological/technical problem does
     this stage solve, and why is it done at this point in the pipeline? -->

## Inputs

- QC-passed `AnnData` with perturbation labels

## Outputs

- Beta matrix (perturbations x genes) with significance statistics

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

{func}`~perturbdecode.inferEffectSizes`

## Next step

::::{grid} 1
:::{grid-item-card} 06 · Gene and knockout modules
:link: 06_modules
:link-type: doc

Continue the walkthrough.
:::
::::

## Source material

<!-- Provenance: the analyses this stage is derived from. Remove once the page
     is written. -->

`E3LigasePerturbSeq`: `08-00-MixedEffectLinearRegressionModel*.ipynb`, R `04_ProcessMixedEfLMPValues`
