# Parameters for building the initial AnnData object.
#
# THIS FILE MUST BE EDITED. The values below are the ones used for the E3
# ligase screen and are kept as a worked example. Paths in particular will not
# exist on your system.
#
# projectDir      absolute path to your project root; the notebooks chdir here
# par_data_dir    directory holding the per-channel files listed in samples.csv
# par_species     "mouse" or "human"; selects the mitochondrial gene prefix

projectDir = "/home/eraslab1/Projects/E3Ligase/analysisSingle/"
anndataFileName="outputs/anndata/adata-hash-features_singlets_05232020.h5ad"
anndataFileName2="outputs/anndata/adata-hash-features_singlets_05242020.h5ad"

par_species = "mouse"
par_data_dir = "data"
par_initial_umi_cutoff = 1000
par_initial_gene_cutoff = 300
par_empty_drops_lower_umi_cutoff = 200
par_empty_drops_ignore_cutoff = 10
par_empty_drops_niters = 10000
par_empty_drops_fdr_cutoff = 0.01
par_empty_drops_retain = 1000
par_cutoff_min_counts = 1000
par_cutoff_min_genes = 300
par_cutoff_min_cells = 400
par_cutoff_max_genes = None
par_cutoff_crispr_chimeric_reads = 0.2
par_final_empty_drops_fdr_cutoff = 0.01
par_remove_mito_genes = True
par_mito_cutoff = 0.15
par_remove_sex_genes = False
par_preprocessing_target_sum = 10000
par_regress_out_variables = []
par_regress_out_n_jobs = 6
par_downstream_n_top_genes = 2000
par_downstream_hvg_batch_key = None
par_downstream_n_pcs = 50
par_downstream_n_neighbors = 15
par_downstream_louvain_resolution = 1
par_downstream_neighbor_metric = "euclidean"
par_save_filename_sample = "outputs/anndata/adata-sample-%s.h5ad"
#### File names of the saved anndata objects:
## After transcriptome integration
par_save_filename_1 = "outputs/anndata/adata.h5ad"
## Anndata object containing the cells with single gene KOs
par_save_filename_5 = "outputs/anndata/adata-SingleKO.h5ad"
## Anndata object containing the cells with multiple gene KOs
par_save_filename_6 = "outputs/anndata/adata-MultipleKO.h5ad"
## Anndata object containing the cells and guides for guide effect testing
par_save_filename_7 = "outputs/anndata/adata-SingleKO_Filtered.h5ad"
## Single KO anndata object after KO guides are merged at the target gene level
par_save_filename_8 = "outputs/anndata/adata-SingleKO_PerGENE.h5ad"
## Multiple KO anndata object after KO guides are merged at the target gene level
par_save_filename_9 = 'outputs/anndata/adata-MultipleKO_PerGENE.h5ad'
## Single KO anndata object after unperturbed cells are filtered out
par_save_filename_10 = "outputs/anndata/adata-SingleKO_PerGENE_EMselected.h5ad"


par_save_filename_group = "outputs/anndata/adata-group-%s.h5ad"
par_remove_doublets = True
par_generate_plots_per_group = True
par_group_key = "round"
par_merge_type = "outer"
par_batch_key = "sample_name"
par_de_group = "leiden"
par_de_n_genes = 2000
par_de_method = "t-test_overestim_var"
par_per_group_de = True
par_save_filename_de = "outputs/reports/de-genes.xlsx"
par_save_filename_de_group = "outputs/reports/de-genes-%s.xlsx"
par_leiden_clustering_resolution=0.5
par_predefined_genesets_filename='TextFiles/PositiveControls/DC_cellstate_genes.csv'
par_initial_guide_pool_file='TextFiles/GuidePoolSummary_2.csv'
par_outlier_controlguides_file='./TextFiles/OutlierControlGuides.csv'
## Number of minimum number of cells considered for selecting the tested genes
par_mincells_for_testedgenes=20000
## Number of genes a cell should have to be used while testing the guide effects
par_mincellgenes_for_testedgenes=800
## Number of cells a guide should have to reliably assess its effect on gene expression
par_ncell_test_threshold=20
par_not_target_control_prefix="NO_TARGET_"
par_nongene_site_control_prefix="ONE_NONGENE_SITE_"
par_guide_testres_file='./TextFiles/GuideKOTestRes.csv'
par_control_testres_file='./TextFiles/GuideControlTestRes.csv'
par_test_guide_interval=200
par_test_guide_method='OLS'
par_bad_KO_guides_file = './TextFiles/GuideSelect_BadKOGuides.csv'
par_test_target_dist='NB'
par_test_target_model='MixedEfNB'
par_test_target_interval=10
par_test_target_file='./TextFiles/TargetTestRes_2.csv'
par_selected_coef_matrix_file='TextFiles/ME_SignificantBetaCoefs.csv'
par_guideModules_file="Leiden_guide_modules.csv"
par_geneModules_file="Leiden_gene_modules.csv"


