# Parameters
projectDir="/home/eraslab1/Projects/E3Ligase/analysisSingle"
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
## After hashing info integration
par_save_filename_2 = par_save_filename_1
## After crispr feature barcode integration
par_save_filename_3 = par_save_filename_1
## After downstream integration (ie. normalization, log transformation etc.)
par_save_filename_4 = par_save_filename_1
## Anndata object containing the cells with single gene KOs
par_save_filename_5 = "outputs/anndata/adata-SingleKO.h5ad"
## Anndata object containing the cells with multiple gene KOs
par_save_filename_6 = "outputs/anndata/adata-MultipleKO.h5ad"
## Anndata object containing the cells and guides for guide effect testing
par_save_filename_7 = par_save_filename_5
## Single KO anndata object after KO guides are merged at the target gene level
par_save_filename_8 = "outputs/anndata/adata-SingleKO_PerGENE.h5ad"
## Multiple KO anndata object after KO guides are merged at the target gene level
par_save_filename_9 = 'outputs/anndata/adata-MultipleKO_PerGENE.h5ad'
## Single KO anndata object after unperturbed cells are filtered out
par_save_filename_10 = par_save_filename_8


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
par_predefined_genesets_filename='PositiveControls/DC_cellstate_genes.csv'
par_initial_guide_pool_file='./PositiveControls/GuidePoolSummary_2.csv'
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
par_selected_coef_matrix_file='./TextFiles/TargetTestRes_2.csv'

