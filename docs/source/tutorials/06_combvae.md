# 06 · ComBVAE

:::{admonition} Step 6 of 8 — the pipeline walkthrough
:class: tip, dropdown
You are on **step 6**, *ComBVAE*. See the [full stage list](index.md), or start from the [quickstart](quickstart.md) for the whole pipeline on one page.
:::

:::{admonition} Draft
:class: caution
This page is a scaffold. Content to be written.
:::

Train the conditional variational autoencoder and extract a continuous embedding of perturbation responses.

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
:::{grid-item-card} 07 · Predicting combinations
:link: 07_prediction
:link-type: doc

Continue the walkthrough.
:::
::::

## Source material

<!-- Provenance: the analyses this stage is derived from. Remove once the page
     is written. -->

`E3LigasePerturbSeq`: `06_RunCVAE.ipynb`, `08_GenerateCells.ipynb`, `11_VisualizeEmbeddings.ipynb`
