# 01 · Quality control

:::{admonition} Step 1 of 5: the pipeline walkthrough
:class: tip, dropdown
You are on **step 1**, *Quality control*. See the [full stage list](index.md), or start from the [quickstart](quickstart.md) for the whole pipeline on one page.
:::

## 1. Generating the AnnData object

Everything downstream operates on a single {class}`~anndata.AnnData` object in
which each row is a cell that passed quality control and carries a known
perturbation. Building that object from sequencing output takes four steps:
calling real cells, filtering and merging the channels, resolving which sample
each cell came from, and attaching the guides each cell received.

:::{important}
**This part is not the package.** PerturbDecode begins once the combined
`AnnData` object exists. Assembling it is highly experiment dependent, so
rather than impose one procedure, we provide the notebooks used for the E3
ligase screen as a worked example that you can adapt.
:::

### Using these notebooks for your own screen

The four notebooks are in the repository under
[`notebooks/build_anndata/`](https://github.com/EraslanBas/PerturbDecode/tree/main/notebooks/build_anndata).
They run against two files you fill in for your experiment:

- **`samples.csv`**, one row per channel. `sample_name` and `raw` are required;
  any other column you add is copied into `.obs`.
- **`parameters.py`**, holding paths and thresholds. Every value in it is
  experiment specific and must be reviewed before use.

Adapt the steps to your design rather than running all four blindly. The E3
ligase screen multiplexed samples with hashtag oligos and read out guides
through a CRISPR feature-barcode library, so it needs the full sequence. A
screen without hashing skips step 3 entirely; a screen whose guide calls arrive
in a different format replaces step 4 with its own join.

| Notebook | Purpose | Skip it if |
|---|---|---|
| `01-upstream-qc` | Cell calling with `emptyDrops`, QC metrics, diagnostics | never, some form of cell calling is always required |
| `02-downstream-qc` | Per-cell filtering, concatenation, gene filtering | never |
| `03-mergeWithHash` | Hashtag demultiplexing, keeping singlets | you did not multiplex with hashing |
| `04-mergeWithCrispr` | Attaching guide calls from the feature-barcode table | your guide calls arrive in another format |

The figures and counts below come from running these notebooks on the full E3
ligase screen, described in
[Geiger-Schuller, Eraslan et al., bioRxiv 2023](https://www.biorxiv.org/content/10.1101/2023.01.23.525198v1),
*Systematically characterizing the roles of E3-ligase family members in
inflammatory responses with massively parallel Perturb-seq*.

:::{note}
These steps consume per-channel CellRanger output, hashtag demultiplexing
results and feature-barcode tables. Those are intermediate files, and they are
not deposited in GEO. To follow the rest of the walkthrough without rebuilding
anything, download the assembled screen from
[GEO GSE327057](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE327057)
and pick up at subsection 2 below. To rebuild from scratch, begin with the
raw reads under BioProject PRJNA1449386.
:::

The E3 ligase screen enters this process as 47 channels across two experimental
rounds and leaves it as one object:

| Step | Operation | Cells |
|---|---|---|
| 1 | Per-channel cell calling | ~21,000 to 28,000 per channel |
| 2 | Filter and concatenate 47 channels | **1,071,671** |
| 3 | Hashtag demultiplexing, singlets only | |
| 4 | Attach guides, drop cells without a confident call | **519,535** |

### Step 1: call real cells in each channel

A droplet experiment produces far more barcodes than cells. Most contain only
ambient RNA, and the boundary between an empty droplet and a small or
low-quality cell is not obvious from total counts alone.

Each channel is read separately, annotated with its sample-sheet metadata, and
tested with `emptyDrops` from
[DropletUtils](https://bioconductor.org/packages/DropletUtils/), which compares
each barcode against the ambient profile rather than applying a fixed threshold.
Per-cell QC metrics are computed at the same time.

```python
for sample in sample_sheet.itertuples():
    ad = sc.read_10x_h5(path) if sample.raw else sc.read(path)
    ad.var_names_make_unique()

    # Test each barcode against the ambient RNA profile
    emptydrops(ad, lower=200, niters=10_000, ignore=10, retain=1000)

    ad.obs["n_umis"]  = ad.X.sum(1)
    ad.obs["n_genes"] = (ad.X != 0).sum(1).A1

    # Coarse cutoffs before any per-cell modelling
    ad = ad[ad.obs.n_umis  > 1000]
    ad = ad[ad.obs.n_genes > 300]

    ad.obs["barcode_rank"] = scipy.stats.rankdata(-ad.obs["n_umis"])
    mt = ad.var_names.str.startswith("mt-")
    ad.obs["mt_frac"] = ad.X[:, mt].sum(1).A1 / ad.obs["n_umis"]
```

The barcode-rank curve is the first thing to inspect. Each panel is one channel,
with the two red lines marking the `ignore` and `lower` bounds given to
`emptyDrops`. A healthy channel shows a clear plateau of real cells and a sharp
drop into the ambient population.

```{image} ../_static/figures/qc/barcode_rank.png
:alt: Barcode rank against UMI count for each of the 47 channels
:width: 100%
```

Total counts against detected genes shows whether the two move together as they
should. Barcodes falling below the diagonal have many reads spread over few
genes, which usually means ambient RNA or a dying cell.

```{image} ../_static/figures/qc/umis_vs_genes.png
:alt: UMIs against detected genes for each channel
:width: 100%
```

The same relationship coloured by `emptyDrops` FDR shows what the test
contributes over a threshold. Points that pass on total counts but score poorly
against the ambient profile are exactly the barcodes a fixed cutoff would keep
by mistake.

```{image} ../_static/figures/qc/umis_vs_genes_emptydrops.png
:alt: UMIs against detected genes coloured by EmptyDrops FDR
:width: 100%
```

The count and gene distributions are worth comparing across channels, since a
channel whose mode sits well away from the others usually indicates a loading or
sequencing-depth problem rather than biology.

::::{grid} 1 2 2 2
:::{grid-item}
```{image} ../_static/figures/qc/umi_distributions.png
:alt: UMI count distributions per channel
```
:::
:::{grid-item}
```{image} ../_static/figures/qc/gene_distributions.png
:alt: Detected gene distributions per channel
```
:::
::::

### Step 2: filter and combine the channels

With cells called, per-cell thresholds are applied and the channels are merged.
The mitochondrial fraction is the informative cut here: a cell whose transcripts
are largely mitochondrial was stressed or dying when captured, and its
expression profile reflects that rather than its perturbation.

```python
for ad in samples.values():
    sc.pp.filter_cells(ad, min_genes=300)
    sc.pp.filter_cells(ad, min_counts=1000)
    ad._inplace_subset_obs(ad.obs.empty_drops_FDR < 0.01)
    ad._inplace_subset_obs(ad.obs.mt_frac < 0.15)
    ad._inplace_subset_var(~ad.var_names.str.startswith("mt-"))

adata = sc.AnnData.concatenate(*samples.values(), join="outer",
                               batch_key="sample_name",
                               batch_categories=list(samples))
sc.pp.filter_genes(adata, min_cells=400)
```

Mitochondrial genes are removed after filtering on them, so that the fraction is
computed from the full transcriptome but the genes themselves do not contribute
to downstream variation. Requiring a gene in at least 400 cells removes those
too rare to estimate an effect on.

This yields **1,071,671 cells by 31,040 genes** across the 47 channels.

### Step 3: resolve which sample each cell came from

Channels are multiplexed, so cells from several samples share a lane and are
separated by hashtag oligos. Demultiplexing assigns each barcode to a sample and
labels doublets, which is the point at which two cells captured together become
detectable.

```python
hash_ad = sc.AnnData.concatenate(*hash_ads.values(),
                                 batch_key="mixhash",
                                 batch_categories=list(hash_ads))

adata.obs["demux_type"]      = hash_ad.obs.demux_type
adata.obs["hash_assignment"] = hash_ad.obs.assignment

adata = adata[adata.obs.demux_type == "singlet"]
```

Only singlets continue. A doublet carries two sets of guides and would appear as
a perturbation combination that was never constructed, which is precisely the
signal [step 04](04_prediction.md) sets out to predict.

### Step 4: attach the guides

The final step joins the feature-barcode table, recording which guides were
detected in each cell. Two filters are applied to the guide counts before the
join.

```python
# A guide seen once is indistinguishable from index hopping
feats = feats.replace(1, 0)
feats = feats[feats.sum(axis=1) > 1]

# Drop guides making up a negligible share of a cell's CRISPR reads
frac = feats.div(feats.sum(axis=1), axis=0)
feats[frac < 0.2] = 0
feats = feats[feats.sum(axis=1) > 0]

adata = adata[adata.obs.index.isin(feats.index)]
adata.obs = adata.obs.join(feats, how="inner")
adata.uns["feature_barcode_names"] = feats.columns.tolist()
```

The first filter discards single-read guide calls, which are as likely to come
from index hopping or ambient guide RNA as from genuine infection. The second
handles chimeric reads: a guide contributing less than 20% of a cell's CRISPR
reads is treated as contamination from another cell rather than as a real
perturbation.

The effect is substantial. The guide matrix goes from 1,166,357 cells to 757,147
after the single-read filter, and to 754,450 after the chimeric filter. Joining
against the hash-filtered expression object leaves **519,535 cells**, each with
a confident sample assignment and a confident set of guides.

### Parameters

| Parameter | Value | Notes |
|---|---|---|
| `initial_umi_cutoff` | 1000 | Coarse pre-filter before `emptyDrops` |
| `initial_gene_cutoff` | 300 | As above |
| `empty_drops_lower` | 200 | Counts below this define the ambient profile |
| `empty_drops_niters` | 10000 | Monte Carlo iterations; sets the lowest reachable p-value |
| `empty_drops_ignore` | 10 | Barcodes below this are not tested at all |
| `empty_drops_retain` | 1000 | Counts above this are always retained |
| `empty_drops_fdr_cutoff` | 0.01 | Applied at step 2 |
| `cutoff_min_counts` | 1000 | Per-cell, after cell calling |
| `cutoff_min_genes` | 300 | Per-cell |
| `cutoff_min_cells` | 400 | Per-gene |
| `mito_cutoff` | 0.15 | Maximum mitochondrial fraction |
| `crispr_chimeric_reads` | 0.2 | Minimum share of a cell's CRISPR reads for a guide to count |

Raising `mito_cutoff` above roughly 0.2 admits dying cells whose profiles are
dominated by stress response. The chimeric threshold is the parameter to
revisit if a screen shows implausibly many multi-guide cells, since ambient
guide contamination scales with loading density.


## 2. Understanding the structure of the data

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

In the E3 ligase screen the model was fitted on the **DC2 population alone**,
the largest of the states identified above, giving **144,138 cells**. That
sidesteps the confounding entirely at the cost of discarding the other states,
and is a reasonable choice when one population dominates.

:::{note}
Whichever route you take, decide it here. Everything from this point rests on
the assumption that the cells being compared are comparable.
:::

## 3. Fitting ComBVAE three times

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

For the E3 ligase screen this fit ran on the DC2 population with 2,132 guide
covariates over 6,685 genes, using 64 latent dimensions and a 64 dimensional
perturbation embedding, trained for 1,000 epochs.

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

