# Reference tables

Small tables the notebooks read, and the small results they write. Both are
committed so the analysis can be rerun from the screen object alone, and so the
published numbers can be checked without rerunning anything.

## Inputs

Read by the notebooks, produced by none of them.

| File | Read by | What it is |
|---|---|---|
| `OutlierControlGuides.csv` | `09_FilterGenesAndCells` | The 31 control guides that showed a transcriptional effect and are dropped from the control population. Notebook 08 records how they were selected and writes its own result to a separate file, so this one is left untouched by a re-run. |
| `ME_SignificantBetaCoefs.csv` | `16_IdentifyGeneAndGuideModules` | The knockout-by-gene effect-size matrix, reduced to the knockouts and genes carrying signal. A knockout is kept when it moves more than `par_significant_target_cutoff` genes at `par_effect_fdr_cutoff`, a gene when more than `par_significant_gene_cutoff` knockouts move it. Rows are knockouts as `GENE_<target>_`, columns are response genes, values are fitted coefficients. This is the matrix notebook 16 clusters into gene and guide modules. |
| `GuideSelect_BadKOGuides.csv` | `13_ReduceGuidesToGenes` | The 958 knockout guides whose effect profile did not agree with another guide against the same gene, dropped before guides are collapsed onto their target. Notebooks 10 and 12 record how they were identified; that fit takes days across all guides, so its result is provided here. |
| `GuideSelect_GoodGuides.csv` | — | The 2,256 guides that were kept, as the gene and guide pairs that agreed. Companion to the file above; the two are disjoint and together cover the knockout guides that survived filtering. |
| `GuidePoolSummary_2.csv` | `07_AnalyseGuideDepletion` | One row per guide: the number of cells that guide contributed to the delivered plasmid pool. Notebook 07 compares each gene's share of the pool with its share of the screen to find guides whose targets are essential. |

## Outputs

Written by the notebooks and committed so the published numbers are readable
without rerunning them. Rerunning overwrites them in place.

| File | Written by | What it is |
|---|---|---|
| `NoOfCellsPerGuide_GeneLevel.csv` | `07_AnalyseGuideDepletion` | One row per target gene: its cell count in the pool and in the screen, both as proportions, with the depletion p-value and FDR. 1,130 genes; 419 are depleted at FDR < 0.1, led by *Mdm2*, *Copa*, *Gnb4*, *Traip* and *Cdc20*. |

## Downloaded separately

Four tables from the guide-effect fits are too large for this repository. They
are shared as files, and the notebooks look for them **by these exact names**:

| File | Size | Read by |
|---|---|---|
| `GuideSelect_weights.csv` | 402 MB | `12_SelectKnockoutGuides` |
| `GuideSelect_pvals.csv` | 379 MB | nothing; the matching p-values, kept for completeness |
| `Control_coefs.csv` | 43 MB | the supplementary figure notebooks |
| `Control_pValues.csv` | 40 MB | the supplementary figure notebooks |

The two `Control_*` files are notebook 11's result: each control guide's fitted
effect on each gene, and the matching p-values. They are the null distribution
the knockout effects are read against.

`GuideSelect_weights.csv` holds each guide's fitted effect on each gene, 6,560
genes by 3,204 guides, with the gene and guide names already in the file.

To use it, put it in the directory named by `par_downloaded_data_dir`, which is
`data/` by default, keeping the file name:

```
notebooks/build_anndata/
  data/
    GuideSelect_weights.csv
    GuideSelect_pvals.csv
    Control_coefs.csv
    Control_pValues.csv
```

Notebook 12 then reads it instead of assembling the per-block fits from
notebook 10, which takes days across all guides. If neither is present the
notebook stops and says so rather than failing part way through.

Neither file is needed to run the rest of the analysis: the selection they lead
to is provided above as `GuideSelect_BadKOGuides.csv` and
`GuideSelect_GoodGuides.csv`, and notebook 13 reads the first of those
directly.
