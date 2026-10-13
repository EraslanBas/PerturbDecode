# Combinatorial perturbation fits

The regression results that the Figure 5 notebooks read. Committed — a narrow
exception to the repository's no-data rule, the same one made for
`build_anndata/TextFiles` — so those figures can be re-run from a clone without
first regenerating them, which would need the `.h5ad` objects from
[GEO GSE327057](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE327057).

All of it is 5 MB. The notebooks that produce these files write to `outputs/`
instead, so nothing here is overwritten by a re-run.

## The pooled fits

| File | Produced by | Read by |
|---|---|---|
| `ComboEffects_lm_residuals.rds` | `01_FitCombinationEffects_NoInteractionTerms` | Figures 5A, 5B, 5F, 5G |
| `ComboEffects_lm_residuals_withInteractions.rds` | `02_FitCrossModuleInteractions` | Figures 5A, 5ACD, 5F, 5G, `00_InteractionTerms` |
| `ComboEffects_doublesSameGroup.rds` | `03_FitSameModuleDoubleEffects` | Figures 5A, 5B, `00_InteractionTerms` |
| `ControlCellsMeanExp.rds` | `03_FitSameModuleDoubleEffects` | Figure 5ACD — the bottom row of the 5D heatmap |
| `PertCellsMeanExp.rds` | `03_FitSameModuleDoubleEffects` | nothing; kept so this is the complete output of 01-05 |
| `ComboEffects_doublesResampleRes.rds` | `05_AverageSameModuleInteractionSplits` | Figures 5A, 5ACD, `00_InteractionTerms` |

Notebooks 01 to 03 each fit one ordinary least squares model per response gene,
1,041 of them, with the guide module indicators as covariates. Their
coefficients were checked against a re-fit of a 25-gene sample: identical
`(gene, term)` keys and estimates agreeing to 5e-16 or better.

## The individual splits

| File | Produced by | Read by |
|---|---|---|
| `ComboEffects_doublesResample_KO_<module>_<iteration>.rds`, 25 files | `04_FitSameModuleInteraction_SingleSplit` | `05_AverageSameModuleInteractionSplits`, `00_InteractionTerms` |

`<module>` is 0-4 and `<iteration>` is 1-5. Notebook 04 fits one module and one
iteration per run; the twenty-five files were produced by setting `GUIDE_GROUP`
and `ITERATION` by hand and re-running.

These **cannot be regenerated**. The half-split is drawn with an unseeded
`random.sample`, so a re-run fits different halves and produces different
coefficients. They are the only record of the splits behind the published
figures.

Module 5 is absent. It is M4, and it has too few same-module doubles to split,
which is why M4 has no same-module interaction bar in Figure 5A.

Each file is a `broom::tidy` table of one fit per response gene,
`y ~ a + b + a*b`, where `a` and `b` are the two random halves of that module's
knockouts: one row per gene per term, the two main effects and the `a:b`
interaction. Notebook 05 keeps the interaction row, FDR corrects the five
splits together within each gene, zeroes what fails at 0.1, and averages.

A gene therefore ends up non-zero in `ComboEffects_doublesResampleRes.rds` when
its within-module interaction was significant in at least one of the five
splits. The values in that file are **averaged effect-size estimates, not
FDRs** — 1,024 of its 5,205 cells are non-zero.
