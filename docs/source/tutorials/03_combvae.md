# 03 · ComBVAE

:::{admonition} Step 3 of 8: the pipeline walkthrough
:class: tip, dropdown
You are on **step 3**, *ComBVAE*. See the [full stage list](index.md), or start from the [quickstart](quickstart.md) for the whole pipeline on one page.
:::

:::{admonition} Draft
:class: caution
This page is a scaffold. Content to be written.
:::

Train the conditional variational autoencoder and extract a continuous embedding of perturbation responses.

## The problem this step addresses

<!-- TODO: write this section. Points to cover:
     - Why single-gene perturbation effects are hard to detect: signal is sparse and subtle.
     - Why the whole perturbation space is modelled jointly rather than one perturbation at a time.
     - What the beta weighting buys: disentangled program embeddings, and why that makes small shifts detectable.
     - Why measuring shifts at the embedding level beats measuring them per gene, given correlation structure across genes (the unequal-pathway-size problem).
     - Why a non-linear model is needed at all.
-->

## What this stage does

<!-- TODO: 2-3 paragraphs of narrative. What biological/technical problem does
     this stage solve, and why is it done at this point in the pipeline? -->

## Inputs

- QC-passed `AnnData` with perturbation categories

## Outputs

- Trained model checkpoint; perturbation embedding matrix

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

{func}`~perturbdecode.createTrainValData`, {func}`~perturbdecode.runTrainingComBVAE`, {func}`~perturbdecode.extract_model_embeddings`, {func}`~perturbdecode.visualizePerturbationEmbeddings`

## Next step

::::{grid} 1
:::{grid-item-card} 04 · Guide selection
:link: 04_guide_selection
:link-type: doc

Continue the walkthrough.
:::
::::

## Source material

<!-- Provenance: the analyses this stage is derived from. Remove once the page
     is written. -->

`E3LigasePerturbSeq`: `06_RunCVAE.ipynb`, `08_GenerateCells.ipynb`, `11_VisualizeEmbeddings.ipynb`
