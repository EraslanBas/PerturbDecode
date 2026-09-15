# Reference tables

Small tables the notebooks read, and the small results they write. They are
committed so the analysis can be rerun from the screen object alone, and so the
published numbers can be checked without rerunning anything.

Each file below names the notebook that **produces** it and the notebooks that
**read** it. Where a file is provided rather than regenerated, the notebook
that would produce it writes its own copy under `outputs/` instead, so nothing
here is overwritten by a re-run.

## Contents

| File | Rows | Produced by | Read by |
|---|---|---|---|
| `GuidePoolSummary_2.csv` | 3,719 guides | not produced here — supplied | `07_AnalyseGuideDepletion` |
| `NoOfCellsPerGuide_GeneLevel.csv` | 1,130 genes | `07_AnalyseGuideDepletion` | — |
| `OutlierControlGuides.csv` | 31 guides | `08_SelectControlGuides` | `09_FilterGenesAndCells` |
| `GuideSelect_BadKOGuides.csv` | 958 guides | `12_SelectKnockoutGuides` | `13_ReduceGuidesToGenes` |
| `GuideSelect_GoodGuides.csv` | 2,085 pairs | `12_SelectKnockoutGuides` | — |
| `selectedCellsAfterEM.csv` | 242,938 cells | `14_SelectWellPerturbedCells` | `15_EstimateKnockoutEffects`, `18_BuildCombinedKOObject` |
| `ME_LMBetaCoefsALL.csv.gz` | 1,035 × 6,685 | `15_EstimateKnockoutEffects` | `16_SelectSignificantEffects` |
| `ME_LMBetaFDRALL.csv.gz` | 1,031 × 6,685 | `16_SelectSignificantEffects` | manuscript figure notebooks |
| `ME_SignificantBetaCoefs.csv` | 329 × 1,041 | `16_SelectSignificantEffects` | `17_IdentifyGeneAndGuideModules` |

## What each one is

**`GuidePoolSummary_2.csv`** — one row per guide, `GuideName` and `Ncells`: how
many cells that guide contributed to the delivered plasmid pool. The only input
here that no notebook produces. Notebook 07 compares each gene's share of the
pool with its share of the screen, so a gene whose knockout is lethal shows up
as depleted.

Two quirks the notebook handles. A totals row named `Fullstats` sits among the
guides rather than at either end, and would otherwise be read as a guide
contributing 2.4 million cells. And three gene names containing a hyphen —
`Rnf8-cmtr1`, `Siah1-ps1`, `Siah1-ps2` — are written with underscores, so they
are restored before the merge.

**`NoOfCellsPerGuide_GeneLevel.csv`** — one row per target gene: its cell count
in the pool and in the screen, both as proportions, with the z-test statistics,
p-values and FDR in both directions. 419 genes are depleted at FDR < 0.1, led
by *Mdm2*, *Copa*, *Gnb4*, *Traip* and *Cdc20*.

**`OutlierControlGuides.csv`** — the control guides that did show a
transcriptional effect and are therefore dropped from the control population. A
control guide is supposed to be inert; one that is not would bias every
knockout effect measured against it.

**`GuideSelect_BadKOGuides.csv`** — the knockout guides whose effect profile did
not agree with another guide against the same gene, in a column named `x`.
Dropped in notebook 13 before guides are pooled onto their target, since
pooling a guide that did not work dilutes the gene-level estimate.

**`GuideSelect_GoodGuides.csv`** — the guides that were kept, as the gene and
the pair of guides that agreed. Companion to the file above: the two are
disjoint and together cover the knockout guides that survived filtering.

**`selectedCellsAfterEM.csv`** — the cells the expectation-maximisation step
judged to be genuinely perturbed, one barcode per row in a column named `x`. A
cell can carry a guide and show no transcriptional response to it; those are
excluded so they do not dilute the effect estimates. Notebooks 15 and 18 subset
to these cells rather than a separate object being written.

**`ME_LMBetaCoefsALL.csv.gz`** — the assembled fit: every knockout against
every response gene. Rows are the fitted terms — the intercept, the 1,031
knockouts, the two quality covariates and the random-effect variance — and
columns are the response genes. Gzipped, which `pandas.read_csv` handles
directly; no decompression step is needed.

**`ME_LMBetaFDRALL.csv.gz`** — the same matrix after correction within each
gene, restricted to the knockout rows. Notebook 16 reads this when notebook 15
has not been run, rather than recomputing it, and the manuscript figure
notebooks read it too.

**`ME_SignificantBetaCoefs.csv`** — the knockout-by-gene effect-size matrix,
reduced to what carries signal: a knockout is kept when it moves more than
`par_significant_target_cutoff` genes at `par_effect_fdr_cutoff`, a gene when
more than `par_significant_gene_cutoff` knockouts move it. Rows are knockouts
as `GENE_<target>_`, columns are response genes, values are fitted
coefficients. This is what notebook 17 clusters into gene and guide modules.

## Downloaded separately

These are too large for the repository and are shared as files. The notebooks
look for them **by these exact names**, in the directory named by
`par_downloaded_data_dir`, which is `data/` by default.

| File | Size | Produced by | Read by |
|---|---|---|---|
| `GuideSelect_weights.csv` | 402 MB | `10_FitGuideEffects_*` | `12_SelectKnockoutGuides` |
| `GuideSelect_pvals.csv` | 379 MB | `10_FitGuideEffects_*` | — |
| `Control_coefs.csv` | 43 MB | `11_FitControlGuideEffects` | supplementary figure notebooks |
| `Control_pValues.csv` | 40 MB | `11_FitControlGuideEffects` | supplementary figure notebooks |
| `ME_LMPValuesALL.csv` | 41 MB | `15_EstimateKnockoutEffects` | `16_SelectSignificantEffects` |
| `ME_LMBetaCoefsALL_Control.csv` | 17 MB | the control effect fit | `16_SelectSignificantEffects`, as the null |
| `ME_LMPValuesALL_Control.csv` | 16 MB | the control effect fit | `16_SelectSignificantEffects`, as the null |

Nothing in the chain needs the guide-level pair: the selection they lead to is
already provided above. The `_Control` pair is the same model run over control guides, which notebook
16 uses as the null when choosing its cutoff.

Put them in place and the notebooks find them:

```
notebooks/build_anndata/
  data/
    GuideSelect_weights.csv
    ME_LMBetaCoefsALL.csv
    ...
```
