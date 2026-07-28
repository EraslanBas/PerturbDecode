# 07 · Predicting combinations

:::{admonition} Draft
:class: caution
This page is a scaffold. Content to be written.
:::

Predict the transcriptional response to perturbation combinations that were not measured, and evaluate those predictions.

## What this stage does

<!-- TODO: 2-3 paragraphs of narrative. What biological/technical problem does
     this stage solve, and why is it done at this point in the pipeline? -->

## Inputs

- Trained ComBVAE model; held-out combination set

## Outputs

- Predicted expression profiles; evaluation metrics

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

<!-- TODO -->

## Source material

<!-- Provenance: the analyses this stage is derived from. Remove once the page
     is written. -->

`E3LigasePerturbSeq`: `11_01_PredictCombKO_BayesianLM_*`, `13_01_EvaluateCombKOPredR2`, `13_02_EvaluateCombKOPredOTDist`
