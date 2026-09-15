# The full pipeline, raw reads to figure inputs

Nineteen notebooks take raw CellRanger output to the objects the combinatorial
models and the manuscript figures read. They run in order, each reading what
the previous ones wrote.

Paths, thresholds and output names are all in `parameters.py`. Edit that file
first: every value in it describes the E3 ligase screen and will not match your
experiment.

## The five stages

```
  raw CellRanger output
        │
  ┌─────▼──────────────────────────────────────────────┐
  │ A. Assemble the object                    01 - 04  │
  │    cell calling, QC, hashing, guide calls          │
  └─────┬──────────────────────────────────────────────┘
        │  par_save_filename_1
  ┌─────▼──────────────────────────────────────────────┐
  │ B. Embed and cluster                           05  │
  │    normalise, HVG, PCA, UMAP, leiden, cell cycle   │
  └─────┬──────────────────────────────────────────────┘
        │  anndataFileName2   ← the screen object
  ┌─────▼──────────────────────────────────────────────┐
  │ C. Guide quality control                  06 - 12  │
  │    which guides worked                             │
  └─────┬──────────────────────────────────────────────┘
        │  bad-guide lists
  ┌─────▼──────────────────────────────────────────────┐
  │ D. Effect sizes and modules               13 - 17  │
  │    per-knockout effects, gene & guide modules      │
  └─────┬──────────────────────────────────────────────┘
        │  module tables
  ┌─────▼──────────────────────────────────────────────┐
  │ E. Model inputs                           18 - 19  │
  │    combined object, train/test splits              │
  └─────┬──────────────────────────────────────────────┘
        │
        combinatorial_perturbations/  →  manuscript_figures/
```

## The notebooks

| # | Notebook | Produces |
|---|---|---|
| 01 | `01-upstream-qc` | per-channel cell calls |
| 02 | `02-downstream-qc` | filtered, concatenated channels |
| 03 | `03-mergeWithHash` | hashtag-demultiplexed singlets |
| 04 | `04-mergeWithCrispr` | `par_save_filename_1`, guide calls attached |
| 05 | `05_DownstreamIntegration` | `anndataFileName2`, the screen object |
| 06 | `06_SplitSingleAndMultipleKO` | `par_save_filename_5`, `par_save_filename_6` |
| 07 | `07_AnalyseGuideDepletion` | `par_guide_depletion_file` *(diagnostic)* |
| 08 | `08_SelectControlGuides` | `par_outlier_controlguides_file` |
| 09 | `09_FilterGenesAndCells` | `par_save_filename_7` |
| 10 | `10_FitGuideEffects_NegativeBinomial` *or* `10_FitGuideEffects_OLS` | per-guide coefficients under `par_guide_lm_dir` |
| 11 | `11_FitControlGuideEffects` | `par_control_coefs_file`, `par_control_pvals_file` |
| 12 | `12_SelectKnockoutGuides` | `par_bad_KO_guides_file`, `par_good_guides_file` |
| 13 | `13_ReduceGuidesToGenes` | `par_save_filename_8`, `par_save_filename_9` |
| 14 | `14_SelectWellPerturbedCells` | `par_em_selected_cells_file` |
| 15 | `15_EstimateKnockoutEffects` | `par_effect_coefs_file`, `par_effect_pvals_file` |
| 16 | `16_SelectSignificantEffects` | `par_effect_fdr_file`, `par_selected_coef_matrix_file` |
| 17 | `17_IdentifyGeneAndGuideModules` | `par_guideModules_file`, `par_geneModules_file` |
| 18 | `18_BuildCombinedKOObject` | `par_save_filename_11`, `par_save_filename_12` |
| 19 | `19_CreateTrainTestSplits` | the four objects under `par_dataset_dir` |

Notebook 07 is a diagnostic. Nothing downstream reads its output, so it can be
skipped without breaking the chain.

## Stage B — embed and cluster

Notebook 05 normalises to a fixed total, log-transforms, selects highly
variable genes, scales, runs PCA and builds the neighbour graph, then computes
the UMAP, a Leiden clustering at `par_leiden_clustering_resolution`, a
diffusion map, per-cluster marker genes and cell-cycle scores.

The `leiden` column it writes is regressed out of expression in notebooks 13
and 18 and is the grouping the EM in notebook 14 runs within. The UMAP is the
embedding Figures 1 and 2 draw. The DC subtype groupings in `par_subcelltypes`
name these clusters by number, so changing the resolution invalidates them.

## Stage C — guide quality control

Determines which guides produced a detectable effect.

Notebook 08 fits each control guide's effect on the principal components of the
control cells, then flags guides whose coefficient profile is an outlier among
control guides. Four detectors vote — isolation forest, elliptic envelope,
local outlier factor and a one-class SVM — and a guide flagged by more than
`par_control_guide_outlier_votes` of them is dropped.

