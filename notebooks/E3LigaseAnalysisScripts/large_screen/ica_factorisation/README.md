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
| 03 | `03_ChooseNumberOfFactors_HeldOut` | R | `figures/HeldOutExplainedVariance.pdf` |
| 04 | `04_FactorizeBetaMatrix` | R | `outputs/ICA_15_factors_effectedGenes.csv`, `outputs/factorGeneGroups.rds` |

The first three weigh the number of components; the fourth does the
decomposition. 01 and 02 are the two halves of the original `IdentifyK`
notebook, split because 01 needs `ICtest`, which once attached registers an
`Ops` method that collides with ggplot2 4.x's S7 objects and breaks every `+`
chain for the rest of the session — detaching it does not undo that, so the
ggplot-drawn sweep in 02 cannot share a session with it.

03 is what was `07_FactorizeBetaMatrix_ICAPredict`. Only the first nine of its
fifty-nine cells had ever been executed, and those nine are a held-out
evaluation rather than a projection; everything after them was copied from the
factorisation notebook and refers to an `icaimax` fit that notebook never makes,
so it could not have run. The notebook is now what those nine cells do, and the
dead tail is gone.

## How 15 was chosen

Five criteria, across 01 to 03:

| Criterion | Where | Result here |
|---|---|---|
| FOBI asymptotic test | 01 | rejects at every k tested |
| FOBI bootstrap test, 200 replicates | 01 | p = 0.005 |
| FOBI ladle estimator | 01 | 56 |
| Explained variance, in sample | 02 | 0.20 at k=2, 0.49 at k=15, 0.80 at k=100 |
| Explained variance on held-out knockouts | 03 | six random 20% splits, 1 to 30 components |

The formal tests do not land on 15 — the ladle estimate is 56 — so the choice
rests on the variance curve, where 15 sits at the shoulder. That is worth
knowing when citing the number.

## Reproducing the published factor table

`04` reproduces `ICA_15_factors_effectedGenes_paper.csv` **byte for byte** — all
15 factors, both sides, the membership and the group 1 / group 2 split within
each one.

That took finding one number. The ported copy clipped the per-factor matrix at
±0.5 before clustering it; the published table was made at ±0.2. The clip only
ever affected the `ward.D2` clustering that divides each factor in two, never
which knockouts and genes belong to the factor, which is why membership matched
from the start while 18 of the 60 columns did not. Scanning the threshold:

| clip | splits matching, of 30 |
|---|---|
| 0.10 | 25 |
| 0.15 | 25 |
| **0.20** | **30** |
| 0.25 | 26 |
| 0.30 | 24 |
| 0.50 (as ported) | 21 |

Nothing else in that space came close: `ward.D`, `complete` and `average`
linkage, correlation distance, and `cutree(k = 2)` against the height loop all
left the same nine splits wrong.

The decomposition is deterministic. `icaimax` defaults to `Rmat = diag(nc)`, so
there is no random initialisation and no seed to set, and the factors come out
the same on every run.

## Notes on the port

**Four things could never have run.** `names(pathwayTargets)` in the tail
referred to a list the loop never creates — it builds `pathwayKOs` — which is
the kind of error that survives in a section that was never executed.
`corrplot(order = 'AOE')` fails on corrplot 0.95, which masks the lower triangle
before computing the ordering, so `eigen()` then sees NAs; the order is now
computed first and the reordered matrix drawn, which gives the same picture.
`plot()` on the ladle object does not fit on any device tried, so 01 draws
`ladleplot()` instead, which is the figure that was wanted. And the held-out
notebook called `%ni%`, `computeR2` and `melt` without loading or defining any
of them.

**Dead parameters.** `geneCutOff` and `targetCutOff` are set and never read.

**Inputs are committed.** `SignificantCoefMatrix.csv` and the gene and guide
module tables all come from `../reference/`, so these notebooks run from a
clone.
