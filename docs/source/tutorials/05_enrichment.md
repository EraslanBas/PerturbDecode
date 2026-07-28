# 05 · Enrichment and interpretation

:::{admonition} Step 5 of 5: the pipeline walkthrough
:class: tip, dropdown
You are on **step 5**, *Enrichment and interpretation*. See the [full stage list](index.md), or start from the [quickstart](quickstart.md) for the whole pipeline on one page.
:::

:::{admonition} Draft
:class: caution
This page is a scaffold. Content to be written.
:::

Connect the modules and embeddings back to biology: protein complexes, transcription factors and pathways.

## What this stage does

<!-- TODO: 2-3 paragraphs of narrative. What biological/technical problem does
     this stage solve, and why is it done at this point in the pipeline? -->

## Inputs

- Gene/knockout modules from stage 05

## Outputs

- Enrichment tables and figures

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

## Next step

That is the end of the pipeline walkthrough. From here:

- Revisit the [concepts](../concepts/index.md) behind each stage
- Browse the [API reference](../api/index.md)

## Source material

<!-- Provenance: the analyses this stage is derived from. Remove once the page
     is written. -->

`E3LigasePerturbSeq` (R): `13_ProteinComplexAnalysis_*`, `14_TFEnrichmentAnalysis`, `15_AnalyseEffectsOnCytokines`
