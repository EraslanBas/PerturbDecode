# Combinatorial perturbation models

The Figure 5 notebooks read five `.rds` files of regression coefficients. The
coefficients are not committed — they are large, and they are results rather
than source — so the notebooks that produce them are kept here instead, to
record how each number was arrived at.

## What produces what

| Notebook | Fits | Writes | Read by |
|---|---|---|---|
| `01_FitCombinationEffects_NoInteractionTerms.ipynb` | one coefficient per perturbation combination: each single module and each module pair is its own dummy covariate, with no interaction terms | `ComboEffects_lm_residuals.rds` | Figures 5A, 5B, 5F, 5G |
| `02_FitCrossModuleInteractions.ipynb` | `y ~ K_0 + ... + K_5` plus all fifteen `K_i*K_j` products | `ComboEffects_lm_residuals_withInteractions.rds` | Figures 5A, 5ACD, 5F, 5G |
| `03_FitSameModuleDoubleEffects.ipynb` | `y ~ K_0 + ... + K_5` over same-module doubles against control cells; also means expression per module and for controls | `ComboEffects_doublesSameGroup.rds`, `ControlCellsMeanExp.rds`, `PertCellsMeanExp.rds` | Figures 5A, 5B; the control means are the bottom row of the 5D heatmap. `PertCellsMeanExp.rds` is read by nothing. |
| `04_FitSameModuleInteraction_SingleSplit.ipynb` | one module, one random half-split: `y ~ a + b + a*b` | `ComboEffects_doublesResample_KO_<module>_<iteration>.rds` | notebook 05 |
| `05_AverageSameModuleInteractionSplits.ipynb` | nothing; pools the five splits per module, FDR corrects, zeroes what fails, averages | `ComboEffects_doublesResampleRes.rds` | Figures 5A, 5ACD |

Notebook 04 fits **one module and one iteration per run** — `guideGroup` and
`iteration` are set by hand in a cell near the top. The twenty-five files on
disk, five modules by five iterations, were produced by editing those two
numbers and re-running. The notebook is currently parked on `guideGroup = 5`,
for which no output exists: module 5 is M4, and it is absent from the figures
for that reason.

The half-split is **not seeded**. `random.sample` draws a fresh half each run,
so re-running notebook 04 will not reproduce the splits behind the published
numbers. The saved per-iteration files are the only record of which genes went
into which half.

## The three models

Each fits one ordinary least squares model per response gene, 1,041 of them,
with the guide module indicators as covariates.

**Between modules.** `y ~ K_0 + ... + K_5 + K_0*K_1 + ... + K_4*K_5`, on cells
carrying knockouts from two different modules. The fifteen `K_i:K_j` terms ask
whether two modules together move a gene by more or less than the sum of their
separate effects.

**Within one module, directly.** `y ~ K_0 + ... + K_5`, on cells carrying two
knockouts from the same module. There is no interaction term and there cannot
be: a variable cannot interact with itself. `K_0` is a main effect.

**Within one module, as an interaction.** The module's genes are split at random
into halves, each half becomes its own covariate, and `y ~ a + b + a*b` is
fitted, so the two knockouts of a double land in different variables. The split
is arbitrary, so it is repeated five times per module; each run is FDR corrected
on its own, non-significant coefficients are zeroed, and the five are averaged.
Modules 0 to 4 have enough same-module doubles for this. Module 5, which is M4,
does not.

`00_InteractionTerms.ipynb` in `../manuscript_figures` states the same three
models and counts what each one produced.

## Running these

They are recorded for provenance rather than for routine re-execution. Each
fits 1,041 models through `%%R` magic over the combinatorial-KO cell matrix,
and the resample notebook does that twenty-five times.

Paths have been repointed: inputs are read from the E3 ligase analysis tree,
and `saveRDS` writes to `outputs/` here, so re-running produces local copies
rather than overwriting the originals the figures currently read.

One cell of `01_FitCombinationEffects_NoInteractionTerms.ipynb` reads
`ComboEffects_lm_residuals_2.rds`, which no notebook in this folder writes and
which is not on disk. That cell will fail; the rest of the notebook does not
depend on it.
