"""Shared configuration for the small screen pipeline.

Paths come from ``paths.py``: this screen's own data root, the large screen's
root for the objects notebooks 04 and 05 read from it, and the reference tables
committed in ``large_screen/reference/`` which both screens share.

Thresholds and the guide definitions below describe this screen and are the
values the published analysis used.
"""
import os

from paths import SCREEN_DATA, large_screen_path, reference_path, screen_path

# --- Project paths ---
PROJECT_DIR = SCREEN_DATA
OUTPUTS_DIR = screen_path("outputs", "anndata")
TEXT_DIR = screen_path("TextFiles")

# --- This screen's objects, written by the notebooks here ---
ANNDATA_RAW = os.path.join(OUTPUTS_DIR, "adataCombo.h5ad")                       # 01, 02
ANNDATA_V1 = os.path.join(OUTPUTS_DIR, "adataCombo_v1.h5ad")
ANNDATA_PROCESSED = os.path.join(OUTPUTS_DIR, "adataComboProcessed.h5ad")        # 03
ANNDATA_LEIDEN_REGOUT = os.path.join(OUTPUTS_DIR, "adataComboProcessed_leidenRegOut.h5ad")
ANNDATA_LEIDEN_TC_TRANSFERRED = os.path.join(OUTPUTS_DIR, "adataComboProcessed_leidenTCTransferred.h5ad")          # 04
ANNDATA_LEIDEN_TC_TRANSFERRED_REGOUT = os.path.join(OUTPUTS_DIR, "adataComboProcessed_leidenTCTransferred_regressedOut.h5ad")
ANNDATA_COMBO_SCREEN = screen_path("ComboScreen_cellStatesRegressedOut.h5ad")
ANNDATA_BIG_COMBO = os.path.join(OUTPUTS_DIR, "BigAndComboScreenForComBVAE.h5ad")  # 05

# --- The large screen's objects, read by 04 and 05 ---
# The screen object build_anndata/05_DownstreamIntegration writes. The original
# config looked for it under outputs/anndata/OriginalFiles/, where it is not;
# it sits in outputs/anndata/, which is also what build_anndata names.
ANNDATA_BIG_SCREEN = large_screen_path("outputs", "anndata",
                                       "adata-hash-features_singlets_05242020.h5ad")
ANNDATA_BIG_SCREEN_SINGLE_KO = large_screen_path(
    "outputs", "anndata", "OriginalFiles", "adata-hash-features_singlets_SingleKO_05242020.h5ad")
ANNDATA_BIG_SCREEN_SINGLE_KO_PER_GENE = large_screen_path(
    "outputs", "anndata", "OriginalFiles", "adata-hash-features_singlets_SingleKO_06292020_PerGENE.h5ad")

# --- Committed reference tables, shared with the large screen ---
LEIDEN_TOP_MARKERS_CSV = reference_path("Leiden_top100Markers.csv")
GUIDE_MODULES_CSV = reference_path("ME_GuideModules_leiden_6_Modules.csv")
GENE_MODULES_CSV = reference_path("ME_GeneModules_leiden_11_Modules.csv")
# --- Guide / KO definitions ---
KO_COLUMNS = [
    "Ambra1", "Ankfy1", "Crebbp", "Ep300", "Fbxw7", "Klhl6",
    "March6", "Pparg", "Rfwd2", "Socs3", "Syvn1", "Traf2",
    "Trip12", "Wdr82",
]

CONTROL_COLUMNS = ["NO_TARGET", "ONE_NON_GENE_SITE"]

ALL_GUIDE_COLUMNS = KO_COLUMNS + CONTROL_COLUMNS

# Raw CRISPR column names (as they appear in the crispr.csv files)
CRISPR_RAW_COLUMNS = [
    "Ambra1_1", "Ankfy1_1", "Crebbp_1", "Ep300_1", "Fbxw7_2", "Klhl6_1",
    "March6_1", "Pparg_1", "Rfwd2_1", "Socs3_1", "Syvn1_1", "Traf2_1",
    "Trip12_1", "Wdr82_1", "NO_TARGET_1", "ONE_NON-GENE_SITE_1",
]

# Prefix used in OLS design matrices
GENE_PREFIX_COLUMNS = [f"GENE_{ko}_" for ko in KO_COLUMNS]

# --- Gene-name corrections (R ↔ Python naming mismatches) ---
GENE_NAME_FIXES = {
    "X2810474O19Rik": "2810474O19Rik",
    "X1810037I17Rik": "1810037I17Rik",
    "X0610012G03Rik": "0610012G03Rik",
    "X2010005H15Rik": "2010005H15Rik",
    "X2010111I01Rik": "2010111I01Rik",
    "X2010107E04Rik": "2010107E04Rik",
    "X2310001H17Rik": "2310001H17Rik",
    "H2.Q6": "H2-Q6",
    "H2.Ab1": "H2-Ab1",
    "H2.K1": "H2-K1",
    "H2.DMa": "H2-DMa",
    "H2.M2": "H2-M2",
    "H2.Q7": "H2-Q7",
    "H2.D1": "H2-D1",
    "H2.Aa": "H2-Aa",
    "H2.Eb1": "H2-Eb1",
    "Atp5o.1": "Atp5o-1",
    "H2.DMb1": "H2-DMb1",
    "H2.T23": "H2-T23",
}

# --- QC thresholds ---
GUIDE_UMI_FRAC_THRESHOLD = 0.1
MT_FRAC_CUTOFF = 0.2
MIN_GENES_PER_CELL = 800
MIN_UMI_PER_GENE = 40
MAX_KO_GUIDES_PER_CELL = 2

# --- Preprocessing parameters ---
N_HVG = 3000
N_PCS = 100
N_NEIGHBORS = 20
NEIGHBOR_METRIC = "euclidean"
LEIDEN_RESOLUTION = 0.3
LEIDEN_RESOLUTION_FINAL = 0.41
REGRESS_OUT_VARS = ["n_umis", "n_genes", "mt_frac"]
N_REGRESS_JOBS = 30

# --- Linear model ---
FDR_THRESHOLD = 0.1
MIN_SIG_KOS_MODULE_GENES = 1   # for gene-module genes
MIN_SIG_KOS_OTHER_GENES = 5    # for non-module genes
