# Revision analyses

Work done for the manuscript revision, after the figures in
`../manuscript_figures/` were made. Two strands: how the knockout modules
interact with the DC subtypes, and two robustness checks.

Ported from `RevisionAnalyses/` in the E3 ligase analysis tree.

## The notebooks

| # | Notebook | Kernel | Produces |
|---|---|---|---|
| 01 | `01_ComputeInteractionsWithDCSubtypes` | Python | `outputs/KOModule_leidenInteractions.csv` |
| 02 | `02_InspectInteractionresults` | R | `figures/Fig2E.pdf`, `figures/Fig2E_supplement.pdf` |
| 03 | `03_ComputeKOModuleEffects` | Python | `outputs/KOModuleEffects.csv` |
| 04 | `04_AnalyseModulEffectExplanability` | R | `outputs/ModuleGenesExplained.csv`, `figures/FigS3N.pdf` |
| 05 | `05_InspectKOGenesIngenePrograms` | R | plots only |
| 06 | `06_CompareComboResultsWithBigScreen` | R | plots only |
| 07 | `07-GenerateGeneAndKOModules_withoutRack1Socs3Rnf128` | Python | `outputs/ConnectivitiesOriginal.csv`, `outputs/ConnectivitiesUpdated.csv`, `outputs/NumberOfOverlappingNeighbours.csv` |

01 and 03 fit the models; 02, 04 and 05 read what they wrote. 06 compares the
combinatorial screen's coefficients against this screen's, and 07 rebuilds the
gene and guide modules with Rack1, Socs3 and Rnf128 dropped, to see how much
the module structure depends on them.

## What runs from a clone

Five of the seven: **02, 04, 05, 06 and 07**. Everything they read is in the
repository — the module tables and `SignificantCoefMatrix.csv` from
`../reference/`, the effect-size matrices as the committed `.csv.gz` in
`../build_anndata/TextFiles/`, and the two intermediates in `TextFiles/` here.

**01 and 03 need the 6 GB knockout object** `adata-hash-features_ALLKO_ForSCVI_09072021.h5ad`
under the screen's data root, so they are the two that need the data. Their
results are committed in `TextFiles/` precisely so the rest does not.

## Notes on the port

**The config was dead.** The original `Conf.R` pointed `dataDir` and `davidDir`
at `/home/beraslan/jovian-work`, a machine that no longer exists. Nothing read
them, and they are gone; everything now resolves through `../paths.R`.

**One path was wrong.** 01 and 03 read the knockout object from
`outputs/anndata/`, where it is not — it sits in `outputs/anndata/OriginalFiles/`.
Corrected in `Conf.R` and `parameters.py`.

**One cell could never have run.** `02` had `coef_norm_geneModulesTmp2[-1:6, ]`,
which is the sequence -1, 0, 1 … 6 and mixes signs, so R refuses it. That is
where the original stopped, at 15 of 17 cells. It is a peek at the data and
nothing depends on it, so it is now `head(..., 6)` and the notebook completes.

**Not ported.** `RevisionAnalyses/TextFiles/` also holds `GuideSelect_pvals.csv`
and `GuideSelect_weights.csv`, about 400 MB each, which no notebook in that
folder reads.
