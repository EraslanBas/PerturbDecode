from libraries import *
from parameters import *


import statsmodels.api as sm
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM


def filterOutOutlierControlGuides(adata):
    
    adata.uns['Control_guides'] = [ x for x in adata.uns['feature_barcode_names'] if
                               (x.startswith(par_nongene_site_control_prefix) or 
                                x.startswith(par_not_target_control_prefix))]
    
    controlGM = adata.obs[adata.uns['Control_guides']]
    controlGM =controlGM[controlGM.sum(axis=1) == 1]
    
    adataControl = adata[controlGM.index,]
    adataControl.obs['Control_guide'] = adataControl.obs[adataControl.uns['Control_guides']].idxmax(axis=1)
    
    sc.tl.pca(adataControl, 
              use_highly_variable=True,
              n_comps=100, 
              svd_solver='arpack')
    
    
    expressionMatrix = adataControl.obsm['X_pca']
    guideMatrix = adataControl.obs[adataControl.uns['Control_guides']]
    
    
    pvalDF = pd.DataFrame()
    coefDF = pd.DataFrame()

    for j in range(0,100):
        est = sm.OLS(np.array(expressionMatrix)[:,j], np.array(guideMatrix))
        est2 = est.fit().summary2().tables[1]
        pvalDF[str(j)] = est2['P>|t|']
        coefDF[str(j)] = est2['Coef.']
        
        
    coefDF.index = adataControl.uns['Control_guides']
    
    
    iso = IsolationForest(contamination=0.1)
    yhat = iso.fit_predict(coefDF)
    k = pd.Series(coefDF.index[yhat == -1,])
    
    
    ee = EllipticEnvelope(contamination=0.1)
    yhat = ee.fit_predict(coefDF)

    k = k.append(pd.Series(coefDF.index[yhat == -1,]))
    
    
    lof = LocalOutlierFactor()
    yhat = lof.fit_predict(coefDF)
    k = k.append(pd.Series(coefDF.index[yhat == -1,]))
    
    
    ee = OneClassSVM(nu=0.01)
    yhat = ee.fit_predict(coefDF)
    k = k.append(pd.Series(coefDF.index[yhat == -1,]))
    
    allSel = pd.DataFrame(k.value_counts())
    allSel.columns = ["nClassf"]
    
    
    allSel = allSel.loc[ allSel.nClassf > 2,]
    allSel['OutlierGuides'] = allSel.index
    allSel = allSel.sort_values(by=['OutlierGuides'])
    allSel.loc[:,"OutlierGuides"].to_csv(par_outlier_controlguides_file, index=False)
    
    return()
  


if __name__ == "__main__":
    
    os.getcwd()
    os.chdir(projectDir)
    
    
    adata = sc.read(par_save_filename_5)
    
    filterOutOutlierControlGuides(adata)
    
    adata.uns['AllExpGeneNames'] = pd.Series(adata.var_names)
    
    sc.pp.filter_genes(adata, min_cells=par_mincells_for_testedgenes)
    sc.pp.filter_cells(adata, min_genes=par_mincellgenes_for_testedgenes)
    
    fBarMat = adata.obs[adata.uns['feature_barcode_names']]
    
    badFBarMat = fBarMat.loc[:,fBarMat.sum(axis=0) < par_ncell_test_threshold]
    badGuides = badFBarMat.columns.to_list()
    badGDF = pd.DataFrame(data={'guides':badGuides})
    badGDF['targetGene'] = badGDF['guides'].str.split("_", n=1, expand=True)[0]

    badControlGuides = pd.read_csv(par_outlier_controlguides_file)
    badControlGuides['targetGene'] = badControlGuides['OutlierGuides'].str.split("_", n=1, expand=True)[0]
    badControlGuides = badControlGuides.rename(columns={"OutlierGuides": "guides"})
    badGDF = pd.concat([badGDF, badControlGuides])
    badGDF = badGDF.sort_values('guides')
    
    selectedBarcodes = adata.uns['feature_barcode_names']
    selectedBarcodes = selectedBarcodes[~pd.Series(selectedBarcodes).isin(badGDF.guides.to_list())]
    adata.uns['feature_barcode_names_filtered'] = selectedBarcodes
    
    fBarMat = adata.obs[adata.uns['feature_barcode_names_filtered']]
    fBarMat[fBarMat>0] = 1
    adata = adata[fBarMat.sum(axis=1) > 0,:]
    adata.uns['feature_KO_barcode_names_filtered'] = [ x for x in adata.uns['feature_barcode_names_filtered'] 
                                                      if not (x.startswith(par_nongene_site_control_prefix) or
                                                              x.startswith(par_not_target_control_prefix))]
    adata.write(par_save_filename_7)



  