# ---------------------------------------------------------------------------
# Notebook 05: downstream integration
# ---------------------------------------------------------------------------
## Written by notebook 05 and read by notebook 06 onwards. This is the screen
## object: normalised, embedded and clustered.
par_downstream_diffmap = True
## Per-cluster marker genes, written by notebook 05.
par_leiden_markers_file = "TextFiles/LeidenMarkerGenes.csv"

# ---------------------------------------------------------------------------
# Notebooks 07-12: guide quality control
# ---------------------------------------------------------------------------
## Number of principal components the control-guide effects are fitted over.
par_control_guide_n_pcs = 100
## A control guide is dropped when more than this many of the four outlier
## detectors flag it.
par_control_guide_outlier_votes = 2
## Contamination rate for the outlier detectors that take one.
par_control_guide_contamination = 0.1
## Seed for the two outlier detectors that are internally stochastic. The
## original analysis set no seed; see the note in notebook 08.
par_control_guide_random_state = 0

## Notebook 08 writes its recomputed list here. The list the rest of the
## analysis reads, par_outlier_controlguides_file, is provided in TextFiles and
## is left untouched by a re-run.
par_outlier_controlguides_recomputed_file = "outputs/OutlierControlGuides_recomputed.csv"

par_guide_depletion_file = "TextFiles/NoOfCellsPerGuide_GeneLevel.csv"

## Per-guide negative binomial fits, written by notebook 10.
## The fit runs one model per response gene with a block of guides as
## covariates; both block sizes are here.
par_guide_block_size = 150
## Which guide block notebook 10 fits. None fits every block in sequence; set an
## integer (with papermill, say) to fit one block per process in parallel.
par_guide_block_start = None
par_gene_block_size = 20
par_nb_control_cells = 5000
par_guide_lm_dir = "outputs/GuideCellLM"
## Which of the two notebook-10 fits notebook 12 reads: "NegativeBinomial" or
## "OLS". Each notebook writes into its own subdirectory of par_guide_lm_dir,
## so both can exist side by side and be compared.
par_guide_lm_model = "NegativeBinomial"
par_guide_lm_fit_dir = par_guide_lm_dir + "/" + par_guide_lm_model
par_guide_lm_weights_file = par_guide_lm_dir + "/GuideSelect_weights.csv"
par_guide_lm_pvals_file = par_guide_lm_dir + "/GuideSelect_pvals.csv"
par_good_guides_file = "TextFiles/GuideSelect_GoodGuides.csv"

## Notebook 12 writes its recomputed lists here. The lists the rest of the
## analysis reads, par_bad_KO_guides_file and par_good_guides_file, are provided
## in TextFiles and are left untouched by a re-run.
par_bad_KO_guides_recomputed_file = "outputs/GuideSelect_BadKOGuides_recomputed.csv"
par_good_guides_recomputed_file = "outputs/GuideSelect_GoodGuides_recomputed.csv"

## Files that are too large for the repository and are downloaded separately.
## Put them in this directory, keeping their names; see TextFiles/README.md.
par_downloaded_data_dir = "data"

## The fitted guide coefficients, genes by guides, from the published analysis.
## If this file is present, notebook 12 reads it instead of assembling the
## per-block fits from notebook 10, which takes days to produce.
par_guide_lm_weights_input = par_downloaded_data_dir + "/GuideSelect_weights.csv"
## The matching p-values. Not read by anything; listed so the pair is documented.
par_guide_lm_pvals_input = par_downloaded_data_dir + "/GuideSelect_pvals.csv"

## The control-guide fits from the published analysis, assembled. Read by the
## supplementary figure notebooks rather than by anything here.
par_control_coefs_input = par_downloaded_data_dir + "/Control_coefs.csv"
par_control_pvals_input = par_downloaded_data_dir + "/Control_pValues.csv"

