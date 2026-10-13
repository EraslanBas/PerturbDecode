# Reference tables

Small tables the notebooks read that no notebook here produces, or that are
cheaper to keep than to regenerate. Committed so the figures can be re-run
without the screen's large intermediate files — 5 MB in all.

Anything the notebooks *write* goes to the screen's data root instead; see
`../paths.py` and `data/README.md`.

## Contents

| File | Read by |
|---|---|
| `ME_GuideModules_leiden_6_Modules.csv` | Figures 2A-C, 2D, 3A, 3F, 3G, 4A, 4B/E/H, S5E; `combinatorial_perturbations/04` |
| `ME_GeneModules_leiden_11_Modules.csv` | Figures 2A-C, 2D, 3F, 4B/E/H, 5ACD |
| `ME_GeneModules_leiden_8_Modules.csv` | `00_BuildGuideModuleObject` |
| `SignificantCoefMatrix.csv` | Figures 4A, 4B/E/H, S5C/D, S5E |
| `ICA_15_factors_effectedGenes_paper.csv` | Figures 4B/E/H, 4C/D/F/G/I/J |
| `ComboKOModels.csv` | Figures 5F, 5G |
| `DC_cellstate_genes.csv` | Figures 1C-H, 3C/D, S1H-Z |
| `Leiden_top100Markers.csv` | Figure S1H-Z |
| `NoOfCellsPerGuide.csv` | Figure S2Z |
| `TF_targets.csv`, `ScoredTFs.csv`, `TF_score_Coefs.csv`, `TF_score_Pvals.csv` | Figure 3G |
| `220610_regulators_metadata_E3_Complex.csv` | Figures 3A, 3F, 3G |
| `Only_E3s.csv`, `allSimulatedFreq.rds` | Figure 3F |
| `allGuidesPerLeiden_withTests_PERGENE.rds` | Figure S2A/B |

The guide and gene module tables are the ones
`build_anndata/17_IdentifyGeneAndGuideModules` reproduces; the rest were
assembled by hand or come from external sources (STRING, published metadata).
The large STRING files those were derived from are not here — they are 133 MB
and 988 MB — and are read from the data root.
