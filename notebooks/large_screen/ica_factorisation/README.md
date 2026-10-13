# ICA factorisation of the effect-size matrix

Decomposes the significant coefficient matrix into 15 independent components,
and records how that number was chosen. The factor table it produces is what
Figures 4B/E/H and 4C/D/F/G/I/J read.

Ported from `R/07_FactorizeBetaMatrix_*.ipynb` in the E3 ligase analysis tree.

## The notebooks

| # | Notebook | Kernel | Produces |
|---|---|---|---|
| 01 | `01_ChooseNumberOfFactors_Tests` | R | `figures/LadlePlot.pdf` |
| 02 | `02_ChooseNumberOfFactors_ExplainedVariance` | R | `outputs/ExplainedVarianceByNumberOfFactors.csv`, `figures/ExplainedVarianceByNumberOfFactors.pdf` |
| 03 | `03_FactorizeBetaMatrix` | R | `outputs/ICA_15_factors_effectedGenes.csv`, `outputs/factorGeneGroups.rds` |
| 04 | `04_ProjectFactors` | R | — |

01 and 02 are the two halves of the original `IdentifyK` notebook. They are
split because 01 needs `ICtest`, which once attached registers an `Ops` method
that collides with ggplot2 4.x's S7 objects and breaks every `+` chain for the
rest of the session — detaching it does not undo that, so the ggplot-drawn
sweep in 02 cannot share a session with it.

## How 15 was chosen

Four criteria, all in 01 and 02:

| Criterion | Result here |
|---|---|
| FOBI asymptotic test | rejects at every k tested |
| FOBI bootstrap test, 200 replicates | p = 0.005 |
| FOBI ladle estimator | 56 |
| Explained variance of the reconstruction | 0.20 at k=2, 0.49 at k=15, 0.80 at k=100 |

The formal tests do not land on 15 — the ladle estimate is 56 — so the choice
rests on the variance curve, where 15 sits at the shoulder. That is worth
knowing when citing the number.

## Reproducing the published factor table

`03` reproduces **the membership of every factor exactly**. For all 15 factors,
on both the gene and the guide side, the set of members matches
`ICA_15_factors_effectedGenes_paper.csv` exactly, and 42 of its 60 columns are
identical outright.

The remaining 18 columns differ in **how each factor's members are split into
group 1 and group 2**, not in who belongs to the factor. That split comes from
cutting a `ward.D2` dendrogram, and it could not be reproduced exactly. Tried:
the height loop the notebook uses and `cutree(k = 2)` (identical results);
`ward.D`, `complete` and `average` linkage; correlation distance; and clipping
the matrix at 0.3, 0.5, 1.0 and not at all. The best of those matched 24 of the
30 factor-and-side splits, against 21 for the notebook's own settings — so no
setting in that space reaches all 30.

The likely reason is that the committed `_paper` file was written by a version
of this notebook that differed in the splitting step. In the copy that was
ported, the entire tail that writes the file — the factor loop and everything
after it — had never been executed: cells 49 to 65 carried no outputs.

The decomposition itself is deterministic. `icaimax` defaults to `Rmat = diag(nc)`,
so there is no random initialisation and no seed to set.

## Notes on the port

**Three things could never have run.** `names(pathwayTargets)` in the tail
referred to a list the loop never creates — it builds `pathwayKOs` — which is
the kind of error that survives in a section that was never executed.
`corrplot(order = 'AOE')` fails on corrplot 0.95, which masks the lower triangle
before computing the ordering, so `eigen()` then sees NAs; the order is now
computed first and the reordered matrix drawn, which gives the same picture.
And `plot()` on the ladle object does not fit on any device tried, so 01 draws
`ladleplot()` instead, which is the figure that was wanted.

**Dead parameters.** `geneCutOff` and `targetCutOff` are set and never read.

**Inputs are committed.** `SignificantCoefMatrix.csv` and the gene and guide
module tables all come from `../reference/`, so these notebooks run from a
clone.
