# 03 · Guide quality control

:::{admonition} Step 3 of 8 — the pipeline walkthrough
:class: tip, dropdown
You are on **step 3**, *Guide quality control*. See the [full stage list](index.md), or start from the [quickstart](quickstart.md) for the whole pipeline on one page.
:::

:::{admonition} Draft
:class: caution
This page is a scaffold. Content to be written.
:::

Identify guides that are depleted or non-functional, choose a trustworthy set of control guides, and filter the targets carried forward.

## What this stage does

<!-- TODO: 2-3 paragraphs of narrative. What biological/technical problem does
     this stage solve, and why is it done at this point in the pipeline? -->

## Inputs

- `AnnData` with assigned guides

## Outputs

- Filtered `AnnData`; per-guide QC statistics

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

{func}`~perturbdecode.selectWorkingGuides`

## Next step

::::{grid} 1
:::{grid-item-card} 04 · Effect sizes
:link: 04_effect_sizes
:link-type: doc

Continue the walkthrough.
:::
::::

## Source material

<!-- Provenance: the analyses this stage is derived from. Remove once the page
     is written. -->

`E3LigasePerturbSeq`: `07_01`-`07_04`, `08_RunEM`, `08_SelectCellsAfterEM`
