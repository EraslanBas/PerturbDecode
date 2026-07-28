---
sd_hide_title: true
---

# PerturbDecode

::::{grid} 1
:::{grid-item}
:class: sd-text-center sd-fs-1 sd-font-weight-bold

PerturbDecode
:::
:::{grid-item}
:class: sd-text-center sd-fs-5 sd-text-secondary

A probabilistic framework for large-scale perturbation screens — from deciding
which measurements to trust, to predicting the experiments you never ran
:::
::::

---

Pooled CRISPR screens read out by single-cell sequencing promise a causal map of
gene function. Getting there means confronting a specific set of problems, most
of which are usually handled with disconnected heuristics applied after the fact.

PerturbDecode approaches them with a single generative model, **ComBVAE**, used
first to decide *which measurements are real* and then to *predict measurements
that were never made*.

:::{admonition} Development status
:class: note
PerturbDecode is under active development. Each challenge below is marked with
its current state, and the {doc}`pipeline table <tutorials/index>` shows which
stages are usable today. Nothing here is claimed as working before it is.
:::

## The challenges

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} Perturbation effects are sparse
{bdg-success}`Available`
^^^
Single-gene perturbations detected by Perturb-seq produce sparse, subtle
transcriptional changes. Testing each perturbation against controls in isolation
is badly underpowered.

**Approach.** ComBVAE places every perturbation in a shared latent space, so
each is estimated with support from the entire screen rather than only its own
cells.
::::

::::{grid-item-card} The effect varies across cells
{bdg-secondary}`Planned`
^^^
Not every cell carrying a guide is properly perturbed. Incomplete editing and
escaping cells mean a perturbation label is not the same thing as a perturbed
cell, and including unperturbed cells dilutes every downstream estimate.

**Approach.** Beyond filtering guides, PerturbDecode will filter *individual
cells* that show no evidence of perturbation, using the model's cell-level
representation. The method is defined; the implementation is not yet in the
package.
::::

::::{grid-item-card} Guide consistency is only knowable after the experiment
{bdg-success}`Available`
^^^
Whether the guides targeting a gene actually agree cannot be determined at
design time — it is a property of the data you have already generated.

**Approach.** ComBVAE learns an embedding per guide; guides nominally targeting
the same gene are then tested for concordant phenotypes by partial correlation
conditioned on the control guides, which removes shared technical structure
before any judgement is made. See
{func}`~perturbdecode.selectWorkingGuides`.
::::

::::{grid-item-card} Perturbation effects are non-linear
{bdg-success}`Available`
^^^
Linear models cannot represent effects that depend on cell state or that combine
non-additively — which is much of the interesting biology.

**Approach.** The conditional VAE uses non-linear encoders and decoders, so
perturbation effects are modelled as non-linear functions of latent state rather
than as additive shifts.
::::

::::{grid-item-card} Grouping genes by disentangled latent factors
{bdg-secondary}`Planned`
^^^
Grouping perturbed genes by correlation of their raw effect vectors is
noise-sensitive. Grouping them by the *latent factors they affect* is a more
robust measure of functional connection.

**Approach.** Perturbations will be grouped through the disentangled factors of
the learned representation rather than through raw expression correlation.
::::

::::{grid-item-card} No tool handles multiome perturbation screens
{bdg-secondary}`Planned`
^^^
Screens with joint RNA and chromatin-accessibility readouts have no dedicated
analysis tool, despite the readout being increasingly common.

**Approach.** Extending the conditional framework to multiple simultaneous
modalities is on the roadmap.
::::

::::{grid-item-card} Unseen combinations must be predicted, not measured
{bdg-secondary}`Planned`
^^^
With a thousand targets there are half a million pairs. Predicting which
combinations are worth running is what makes screen design efficient.

**Approach.** Because perturbations occupy a continuous latent space rather than
a lookup table, the model can generate expected responses to combinations that
were never assayed.
::::

::::{grid-item-card} Computation becomes the bottleneck at scale
{bdg-warning}`In development`
^^^
At hundreds of thousands of cells and thousands of perturbations, naive
implementations stop being practical.

**Approach.** GPU training for the model, and batched, parallel estimation for
the effect-size stage. The parallel effect-size path is written but not yet
wired up — see the {doc}`release notes <changelog>`.
::::

:::::

## The pipeline

Each stage is an importable function operating on {class}`~anndata.AnnData`.

| | Stage | Status | What it produces |
|---|---|---|---|
| 01 | [Quality control](tutorials/01_quality_control.md) | {bdg-secondary}`v1 notebooks` | Filtered, concatenated expression object |
| 02 | [Guide assignment](tutorials/02_guide_assignment.md) | {bdg-secondary}`v1 notebooks` | Cells labelled with the guides they carry |
| 03 | [ComBVAE](tutorials/03_combvae.md) | {bdg-success}`Available` | Perturbation embeddings; cell embeddings with perturbation factored out |
| 04 | [Guide selection](tutorials/04_guide_selection.md) | {bdg-success}`Available` | The subset of guides with reproducible phenotypes |
| 05 | [Effect sizes](tutorials/05_effect_sizes.md) | {bdg-warning}`Partial` | Coefficient and FDR matrices — the beta matrix |
| 06 | [Modules](tutorials/06_modules.md) | {bdg-secondary}`Planned` | Gene programmes and perturbation groups |
| 07 | [Combination prediction](tutorials/07_prediction.md) | {bdg-secondary}`Planned` | Predicted responses to unmeasured combinations |
| 08 | [Enrichment](tutorials/08_enrichment.md) | {bdg-secondary}`Planned` | Complexes, transcription factors, pathways |

:::{note}
Stages 03 and 04 are what distinguish PerturbDecode. The generative model is not
only a downstream analysis — it is the instrument used to decide which of your
measurements to trust.

Stages marked *v1 notebooks* were performed for the manuscript using
[PerturbDecode_v1](https://github.com/EraslanBas/PerturbDecode_v1) and are
documented here as a methods record; they are not yet part of the package API.
:::

## Installation

```bash
pip install PerturbDecode
```

See {doc}`installation` for the optional R integration and development setup.

## Quick example

```python
import perturbdecode as pd

# Train the model on every guide in the screen
pd.createTrainValData(adata, "guide_id", guides, dataDir="out/")
pd.runTrainingComBVAE(model_dir="out/models", ...)

# Use the learned embedding to find the guides that actually worked
_, _, embeddings, guide_list = pd.extract_model_embeddings(...)
pert_embed, _ = pd.visualizePerturbationEmbeddings(embeddings, guide_list)
working, stats = pd.selectWorkingGuides(pert_embed, ["NTC"], numberOfGuidesPerTarget=4)
```

## Example data

The tutorials use a genome-scale Perturb-seq screen of ~1,130 E3 ligases in
primary mouse dendritic cells, available from
[GEO GSE327057](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE327057).

## Citation

If you use PerturbDecode in your research, please cite the accompanying
manuscript — see {doc}`about/citation`. The analysis code used for the
manuscript is archived at
[PerturbDecode_v1](https://github.com/EraslanBas/PerturbDecode_v1); it predates
this package and does not reflect the current API.

```{toctree}
:hidden:
:maxdepth: 2

installation
tutorials/index
concepts/index
api/index
```

```{toctree}
:hidden:
:caption: Development

contributing
changelog
about/citation
```
