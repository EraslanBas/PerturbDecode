# Notebooks

Two different kinds of thing live here, and they are kept apart because they
answer different questions.

```
notebooks/
  E3LigaseAnalysisScripts/   what was done to one dataset
    large_screen/            the 1,130-gene E3 ligase screen
    small_screen/            the combinatorial screen
  PerturbDecodePackageUsage/ how to use PerturbDecode on your own data
```

## `E3LigaseAnalysisScripts/`

The analysis of the E3 ligase Perturb-seq screens of Geiger-Schuller, Eraslan
et al., [doi:10.1101/2023.01.23.525198](https://doi.org/10.1101/2023.01.23.525198):
raw reads to published figure, plus the revision analyses and the factorisation
behind them.

These are a **record of what was done**, not a tutorial. They are specific to
that experiment — its guide library, its hashing design, its module
definitions, its thresholds — and they do not import `perturbdecode`. Several
predate the package. Read them to see how a real screen was taken apart, or to
reproduce a published number; do not read them as the recommended way to use
the package.

Each folder's README says what its notebooks produce, which of them run from a
clone and which need data, and what was found broken when they were ported.

## `PerturbDecodePackageUsage/`

Notebooks that demonstrate `perturbdecode` itself: the pipeline steps, on data
small enough to ship or synthesise, with the API as it is now rather than as it
was in 2023.

The prose tutorials in `docs/source/tutorials/` cover the same ground for the
published documentation site; these are the executable counterpart.

## Which one you want

| You want to | Look in |
|---|---|
| use PerturbDecode on your own screen | `PerturbDecodePackageUsage/`, or the docs tutorials |
| reproduce a figure from the paper | `E3LigaseAnalysisScripts/large_screen/manuscript_figures/` |
| see how the screen object was built | `E3LigaseAnalysisScripts/large_screen/build_anndata/` |
| understand a specific published number | the folder README that names it |
