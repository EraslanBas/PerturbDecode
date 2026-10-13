# Manuscript figure notebooks

The notebooks that produced the figures in Geiger-Schuller, Eraslan et al.,
*Systematically characterizing the roles of E3-ligase family members in
inflammatory responses with massively parallel Perturb-seq*, bioRxiv 2023,
[doi:10.1101/2023.01.23.525198](https://doi.org/10.1101/2023.01.23.525198).

They are kept here as a **methods record**: the code behind each published
panel, in the state it was run. They are not part of the PerturbDecode package,
are not installed by `pip install PerturbDecode`, and are not maintained against
the current API. They come from
[PerturbDecode_v1](https://github.com/EraslanBas/PerturbDecode_v1), which
predates the package.

For the current, supported pipeline see the
[tutorials](https://perturbdecode.readthedocs.io/en/latest/tutorials/index.html).

## What each notebook produces

| Notebook | Kernel | Panels | Writes |
|---|---|---|---|
| `00_BuildGuideModuleObject.ipynb` | Python | builds the guide-module object the Figure 5 notebooks read | `outputs/adata_SingleKO_GuideModules.h5ad` |
| `00_InteractionTerms.ipynb` | R | reference: the three combinatorial models and what each produced | — |
| `00_LPSPlusMinusAnalysis.ipynb` | Python | LPS +/- comparison underlying Figure 1 | `outputs/LPSPlusOverMinusDEGenes.csv` |
| `Figure1_CDEFGH.ipynb` | Python | Figure 1C-H | — |
| `Figure1_I-GeneLevel.ipynb` | Python | Figure 1I, gene level | `figures/Figure_1I.pdf` |
| `Figure2_ABC.ipynb` | Python | Figure 2A-C | — |
| `Figure2_D.ipynb` | R | Figure 2D | `outputs/GuideModuleGeneModuleEffectSignificance.csv` |
| `Figure3_A.ipynb` | R | Figure 3A, Supp. 1H | `figures/Figure_S4A.pdf`, `figures/Figure_S4B.pdf` |
| `Figure3_B.ipynb` | Python | Figure 3B | — |
| `Figure3_CD.ipynb` | Python | Figure 3C, 3D | — |
| `Figure3_E.ipynb` | R | Figure 3E, Supp. 4D, 4E | `figures/Figure3_E.pdf` |
| `Figure3_F.ipynb` | R | Figure 3F | `outputs/Only_E3s.csv` |
| `Figure3_G.ipynb` | R | Figure 3G | `figures/Figure_3G.pdf`, `figures/Figure_3G_2.pdf`, `figures/S_4J.pdf`, `outputs/Figure_3G_matrix.csv`, `outputs/TF_score_Coefs_Katie.csv` |
| `Figure4_A.ipynb` | R | Figure 4A | `figures/Figure_4A.pdf`, `outputs/ExplainedVariancePerFactor.csv` |
| `Figure4_BEH.ipynb` | R | Figure 4B, E, H | `figures/S_5G.pdf`, `figures/S_5H.pdf`, `figures/Factor_<n>.pdf` |
| `Figure4_CDFGIJ.ipynb` | Python | Figure 4C, D, F, G, I, J | — |
| `Figure5_A.ipynb` | R | Figure 5A | `figures/Figure_5A.pdf` |
| `Figure5_B.ipynb` | R | Figure 5B | `figures/Figure_5B.pdf` |
| `Figure5_CD.ipynb` | R | Figure 5D, Supp. 6B; the 5C assignment is unsettled | `figures/Figure_5D.pdf`, `figures/Figure_S6B.pdf`, `figures/M<i>_M<j>.pdf` ×15, `outputs/Fig_5D.csv`, `outputs/CombosInter.csv` |
| `Figure5_F.ipynb` | R | Figure 5F, Supp. 7D, 7E | `figures/S_7E.pdf` |
| `Figure5_G.ipynb` | R | Figure 5E, Supp. 6O, 6P, 7F | `figures/S_7F.pdf`, `figures/Figure_5E.pdf` |
| `SuppFigure1_F.ipynb` | R | Supp. 1F | `figures/S_1F.pdf` † |
| `SuppFigure1_G.ipynb` | R | Supp. 3A, 3B | `figures/S_3B.pdf` † |
| `SuppFigure1_HZ.ipynb` | Python | Supp. 1H-Z | — † |
| `SuppFigure_2AB.ipynb` | Python | Supp. 2A, 2B | `figures/S_2AB.pdf`, `outputs/SupFig_1Z.csv` † |
| `SuppFigure_2Z.ipynb` | R | Supp. 2Z | `figures/S_2Z.pdf`, `outputs/GuideDepletion.csv`, `outputs/GuideDepletion_ControlGuidesBackground.csv` † |
| `SuppFigure_5CD.ipynb` | R | Supp. 5C, 5D | `figures/S_5C.pdf`, `figures/S_5D.pdf` † |
| `SuppFigure_5E.ipynb` | R | Supp. 5E | `figures/S_5E.pdf` † |

† Not executed since the port, so the outputs listed for these seven have
not been produced and are absent from `figures/` and `outputs/`. Everything
else in the table has been run and its files are on disk.

Paths are relative to this folder. `Figure5_CD` also writes one heatmap per
module pair, named `M<i>_M<j>.pdf`, and `Figure4_BEH` one per ICA factor,
named `Factor_<n>.pdf`.

10 notebooks run on the IPython kernel, several calling into R through `rpy2`'s `%%R` magic, and 18 on the IRkernel. `Main.R`, `Conf.R`,
`Utilities.R`, `libraries.py` and `parameters.py` are the shared setup they
source.

## Why they are not executable as committed

The notebooks are committed **with** their outputs, so the published figures are
readable on GitHub without the data. They cannot, for the most part, be re-run
from this repository, for two reasons.

**The data is not here and is not distributable.** They read the intermediate
results of the full E3 ligase screen: effect-size matrices, gene and guide
module assignments, combinatorial-perturbation RDS files, and `.h5ad` objects
that run to tens of gigabytes each. None of that is in this repository, and the
assembled screen is available from
[GEO GSE327057](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE327057)
rather than from here.

**The paths they use are those of the original analysis tree.** Every notebook
reads relative paths such as `./../TextFiles/` and `./../MixedEffectLMOutputs/`,
and the Python ones `os.chdir(projectDir)` into an absolute path set in
`parameters.py`. Those locations describe the analysis directory as it stood in
2023; reproducing a figure means pointing them at your own copy of the
corresponding inputs.

The six notebooks that read the combinatorial-perturbation fits are the
exception, and they need no data at all. `00_InteractionTerms`, `Figure5_A`,
`Figure5_CD`, `Figure5_B`, `Figure5_F` and `Figure5_G` read
`../combinatorial_perturbations/RDSFiles/`, which is committed — 5 MB of
regression results. Four of them re-run from a clone as they stand. The
exceptions are `Figure5_F` and `Figure5_G`, which have not been run since the
port and still `source("Main.R")`, which breaks ggplot.

`Conf.R` still carries the absolute paths of the machine the analysis was
originally run on, which no longer exist.

## Dependencies

Beyond the PerturbDecode dependencies these notebooks need the `[r]` extra, an
IRkernel, and the R packages sourced by `Main.R`: `pheatmap`, `corrplot`,
`ggplot2`, `cowplot`, `RColorBrewer`, `pls`, `data.table`, `reshape2`,
`factoextra`, `maptree`, `ggpubr`, `ica`, `ICtest`, `repr`, `plyr`.
