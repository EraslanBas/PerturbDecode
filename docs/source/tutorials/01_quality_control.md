# 01 · Quality control

:::{admonition} Step 1 of 5: the pipeline walkthrough
:class: tip, dropdown
You are on **step 1**, *Quality control*. See the [full stage list](index.md), or start from the [quickstart](quickstart.md) for the whole pipeline on one page.
:::

This stage takes the assembled object produced in
[00 · Generating the AnnData object](00_data_preparation.md) and returns a
filtered object of properly perturbed cells, with working guides pooled to
their target genes.

Quality control here is not a fixed sequence of thresholds. It first establishes
which cell states the screen contains, and then uses ComBVAE itself to decide
which guides and which cells carry real perturbation signal.

## 1. Understanding the structure of the data

Before any perturbation is tested it is worth knowing what cell states are
present. A screen in primary cells is rarely homogeneous, and the substructure
found here matters for every step that follows: clusters become covariates in
the effect-size model, and a perturbation that shifts cells between states looks
very different from one that changes expression within a state.

This corresponds to `05-downstreamIntegration.ipynb`.

```python
adata.layers["counts"] = adata.X.copy()
sc.pp.normalize_total(adata, target_sum=10_000)
sc.pp.log1p(adata)
adata.raw = adata

sc.pp.highly_variable_genes(adata, n_top_genes=2000)
sc.pp.scale(adata, max_value=10)

sc.pp.pca(adata, n_comps=50, svd_solver="arpack")
sc.pp.neighbors(adata, n_neighbors=15, metric="euclidean")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
```

```{image} ../_static/figures/structure/umap_leiden.png
:alt: UMAP of all cells coloured by leiden cluster
:width: 60%
:align: center
```

Marker genes tell you what the clusters are. In the E3 ligase screen these
separate dendritic cell states rather than arbitrary partitions, which is the
result you want before proceeding.

```python
sc.tl.rank_genes_groups(adata, groupby="leiden", n_genes=2000,
                        method="t-test_overestim_var")
```

```{image} ../_static/figures/structure/marker_dotplot.png
:alt: Dot plot of top marker genes per leiden cluster
:width: 100%
```

Two technical sources of structure are worth scoring explicitly, because both
can masquerade as a perturbation effect. Cell cycle phase drives a large
fraction of transcriptional variance in proliferating cells, and mitochondrial
content tracks cell health.

```python
sc.tl.score_genes_cell_cycle(adata, s_genes=s_genes, g2m_genes=g2m_genes)
```

::::{grid} 1 2 2 2
:::{grid-item}
```{image} ../_static/figures/structure/umap_phase.png
:alt: UMAP coloured by inferred cell cycle phase
```
:::
:::{grid-item}
```{image} ../_static/figures/structure/mito_diagnostics.png
:alt: Mitochondrial fraction against counts and detected genes
```
:::
::::

Finally the cells are split by how many guides they carry, since single and
multiple knockouts are analysed differently from here on.

```python
fbar = adata.obs[adata.uns["feature_barcode_names"]]
fbar[fbar > 0] = 1

adata.obs["KONo"]   = fbar.sum(axis=1).to_numpy()
adata.obs["KOType"] = np.where(adata.obs.KONo > 1, "MultipleKO", "SingleKO")
```

### When the population is not homogeneous

The clustering above is not only descriptive. If the screen contains genuinely
distinct cell states, and in particular if the **control cells** occupy several
states, a single model fitted across all of them will confound perturbation
effects with cell state. A perturbation enriched in one state will appear to
have the transcriptional signature of that state.

There are two ways to handle this:

**Condition on cell state.** Add the state label as a further conditioning
variable alongside perturbation identity, so the model accounts for it
explicitly.

**Fit one model per cell state.** Analyse each state separately. This is the
cleaner option when states are strongly distinct, but it requires each
perturbation to retain enough cells within each state to be estimable, which
becomes the limiting constraint in a large screen.

