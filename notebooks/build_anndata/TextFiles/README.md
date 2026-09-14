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

## Notes on `GuidePoolSummary_2.csv`

3,719 guides, matching 3,710 of the 3,720 in the screen object. The ten that do
not match are accounted for:

- Nine are genes whose names contain a hyphen — `Rnf8-cmtr1`, `Siah1-ps1`,
  `Siah1-ps2`, three guides each. The pool table writes them with underscores,
  and notebook 07 restores the hyphens before merging.
- `ONE_NONGENE_SITE_330` appears in the screen but has no pool entry, so it
  drops out of the comparison.

Line 890 is a totals row, `Fullstats,2361996`, sitting among the guides rather
than at the top or bottom of the file. Notebook 07 removes it by name. Left in,
it would be treated as a guide contributing 2.4 million cells and would distort
every proportion in the depletion test.

A second file named `GuidePoolSummary.csv` exists in the original analysis tree.
It is a different table and matches the screen object far less well (3,519 of
3,720 guides). It is not the one to use.