Notebook 10 fits the knockout guides, and comes in two versions. Run one.

`10_FitGuideEffects_NegativeBinomial` fits `MASS::glm.nb` through `rpy2` per
response gene on raw counts, with `n_genes`, `mt_frac` and `leiden` as
covariates. Guides are taken in blocks of `par_guide_block_size` and genes in
blocks of `par_gene_block_size`. Setting `par_guide_block_start` fits one guide
block, so it can be run as several parallel processes.

`10_FitGuideEffects_OLS` fits ordinary least squares per response gene on the
log-normalised matrix, with all guides as covariates at once and the Leiden
cluster as dummies. Faster, but it models log-normalised values rather than
counts.

Each writes into its own subdirectory of `par_guide_lm_dir`, so both can exist
side by side. `par_guide_lm_model` selects which notebook 12 reads.

Notebook 12 correlates each guide's coefficient profile against every other.
For each gene: if every pair of its guides correlates above
`par_guide_pair_corr_threshold`, all are kept; otherwise only the
best-correlated pair survives. A guide in no surviving pair is a bad guide.

## Stage D — effect sizes and modules

Notebook 15 fits a linear mixed model per response gene, with the knockouts as
fixed effects and the Leiden cluster as a random effect. The coefficients are
FDR corrected within each gene, then reduced: a knockout is kept when it moves
more than `par_significant_target_cutoff` genes, a gene when more than
`par_significant_gene_cutoff` knockouts move it.

Notebook 16 corrects those coefficients within each gene and reduces them to
the knockouts and genes carrying signal, which is the matrix the clustering
reads. Notebook 17 clusters that matrix twice with Leiden — over knockouts at
`par_guide_module_resolution`, giving the guide modules, and over genes at
`par_gene_module_resolution`. The number of modules is the result, not a
setting.

The guide modules are the `K_0` … `K_5` of every saved table. In the published
analysis they map to the manuscript's module names as K0=M2, K1=M3, K2=M6,
K3=M5, K4=M1, K5=M4.

## Stage E — model inputs

Notebook 18 concatenates the two populations, restricts to the module genes,
recomputes the `ClusterResiduals` layer over that gene set, and labels each
cell with the guide module it was perturbed in. Notebook 19 splits the result
into train singles, doubles, same-module doubles and held-out controls.

## What you supply

One input is not produced by any notebook:

| Parameter | What it is |
|---|---|
| `par_initial_guide_pool_file` | cells per guide in the delivered plasmid pool |

It is provided in `TextFiles/`, and is needed only by notebook 07, which is a
diagnostic. Notebook 05 fetches the Regev lab cell-cycle gene list over the
network.

## What is provided rather than rerun

Four steps take days or longer, so their results are provided and the notebooks
document how they were produced. Each writes its own copy under `outputs/`, so
nothing provided is overwritten by a re-run.

| Step | Provided as |
|---|---|
| 08, control-guide selection | `TextFiles/OutlierControlGuides.csv` |
| 10 and 12, guide selection | `TextFiles/GuideSelect_BadKOGuides.csv`, `GuideSelect_GoodGuides.csv` |
| 14, the EM cell selection | `TextFiles/selectedCellsAfterEM.csv` |
| 15 and 16, the effect sizes | `TextFiles/ME_LMBetaCoefsALL.csv.gz`, `ME_LMBetaFDRALL.csv.gz`, `ME_SignificantBetaCoefs.csv` |

`TextFiles/README.md` lists every one of them with what it contains and which
notebooks read it. A few larger matrices are shared separately rather than
committed; they are listed there too.

## Reproducibility notes

**Blocked fits.** Notebooks 10, 11 and 16 fit in blocks and skip blocks already
on disk. Changing a block size after a partial run mixes incompatible outputs;
clear the output directory instead.

**Positional control split.** In notebook 18 the first `par_n_control_train`
control cells train and the next `par_n_control_test` test. The split follows
row order and is not seeded.

**Unseeded resampling.** `combinatorial_perturbations/04` draws a fresh random
half-split on each run. `ComboEffects_doublesResampleRes.rds`, which Figures 5A
and 5ACD read, is therefore not reproducible exactly; the 25 saved
per-iteration files record the published splits.

**Cluster numbering.** Leiden labels depend on the graph and the implementation
version. Rerunning notebook 5 or 17 can renumber clusters and modules even
when the partition is nearly unchanged, which affects `par_subcelltypes` and
every table keyed by `K_0` … `K_5`.

**Not yet run end to end.** Notebooks 05 to 19 are committed without outputs.
Compare the cell, gene and guide counts each step prints against the numbers in
the paper before treating a result as reproduced.