In the E3 ligase screen the model was fitted on the largest population alone.
That sidesteps the confounding entirely at the cost of discarding the other
states, and is a reasonable choice when one population dominates.

:::{note}
Whichever route you take, decide it here. Everything from this point rests on
the assumption that the cells being compared are comparable.
:::

## 2. Fitting ComBVAE three times

The model is not fitted once. Quality control runs it three times, each on a
different labelling of the same cells, because each pass answers a different
question and each depends on the previous one having cleaned the data it uses.

| Fit | Perturbation label | Purpose |
|---|---|---|
| First | Individual guide | Remove untrustworthy guides |
| Second | Target gene | Remove cells that were not properly perturbed |
| Third | Target gene, clean data | Produce the perturbation embeddings used downstream |

The ordering matters. Guides have to be judged before cells, because a cell
assigned to a dead guide cannot be assessed for whether it responded. Cells have
to be filtered before the final embedding, because unperturbed cells drag every
perturbation towards the control.

### First fit: at the guide level

The first fit treats **each guide as its own perturbation**, with no pooling by
target gene. At this point guide identity is the only label that is certain,
and pooling guides by their annotated target would assume exactly what is being
tested.

Two kinds of guide are removed using the resulting embeddings.

**Outlier non-targeting controls.** A screen carries many non-targeting guides,
and together they define the reference against which everything else is
measured. A control guide whose embedding sits away from the control population
is behaving like a perturbation, whether through an unintended cut site or an
effect of the guide sequence itself. Leaving it in corrupts the reference.

**Targeting guides with outlier off-target effects.** A guide can produce a
strong phenotype that has nothing to do with its intended target. These are
identified as guides whose embeddings are inconsistent with the other guides
against the same gene.

What remains are the guides retained on the **conditional dependency structure**
of the whole embedding space: guides against the same gene are kept when their
phenotypes are concordant, given the controls.

:::{admonition} Draft
:class: caution
Code, figures and counts for this subsection still to be written.
:::

<!-- TODO:
     - Show the call: runTrainingComBVAE, extract_model_embeddings,
       visualizePerturbationEmbeddings, selectWorkingGuides.
     - Figures: guide embedding space; control guide distribution with outliers
       marked; concordance statistics for retained versus dropped guides.
     - Counts at each removal criterion. Source material available:
       PerturbMap/SRC/Outputs/model_4 (best.pth, TrainTestErrors.csv over 1000
       epochs), E3Ligase TextFiles/GuideSelect_GoodKOGuides.csv (1752 rows) and
       GuideSelect_BadKOGuides.csv (1145 rows).
-->

### Second fit: at the target gene level

With trustworthy guides selected, the model is fitted again, now with cells
labelled by **target gene** rather than by individual guide. This pass is what
identifies cells that carry a guide but show no evidence of having been
perturbed, whether through incomplete editing or escape.

Filtering cells here, rather than earlier, is deliberate. Whether a cell
responded can only be judged against what the perturbation does in general, and
that is only estimable once the guides defining it are known to work.

:::{admonition} Draft
:class: caution
Not yet implemented in the package. Method and figures to be written.
:::

<!-- TODO:
     - How unperturbed cells are identified from this fit.
     - Where the threshold sits and how it is chosen.
     - Counts before and after.
     - State the implementation status plainly.
-->

### Third fit: on the clean data

The final fit runs on the filtered object: working guides only, properly
perturbed cells only, pooled to target gene. Its output is the perturbation
embedding that the rest of the pipeline consumes, and it is the object that
[effect sizes](02_effect_sizes.md), [modules](03_modules.md) and
[combination prediction](04_prediction.md) are all built on.

:::{admonition} Draft
:class: caution
Code, figures and counts for this subsection still to be written.
:::

<!-- TODO:
     - Show that this embedding is cleaner than the first-fit embedding.
     - Final object dimensions.
     - What is handed to the downstream stages.
-->

## Next step

::::{grid} 1
:::{grid-item-card} 02 · Effect sizes
:link: 02_effect_sizes
:link-type: doc

Continue the walkthrough.
:::
::::

