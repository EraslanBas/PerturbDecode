from libraries import *
from parameters import *

def keepKOGuidesAtTargetGeneLevel(adata, selectedBarcodes, saveFileName, isMulti): 
    
    
    adata.uns['feature_barcode_names_filtered'] = selectedBarcodes
    
    
    fBarMat = adata.obs[adata.uns['feature_barcode_names_filtered']]
    #fBarMat[fBarMat>0] = 1
    adata = adata[fBarMat.sum(axis=1) > 0,:]
    
    adata.obs['Cell_category'] = adata.obs[adata.uns['feature_barcode_names_filtered']].idxmax(axis=1)
    adata.obs['Cell_category'] = adata.obs['Cell_category'].replace(to_replace=[r'ONE_NONGENE_SITE_.*',r'NO_TARGET_.*'],
                                                                    value='CONTROL_', 
                                                                    regex=True)
    adata.obs['Cell_category'] = [('_'.join(x.split('_')[:-1])+"_" ) for x in adata.obs['Cell_category']] 
    
    feature_barcode_names_filtered_GENES = [ x for x in adata.uns['feature_barcode_names_filtered'] if not 
                                            (x.startswith(par_nongene_site_control_prefix) or 
                                             x.startswith(par_not_target_control_prefix))]
    
    fBarMat = adata.obs[feature_barcode_names_filtered_GENES]
    
    koGenes = list(set([ ('_'.join(x.split('_')[:-1])+"_" ) for x in fBarMat.columns]))
    koGenes.sort()
    grouper = [next(p for p in koGenes if p in c) for c in fBarMat.columns]
    koGene = fBarMat.groupby(grouper, axis=1).sum()
    koGene[koGene > 0] = 1
    koGene.columns = "GENE_"+koGene.columns

    adata.obs = adata.obs.join(koGene,how="inner")
    
    adata.obs['GENE_CONTROL_'] = 0
    adata.obs['GENE_CONTROL_'][adata.obs['Cell_category'] == "CONTROL_"] = 1
    
    adata.uns['feature_barcode_names_filtered_GENES'] = [ x for x in adata.obs.columns if (x.startswith("GENE_"))]

    adata.obs = adata.obs.drop(labels=list(adata.uns['feature_barcode_names_filtered']), axis=1).copy()
    
    if isMulti:
        adata.obs['GENE_INEFFECT_'] = 0
        adata.obs['GENE_INEFFECT_'][adata.obs[adata.uns['feature_barcode_names_filtered_GENES']].sum(axis=1) == 1] = 1
        adata = adata[adata.obs['GENE_INEFFECT_'] != 1,:]
    
    adata.write(saveFileName)
    
    return()
   

if __name__ == "__main__":
    
    os.getcwd()
    os.chdir(projectDir)
    
    
    adata = sc.read(par_save_filename_7)
    
    badKOGuides = pd.read_csv(par_bad_KO_guides_file)
    badKOGuides['targetGene'] = badKOGuides['x'].str.split("_", n=1, expand=True)[0]
    badKOGuides = badKOGuides.rename(columns={"x": "guides"})
    
    selectedBarcodes = adata.uns['feature_barcode_names_filtered']
    selectedBarcodes = selectedBarcodes[~pd.Series(selectedBarcodes).isin(badKOGuides.guides.to_list())]
    
    keepKOGuidesAtTargetGeneLevel(adata, 
                                 selectedBarcodes, 
                                 par_save_filename_8, 
                                 False)
    
    adata_multi = sc.read(par_save_filename_6)
    
    keepKOGuidesAtTargetGeneLevel(adata_multi, 
                                 selectedBarcodes, 
                                 par_save_filename_9, 
                                 True)
    
    
 
    

