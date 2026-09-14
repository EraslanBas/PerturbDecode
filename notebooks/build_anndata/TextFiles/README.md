# Reference tables

Small tables the notebooks read, and the small results they write. Both are
committed so the analysis can be rerun from the screen object alone, and so the
published numbers can be checked without rerunning anything.

## Inputs

Read by the notebooks, produced by none of them.

| File | Read by | What it is |
|---|---|---|
| `GuidePoolSummary_2.csv` | `07_AnalyseGuideDepletion` | One row per guide: the number of cells that guide contributed to the delivered plasmid pool. Notebook 07 compares each gene's share of the pool with its share of the screen to find guides whose targets are essential. |

## Outputs

Written by the notebooks and committed so the published numbers are readable
without rerunning them. Rerunning overwrites them in place.

| File | Written by | What it is |
|---|---|---|
| `NoOfCellsPerGuide_GeneLevel.csv` | `07_AnalyseGuideDepletion` | One row per target gene: its cell count in the pool and in the screen, both as proportions, with the depletion p-value and FDR. 1,130 genes; 419 are depleted at FDR < 0.1, led by *Mdm2*, *Copa*, *Gnb4*, *Traip* and *Cdc20*. |