## Control-guide effect sizes, written by notebook 11 and read by SuppFigure1_F.
par_control_lm_dir = "outputs/ControlGuideEffects"
## Notebook 11 writes its assembled control-guide fits here. They are large, so
## they stay out of the repository; the published versions are downloaded
## separately as par_control_coefs_input / par_control_pvals_input below.
par_control_coefs_file = "outputs/Control_coefs.csv"
par_control_pvals_file = "outputs/Control_pValues.csv"

## Two guides against the same gene agree when the correlation between their
## beta profiles exceeds this. If every pair for a gene clears it, all are kept;
## otherwise only the best-correlated pair is.
par_guide_pair_corr_threshold = 0.015

# ---------------------------------------------------------------------------
# Notebooks 12 and 13: effect sizes and modules
# ---------------------------------------------------------------------------
## Which model notebook 15 fits. "NB" uses a negative binomial mixed model
## (lme4::glmer.nb) on raw counts; anything else uses a linear mixed model
## (statsmodels MixedLM) on normalised expression.
##
## The two differ in more than the likelihood. glmer.nb cannot carry a thousand
## fixed effects, so the NB path fits par_target_block_size knockouts at a time
## against a fixed panel of control cells, while the linear path fits all
## knockouts together against the whole population.
par_target_block_size = 10
par_nb_target_control_cells = 5000
par_effect_nb_dir = "outputs/MixedEffectNegativeBinomialLMOutputs"

## Notebook 15 writes these; they are tens of megabytes, so they stay out of
## the tracked directory. The reduced matrix it derives,
## par_selected_coef_matrix_file, is small and is provided in TextFiles.
par_effect_coefs_file = "outputs/ME_LMBetaCoefsALL.csv"
par_effect_pvals_file = "outputs/ME_LMPValuesALL.csv"
par_effect_fdr_file = "outputs/ME_AdjustedPValues.csv"
par_selected_coef_matrix_recomputed_file = "outputs/ME_SignificantBetaCoefs_recomputed.csv"
par_effect_fdr_cutoff = 0.1
## A knockout is kept when it moves more than this many genes at that FDR;
## a gene is kept when more than this many knockouts move it.
par_significant_target_cutoff = 14
par_significant_gene_cutoff = 4

## Leiden resolutions for the module clustering in notebook 13. The number of
## modules is the result, not a setting.
par_guide_module_resolution = 0.9
par_gene_module_resolution = 0.8

# ---------------------------------------------------------------------------
# Notebooks 14 and 15: model inputs
# ---------------------------------------------------------------------------
## Combined single + multiple KO object, per target gene
par_save_filename_11 = "outputs/anndata/adata-AllKO_PerGENE.h5ad"
## The same object reduced to the module genes, with the ClusterResiduals layer
## and the K_0..K_5 guide-module columns. Input to the combinatorial models.
par_save_filename_12 = "outputs/anndata/adata-AllKO_modelInput.h5ad"

par_dataset_dir = "outputs/anndata/dataset"
par_save_filename_trainsingles = par_dataset_dir + "/adataTrainSingles.h5ad"
par_save_filename_doubles = par_dataset_dir + "/adataDoubles.h5ad"
par_save_filename_doubles_samegroup = par_dataset_dir + "/adataDoubles_sameGroup.h5ad"
par_save_filename_testcontrol = par_dataset_dir + "/adataTestControl.h5ad"

## Probability cutoff for the EM in notebook 11. Cells at or below this carry a
## guide but show no transcriptional response to it.
## The cells the EM judged to be genuinely perturbed, written by notebook 14.
## Notebooks 15 and 17 subset the per-gene object to these before fitting, so
## the large intermediate object never has to exist.
par_em_selected_cells_file = "TextFiles/selectedCellsAfterEM.csv"

par_em_probability_cutoff = 0.7

## Control cells held out by notebook 15. The split is positional, not seeded.
par_n_control_train = 20000
par_n_control_test = 21000

## Leiden clusters grouped into DC subtypes by notebook 14.
par_subcelltypes = {
    "SubCellType_0": ["0", "1", "4", "7"],
    "SubCellType_1": ["2", "6"],
    "SubCellType_2": ["5", "8"],
    "SubCellType_3": ["3", "9"],
}

## Genes appended to the module gene list before the response set is fixed.
par_extra_response_genes = [
    "0610012G03Rik", "2010005H15Rik", "2010111I01Rik", "2310001H17Rik",
    "2810474O19Rik", "H2-Q7", "H2-Q6", "H2-DMa", "H2-T23", "H2-DMb1",
    "H2-Ab1", "H2-Aa", "H2-Eb1", "H2-M2", "H2-K1", "H2-D1",
]
